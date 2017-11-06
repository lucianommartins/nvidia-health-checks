#!/usr/bin/python3 -B

import netifaces

def list_adapters():
    netdevs = []
    for output in netifaces.interfaces():
        if 'lo' not in output and 'docker' not in output and 'veth' not in output:
            netdevs.append(output)
    return(netdevs)

def is_interface_up(interface):
    addr = netifaces.ifaddresses(interface)
    return netifaces.AF_INET in addr
    
def check_netevs():
    for adapter in list_adapters():
        success = True
        if is_interface_up(adapter) is False:
            print('\033[1;33mINFO\033[0m: System has multiple adapters but', adapter, 'is unused')
            success = False
    if success is True:
        print('\033[1;32mPASS\033[0m: network configuration is properly set and used')
            
        