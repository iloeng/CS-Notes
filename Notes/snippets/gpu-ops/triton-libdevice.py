# https://triton-lang.org/main/getting-started/tutorials/07-extern-functions.html
# https://docs.nvidia.com/cuda/libdevice-users-guide/index.html
# https://github.com/ROCm/llvm-project/tree/amd-staging/amd/device-libs/ocml/src

import torch

import triton
import triton.language as tl
import inspect
import os
from triton.language.extra import libdevice

from pathlib import Path

DEVICE = torch.cuda.current_device()

@triton.jit
def asin_kernel(
    x_ptr,
    y_ptr,
    n_elements,
    BLOCK_SIZE: tl.constexpr,
):
    pid = tl.program_id(axis=0)
    block_start = pid * BLOCK_SIZE
    offsets = block_start + tl.arange(0, BLOCK_SIZE)
    mask = offsets < n_elements
    x = tl.load(x_ptr + offsets, mask=mask)
    x = libdevice.asin(x)
    tl.store(y_ptr + offsets, x, mask=mask)


# use the default libdevice library path encoded in triton/language/math.py

torch.manual_seed(0)
size = 98432
x = torch.rand(size, device=DEVICE)
output_triton = torch.zeros(size, device=DEVICE)
output_torch = torch.asin(x)
assert x.is_cuda and output_triton.is_cuda
n_elements = output_torch.numel()
grid = lambda meta: (triton.cdiv(n_elements, meta['BLOCK_SIZE']), )
asin_kernel[grid](x, output_triton, n_elements, BLOCK_SIZE=1024)
print(output_torch)
print(output_triton)
print(f'The maximum difference between torch and triton is '
      f'{torch.max(torch.abs(output_torch - output_triton))}')


# customize the libdevice library path by passing the path to the libdevice library to the asin kernel.

def is_cuda():
    return triton.runtime.driver.active.get_current_target().backend == "cuda"


def is_hip():
    return triton.runtime.driver.active.get_current_target().backend == "hip"


current_file = inspect.getfile(inspect.currentframe())
current_dir = Path(os.path.dirname(os.path.abspath(current_file)))

if is_cuda():
    # libdir = current_dir.parent.parent / 'third_party/nvidia/backend/lib'
    libdir = Path('/usr/local/cuda/nvvm/libdevice')
    extern_libs = {'libdevice': str(libdir / 'libdevice.10.bc')}
elif is_hip():
    # libdir = current_dir.parent.parent / 'third_party/amd/backend/lib'
    libdir = Path('/usr/local/cuda/nvvm/libdevice')
    extern_libs = {}
    libs = ["ocml", "ockl"]
    for lib in libs:
        extern_libs[lib] = str(libdir / f'{lib}.bc')
else:
    raise RuntimeError('unknown backend')

output_triton = torch.empty_like(x)
asin_kernel[grid](x, output_triton, n_elements, BLOCK_SIZE=1024, extern_libs=extern_libs)
print(output_torch)
print(output_triton)
print(f'The maximum difference between torch and triton is '
      f'{torch.max(torch.abs(output_torch - output_triton))}')