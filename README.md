# example
An repository showing an example of use for the sparpy/aboria libraries

## Prerequisites:

You need to have the Boost libraries and the VTK libraries installed on your 
computer. E.g. on Ubuntu you can use apt-get

```bash
$ sudo apt install libboost-dev libvtk6-dev
```

## Compiling and running the example:

1. clone the `sparpy` repository to your computer

```bash
$ git clone https://github.com/martinjrobins/sparpy
```

2. make a build directory within the sparpy source tree, and use CMake to 
   configure the project. 

```bash
$ cd sparpy
$ mkdir build
$ cd build
$ cmake ..
```

3. Assuming you don't get any errors here, you can then compile sparpy using 
   make

```bash
$ make
```

4. Now you need to tell Python where the sparpy library is, so add the build 
   directory to your PYTHONPATH. For example, in bash (Ubuntu) you use

```bash
$ export set PYTHONPATH=/path/to/sparpy/build
```

5. Now clone this repository and run the example python script to check that it 
   is working

```bash
$ cd ../..
$ git clone https://github.com/martinjrobins/example
$ cd example
$ python example.py
```

6. You now should have a bunch of `integrate<outputset>.vtu` files in the 
   example directory. You can open these with Paraview (`sudo apt install 
   paraview`) and view the simulation output if you wish, or use matplotlib 
   within Python to plot the data

7. You might also want to go back to your sparpy build directory and recompile 
   the library in release mode (all optimisations enabled). To do this, try 
   using `ccmake`, which is a simple gui for CMake

```bash
$ cd /path/to/sparpy/build
$ ccmake .
```

8. Put `Release` in the `CMAKE_BUILD_TYPE` variable field, then configure and 
   generate the project (i.e. hit `c`, then `g`). After this you can re-build 
   the project using make

```bash
$ make
```

