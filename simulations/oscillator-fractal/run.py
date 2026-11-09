"""Finite graphene-microtubule oscillator design simulation, not hardware validation."""
import json, platform, time, hashlib
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from manifold_reference import braid_gate

OUT = Path(__file__).parent
WORD = [1, 2, -1, 2, 1, -2, 1, 2] * 2
PRIMES = [2, 3, 5, 13, 89]

def prepare(h, v, oscillators=1):
    # Each VM retains its two independent binary recursion paths.
    addresses = [(format(x, f'0{h}b'), format(y, f'0{v}b'))
                 for y in range(2**v) for x in range(2**h)]
    n = len(addresses) * oscillators
    # Four logical qubits = sixteen complex amplitudes PER oscillator.
    state = np.full((n, 16), 0.25, dtype=np.complex128)
    x = np.tile(np.arange(2**h), 2**v).repeat(oscillators)
    y = np.repeat(np.arange(2**v), 2**h).repeat(oscillators)
    theta = 0.1 + (x + 2*y) / (2**h + 2**v)
    weights = np.array([int(i).bit_count() for i in range(16)])
    # Phenomenological controller phase; no empirical graphene coupling claimed.
    phases = np.exp(1j * theta[:, None] * weights[None, :])
    gates = [np.kron(braid_gate(g), np.eye(8)) for g in WORD]
    return addresses, state, phases, gates

def evolve(state, phases, gates, batch):
    result = state.copy()
    if batch:
        for gate in gates:
            result *= phases
            result = result @ gate.T
    else:
        for i in range(len(result)):
            for gate in gates:
                result[i] *= phases[i]
                result[i] = gate @ result[i]
    return result

def main():
    rows = []
    for h, v in [(1,1),(3,1),(3,3),(5,3),(5,5),(7,5),(7,7)]:
        addresses, state, phases, gates = prepare(h,v)
        assert len(set(addresses)) == len(addresses)
        a = evolve(state, phases, gates, False)
        b = evolve(state, phases, gates, True)
        error = float(np.max(np.abs(a-b)))
        norm_error = float(np.max(np.abs(np.sum(abs(b)**2,axis=1)-1)))
        assert error < 1e-12 and norm_error < 1e-12
        timings = {'scalar': [], 'batch': []}
        for trial in range(5):
            for batch in ([False,True] if trial%2==0 else [True,False]):
                start = time.perf_counter()
                evolve(state, phases, gates, batch)
                timings['batch' if batch else 'scalar'].append(time.perf_counter()-start)
        s, t = [float(np.median(timings[k])) for k in ('scalar','batch')]
        row = dict(horizontal_depth=h,vertical_depth=v,vms=len(state),oscillators=len(state),
                   qubits_per_oscillator=4,logical_qubits=4*len(state),state_bytes=state.nbytes,
                   scalar_seconds=s,batch_seconds=t,speedup=s/t,oscillators_per_second=len(state)/t,
                   max_amplitude_error=error,max_norm_error=norm_error,trials=timings)
        rows.append(row)
        print(json.dumps(row), flush=True)
    # Spectral carrier check on endpoint-exclusive grid, below Nyquist.
    grid = np.arange(1024)/1024
    carriers = np.exp(2j*np.pi*np.outer(PRIMES,grid))
    gram = carriers @ carriers.conj().T / len(grid)
    crosstalk = float(np.max(abs(gram-np.eye(len(PRIMES)))))
    # Order must matter; guard against replacing a braid word by counts.
    noncommuting = float(np.linalg.norm(braid_gate(1)@braid_gate(2)-braid_gate(2)@braid_gate(1)))
    assert noncommuting > 1e-6 and crosstalk < 1e-12
    report = dict(host=platform.node(),platform=platform.platform(),numpy=np.__version__,
        scope='Classical CPU simulation; scalar NumPy dispatch versus batched NumPy; setup excluded equally.',
        assumptions=['One graphene-microtubule oscillator per VM; four logical qubits each.',
                     'Independent oscillator states; no cross-oscillator entanglement represented.',
                     'Braid generator embedded on first logical qubit, other three retained.',
                     'Controller phase is phenomenological, not calibrated to physical material.',
                     'Spectral tones are normalized mathematical carriers, not measured THz modes.'],
        braid_word=WORD,primes=PRIMES,carrier_crosstalk=crosstalk,braid_noncommutator=noncommuting,results=rows)
    (OUT/'results.json').write_text(json.dumps(report,indent=2)+'\n')
    plt.style.use('dark_background')
    fig, axes = plt.subplots(2,2,figsize=(13,9),layout='constrained')
    n = [r['vms'] for r in rows]
    axes[0,0].plot(n,[r['speedup'] for r in rows],'o-',color='#54ded4')
    axes[0,0].axhline(1,ls='--',label='1× scalar reference',alpha=.6)
    axes[0,0].set(xscale='log',xlabel='VMs / oscillators',ylabel='Scalar time ÷ batch time',title='Measured equal-work speedup')
    axes[0,0].legend()
    for key in ('scalar','batch'):
        axes[0,1].plot(n,[r[key+'_seconds']*1000 for r in rows],'o-',label=key)
    axes[0,1].set(xscale='log',yscale='log',xlabel='VMs / oscillators',ylabel='Median latency (ms)',title='16 ordered phase + braid stages')
    axes[0,1].legend()
    im=axes[1,0].imshow(np.angle(b[:,0]).reshape(2**v,2**h),cmap='twilight',vmin=-np.pi,vmax=np.pi,origin='lower')
    axes[1,0].set(title='Final amplitude phase across recursive VM frontier',xlabel='Horizontal address',ylabel='Vertical address')
    fig.colorbar(im,ax=axes[1,0],label='Radians')
    for i,p in enumerate(PRIMES): axes[1,1].plot(grid[:128],carriers[i,:128].real+i*2.5,label=str(p))
    axes[1,1].set(title='Prime-index carrier modes (offset for visibility)',xlabel='Normalized interval',ylabel='Real amplitude + display offset')
    axes[1,1].legend(title='Cycles / interval',ncol=5,fontsize=8)
    fig.suptitle('OMEGA · Four-qubit oscillator / recursive manifold simulation',fontsize=17)
    fig.savefig(OUT/'simulation.png',dpi=160)
    fig.savefig(OUT/'simulation.svg')
    hashes = {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.iterdir() if p.is_file() and p.name!='sha256.json'}
    (OUT/'sha256.json').write_text(json.dumps(hashes,indent=2)+'\n')

if __name__ == '__main__': main()
