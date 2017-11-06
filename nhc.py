#!/usr/bin/python3 -B

from nvidia_packages import *
from nvidia_platform import *
from nvidia_network import *

# check DGX platform configuration
print('\033[1mTEST\033[0m - Verifying DGX platform general configuration')
dgx_check()
print('\n')

# check DGX memory configuration
print('\033[1mTEST\033[0m - Verifying DGX platform memory configuration')
memory_check()
print('\n')

# check DGX CPU configuration
print('\033[1mTEST\033[0m - Verifying DGX platform CPU configuration')
cpu_check()
print('\n')

# check DGX GPU configuration
print('\033[1mTEST\033[0m - Verifying DGX platform GPU configuration')
gpu_check()
print('\n')

# verify CUDA version
print('\033[1mTEST\033[0m - Verifying DGX platform CUDA configuration')
status_cuda = cuda_version()
print(message('cuda', status_cuda))
print('\n')

# verify libcudnn version
print('\033[1mTEST\033[0m - Verifying DGX platform CuDNN configuration')
status_cudnn = cudnn_version()
print(message('libcudnn', status_cudnn))
print('\n')

# verify network adapters
print('\033[1mTEST\033[0m - Verifying DGX platform network configuration')
check_netevs()
print('\n')