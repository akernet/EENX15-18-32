# Building UHD Applications using CMake

This directory contains a tiny example of a UHD-based application.
Unlike the other examples, it is completely independent of the UHD
source tree and can be compiled from any path as long as UHD is
currently installed on the current machine.

To try it out, run these commands:
```bash
$ mkdir build/ # Creates a new build directory
$ cd build/
$ cmake ..
$ make
```

This will find the UHD libraries, and link and compile the example
program. Include header directories and library names are automatically
gathered.

See the CMakeLists.txt file to figure out how to set up a build system.

```bash
./main --tx-rate 64e3 --rx-rate 64e3 --tx-freq 100e6 --rx-freq 100e6 --wave-type COMB --wave-freq 2000 --tx-gain 60 --rx-gain 20 --type double --tx-bw 50e5 --rx-bw 50e5
```

