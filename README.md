# NHC - NVIDIA Health Check

NVIDIA Health Check (NHC) is a best practices and configuration validation framework
used to assess if DGX platform servers (DGX Station and DGX-1) are on the best 
possible state to be used on their best performance and stability.

NHC framework is developed using python language and allows inclusion of custom and
ad-hoc checks, delivering extensive and flexible checking mechanisms.

It is highly recommended to address all checks marked as FAIL on NHC execution before
start running deep learning frameworks and models on DGX platform servers.

## Requirements

NHC depends only of few extra packages to be installed before using it. They are:

- python-3 (normally already installed on the standard DGX platform setup)
- python3-dev
- python3-pip
- python-netifaces module
- python3-setuptools module

## Installation

Firstly all those required packages must be installed on the target system. Those
packages are present on the standard Ubuntu 16.04 repositories, being their
installation performed as below:

```
$ sudo apt-get install <package name>
```

Once all requirements are installed, just download the deb package (NHC.deb) present
on this repository and run the installation as below:

```
$ sudo dpkg -i NHC.deb
Selecting previously unselected package NHC.
(Reading database ... 232864 files and directories currently installed.)
Preparing to unpack nhc.deb ...
Unpacking NHC (0.1b) ...
Setting up NHC (0.1b) ...
```

You can validate that the package was successfully installed by running:

```
$ dpkg -l nhc
||/ Name                                       Version                    Architecture               Description
+++-==========================================-==========================-==========================-====================================
ii  nhc                                        0.1b                       all                        NVIDIA Health Check for DGX Platform
```

## Running NHC

NHC execution is really straightforward and does not require any complex knowledge
or previous learning to be performed. All detailed information as also the steps to
perform the checks are embedded on NHC framework.

The execution runs as below:

```
$ nhc
TEST - Verifying DGX platform general configuration
PASS: OS software layer is on recommended levels


TEST - Verifying DGX platform memory configuration
FAIL: system memory is below the recommended setup


TEST - Verifying DGX platform CPU configuration
FAIL: system CPU is below the recommended setup


TEST - Verifying DGX platform filesystems usage
PASS: No filesystems are beyond 80% used


TEST - Verifying DGX platform GPU configuration
INFO: It is recommended to replace Pascal GPUs by Volta ones
PASS: GPU devices are properly set


TEST - Verifying DGX platform CUDA configuration
PASS: cuda is on the recommended version


TEST - Verifying DGX platform CuDNN configuration
PASS: libcudnn is on the recommended version


TEST - Verifying DGX platform network configuration
INFO: System has multiple adapters but enp2s0f1 is unused
```

It is highly recommended to address all checks marked as FAIL on NHC execution before
start running deep learning frameworks and models on DGX platform servers.
