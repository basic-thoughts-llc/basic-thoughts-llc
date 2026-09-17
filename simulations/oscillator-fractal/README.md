# OMEGA · Four-qubit oscillator simulation

Every materialized fractal VM contains one modeled graphene–microtubule oscillator, assigned four logical qubits (16 complex128 amplitudes). Horizontal and vertical recursion addresses are retained separately. The materialized frontier grows from 4 to 16,384 VMs.

![Measured simulation](simulation.png)

## Reproduce

```bash
python3 -m venv .venv
.venv/bin/pip install numpy matplotlib
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 .venv/bin/python run.py
```

Five alternating-order trials per case follow correctness checks and warmup. Compare median scalar dispatch against median batched dispatch, with identical initial states, phase schedules, braid word, precision and output shape. Setup is excluded from both. This measures Python/NumPy batching speedup, not acceleration against optimized GPU code or physical quantum hardware. Results are from Red, not the S26.

## Four-qubit interpretation

Each oscillator stores a full 16-amplitude local state. Across oscillators the state is factorized; cross-oscillator entanglement is not simulated. At 16,384 oscillators there are 65,536 logical qubit labels, but this is NOT a dense 65,536-qubit quantum simulation. State arrays use 4 MiB, excluding phase arrays, temporary arrays and process overhead. A general entangled register would require 2^(4N) amplitudes.

The graphene–microtubule controller is a phenomenological phase gate. Four physical qubits per oscillator is the user's architectural assumption, not a measured device property. Braid generators from the preserved reference are embedded on the first logical qubit; the remaining three are retained. No calibrated graphene Hamiltonian, microtubule material dynamics or plasma containment is claimed.

## Scope map

OMEGA is the orchestrator; LISA is part of OMEGA's identity. BTOL is Basic Thoughts Omega Language (.btol). MAR twin-core, Murphy Manifold, Saturn, PAION/RIMAC, OMEGA Telemetry, Monument, Factory, Sentinel and audit remain distinct architectural components. This benchmark implements the finite recursive oscillator kernel and normalized spectral carrier test. It does not claim to deploy those services, implement the complete MAR staged dynamics, or run inference VMs.

The display → spectral → manifold → VM → oscillator → readout design remains the integration context. Proposed containment, soliton storage and hardware output translation remain design interfaces. “Fractal compression” does not describe a compression result here.

## Evidence

`results.json` contains all timings, errors, environment and assumptions. `run.py` contains the executed model; `manifold_reference.py` preserves the recovered reference byte-for-byte (source SHA-256 1c3a3504bbbf997445a05f5f3634a931eadc5815d43905a7498e2712c6a7c1f9). `sha256.json` records artifact hashes. Spectral frequencies 2, 3, 5, 13, 89 are cycles per normalized interval, with 1,024 samples; orthogonality follows the sampled Fourier grid, not primality alone.

Measured peak: **25.39×** at **1,024 oscillators**. The 59× target was not reached. All seven cases, including declining speedup at larger frontiers, are retained.
