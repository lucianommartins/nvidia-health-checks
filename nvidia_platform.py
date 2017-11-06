#!/usr/bin/python3 -B

import platform
from collections import OrderedDict
from subprocess import Popen, PIPE, TimeoutExpired

# get OS related information
def platform_info():
    distro = platform.linux_distribution()
    return(distro)

# get DGX platform related information
def dgx_info():
    dgx = {}
    with open('/etc/dgx-release') as file:
        for line in file:
            field = line.split('=')[0]
            value = line.split('=')[1].strip('"\n')
            dgx.update({ field : value })
    return(dgx)

# get system memory information
def memory_info():
    
    meminfo=OrderedDict()
    with open('/proc/meminfo') as file:
        for line in file:
            meminfo[line.split(':')[0]] = line.split(':')[1].strip()
    return(int(meminfo['MemTotal'].split()[0]))

# get system CPU information
def cpu_info():
    count = 0
    with open('/proc/cpuinfo') as file:
        for line in file:
            if 'processor' in line:
                count += 1
    return(count)

# get GPU related information
def gpu_info():
    try:
        command = ['nvidia-smi', 
        '--query-gpu=gpu_name,gpu_bus_id,vbios_version,temperature.gpu,pcie.link.gen.current', 
        '--format=csv,noheader']
        cmd = Popen(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        output = cmd.communicate(timeout=10)[0]
        gpus = []
        for line in output.splitlines():
            gpus.append(line)
        return(gpus)
    except TimeoutExpired:
            cmd.kill()
            return('timeout')

def fs_info():
    command = ['df', '-h']
    df = Popen(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    output = df.communicate()[0]
    return(output)

# verify OS software layer
def dgx_check():
    standard_ubuntu = '16.04'
    standard_dgx_ver = '3.1.2'
    os_release = platform_info()[1]
    dgx_sw_ver = dgx_info()['DGX_SWBUILD_VERSION']
    if os_release == standard_ubuntu and dgx_sw_ver == standard_dgx_ver:
        print('\033[1;32mPASS\033[0m: OS software layer is on recommended levels')
    else:
        print('\033[1;31mFAIL\033[0m: OS software layer needs to be upgraded')

# verify memory resources for DGX platform
def memory_check():
    platform = dgx_info()['DGX_NAME']
    total_mem = int(memory_info())
    if (platform == 'DGX Station' and total_mem >= 268435456) or \
        (platform == 'DGX-1' and total_mem >= 536870912):
        print("\033[1;32mPASS\033[0m: system memory is properly set")
    else:
        print("\033[1;31mFAIL\033[0m: system memory is below the recommended setup")

# verify CPU resources for DGX platform
def cpu_check():
    platform = dgx_info()['DGX_NAME']
    total_cpu = int(cpu_info())
    if (platform == 'DGX Station' and total_cpu == 20) or \
        (platform == 'DGX-1' and total_cpu == 40):
        print("\033[1;32mPASS\033[0m: system CPU is properly set")
    else:
        print("\033[1;31mFAIL\033[0m: system CPU is below the recommended setup")

# verify GPU resources for DGX platform
def gpu_check():
    platform = dgx_info()['DGX_NAME']
    gpu_names = []
    gpu_bus_ids = []
    vbios_versions = []
    temperatures = []
    pcie_links = []
    gpus = gpu_info()
    n_gpus = int(len(gpus))
    standard_vbios = '86.00.3A.00.04' # TODO: check vbios for Volta
    for gpu in gpus:
        gpu_names.append(gpu.split(',')[0].strip(' '))
        gpu_bus_ids.append(gpu.split(',')[1].strip(' '))
        vbios_versions.append(gpu.split(',')[2].strip(' '))
        temperatures.append(gpu.split(',')[3].strip(' '))
        pcie_links.append(gpu.split(',')[4].strip(' '))
    
    if 'P100' in gpu_names[0]:
        print('\033[1;33mINFO\033[0m: It is recommended to replace Pascal GPUs by Volta ones')
        
    if (platform == 'DGX Station' and n_gpus == 4) or \
       (platform == 'DGX-1' and n_gpus == 8):
        
        vbios_ok = True
        bad_vbios = []
        for vbios in vbios_versions:
            if vbios != standard_vbios:
                vbios_ok = False
                bad_vbios.append(vbios_versions.index(vbios))

        temp_ok = True
        bad_temp = []
        for temperature in temperatures:
            if int(temperature) > 70:
                temp_ok = False
                bad_temp.append(temperatures.index(temperature))
                
        pcie_ok = True
        bad_pcie = []
        for pcie_link in pcie_links:
            if int(pcie_link) < 3:
                pcie_ok = False
                bad_pcie.append(pcie_links.index(pcie_link))

        if vbios_ok is False:
            print('\033[1;31mFAIL\033[0m: GPU issues - bad vbios on the following GPUs:')
            for count in bad_vbios:
                print(gpus[count])

        elif temp_ok is False:
            print('\033[1;31mFAIL\033[0m: GPU issues - bad temperature on the following GPUs:')
            for count in bad_temp:
                print(gpus[count])

        elif pcie_ok is False:
            print('\033[1;31mFAIL\033[0m: GPU issues - bad pcie links on the following GPUs:')
            for count in bad_pcie:
                print(gpus[count])
        else:
            print('\033[1;32mPASS\033[0m: GPU devices are properly set')
    
    else:
        print('\033[1;31mFAIL\033[0m: GPU setup is invalid, please verify')

def fs_check():
    output = fs_info()
    bad_fs = []
    fs_ok = True
    for line in output.splitlines():
        if '/dev/' in line:
            used = line.split()[4].strip('%')
            if int(used) > 80:
                fs_ok = False
                bad_fs.append(line)
    if fs_ok is True:
        print('\033[1;32mPASS\033[0m: No filesystems are beyond 80% used')
    else:
        print('\033[1;31mFAIL\033[0m: The following filesystems are more than 80% used')
        print('\n'.join(str(fs) for fs in bad_fs))
