#!/usr/bin/python3 -B

import apt

# load the apt cache into memory
cache = apt.Cache()

# function to query apt cache looking for packages versions
def pkg_version(package, required):
    try:
        pkg = cache[package]
        status = pkg.is_installed
        if status is True:
            version = str(pkg.versions).split('=')[1][0]
            return(version, status)
        else:
            error = ('package \'' + package + '\' is not installed')
            return(error, status)
    except Exception as e:
        exception = str(e).strip('"')
        return(exception, False)


# verify CUDA metapackage -- version must be >= 9
def cuda_version():
    cuda = ['cuda', '9' ]
    version, status = pkg_version(cuda[0], cuda[1])
    if status is True:
        if int(version) >= 9:
            return('PASS')
        else:
            return('FAIL')
    else:
        return('ERROR')
        
# verify CUDA metapackage -- version must be >= 9
def cudnn_version():
    cuda = ['libcudnn7', '7' ]
    version, status = pkg_version(cuda[0], cuda[1])
    if status is True:
        if int(version) >= 7:
            return('PASS')
        else:
            return('FAIL')
    else:
        return('ERROR')

# print standard messages for the possible outputs
def message(package, status):
    if status == "PASS":
        return('\033[1;32m' + status + '\33[0m: ' + package + ' is on the recommended version')
    if status == "FAIL":
        return('\033[1;31m' + status + '\033[0m: ' + package + ' needs to be updated')
    if status == "ERROR":
        return('\033[1;31m' + status + '\033[0m: ' + package + ' is not installed')
