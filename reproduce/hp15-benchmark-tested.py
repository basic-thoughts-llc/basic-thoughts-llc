#!/usr/bin/env python3
"""Bounded, equivalent-work CPU/OpenCL measurements; no simulated network results."""
import argparse, hashlib, json, os, platform, statistics, time
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]

def measure(fn, repeats=15):
    fn()
    samples=[]
    for _ in range(repeats):
        start=time.perf_counter_ns(); fn(); samples.append((time.perf_counter_ns()-start)/1e6)
    return {'median_ms':statistics.median(samples),'p95_ms':float(np.percentile(samples,95)), 'samples_ms':samples}

def run(label):
    result={'label':label,'timestamp_unix':time.time(),'machine':platform.node(),
            'scope':'Local equivalent-work benchmark, not full MAR or Saturn integration',
            'seed':20260913,'cases':[],'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    rng=np.random.default_rng(result['seed'])
    import pyopencl as cl
    devices=[d for p in cl.get_platforms() for d in p.get_devices(device_type=cl.device_type.GPU)]
    if not devices: raise RuntimeError('A hardware GPU is required; no software fallback')
    dev=devices[0];ctx=cl.Context([dev]);q=cl.CommandQueue(ctx,properties=cl.command_queue_properties.PROFILING_ENABLE)
    result['gpu']={'name':dev.name,'vendor':dev.vendor,'driver':dev.driver_version,'compute_units':dev.max_compute_units}
    program=cl.Program(ctx, '''
    __kernel void transform(__global const float *x,__global float *y,int n){
      int i=get_global_id(0); if(i<n) y[i]=x[i]*1.25f+0.5f;
    }
    ''').build()
    kernel=cl.Kernel(program,'transform')
    for n in (4096,65536,1048576):
        x=rng.uniform(-1,1,n).astype(np.float32); ref=x*np.float32(1.25)+np.float32(.5);out=np.empty_like(x)
        a=cl.Buffer(ctx,cl.mem_flags.READ_ONLY|cl.mem_flags.COPY_HOST_PTR,hostbuf=x)
        b=cl.Buffer(ctx,cl.mem_flags.WRITE_ONLY,x.nbytes)
        def gpu():
            ev=kernel(q,(n,),None,a,b,np.int32(n));ev.wait();return ev
        def e2e():
            cl.enqueue_copy(q,a,x);gpu();cl.enqueue_copy(q,out,b).wait()
        def cold():
            aa=cl.Buffer(ctx,cl.mem_flags.READ_ONLY|cl.mem_flags.COPY_HOST_PTR,hostbuf=x)
            bb=cl.Buffer(ctx,cl.mem_flags.WRITE_ONLY,x.nbytes)
            kernel(q,(n,),None,aa,bb,np.int32(n));cl.enqueue_copy(q,out,bb).wait()
        cpu=measure(lambda: np.add(np.multiply(x,np.float32(1.25)),np.float32(.5)))
        pooled=measure(e2e);fresh=measure(cold);resident=measure(gpu)
        e2e();error=float(np.max(np.abs(out-ref)))
        if not np.allclose(out,ref,rtol=1e-6,atol=1e-6):raise AssertionError('GPU numerical fidelity failed')
        device_ms=[]
        for _ in range(15):
            ev=gpu();device_ms.append((ev.profile.end-ev.profile.start)/1e6)
        result['cases'].append({'elements':n,'bytes_each_buffer':x.nbytes,'cpu':cpu,'gpu_pooled_end_to_end':pooled,
           'gpu_fresh_buffers_end_to_end':fresh,'gpu_resident_dispatch':resident,'device_kernel_median_ms':statistics.median(device_ms),
           'max_abs_error':error,'equivalent_work':True,'pooling_speedup':fresh['median_ms']/pooled['median_ms'],
           'gpu_vs_cpu_end_to_end_speedup':cpu['median_ms']/pooled['median_ms']})
    path=ROOT/'evidence'/f'benchmark-{label}.json';path.write_text(json.dumps(result,indent=2))
    print(json.dumps({'file':str(path),'gpu':result['gpu'],'cases':[{k:v for k,v in c.items() if not isinstance(v,dict)} for c in result['cases']]},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--label',default='baseline',choices=['baseline','performance','balanced-repeat']);run(p.parse_args().label)
