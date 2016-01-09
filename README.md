# LLVM extended python bindings
A extended version of the LLVM binding for Python. Updated for 3.6.2

This is an extended version of the LLVM python binding. It extends the official python 
binding to a later version (3.6.2), provides more APIs and fixed a few issues with the 
library.

## Why

The official LLVM python binding that comes with the LLVM distribution is a few versions
behind the current release. And it only implements a few APIs as illustrative purposes. 
While trying to get familiar with LLVM I took some time to fix the binding with a newer
version (3.6.2). At the time of this writing, the latest version is 3.8. More work needs
to be dond to bring it to the latest version.

There are other alternatives, *e.g.*, there are `llvmpi` and `llvmlite`. Although the former
has been since deprecated and the second was designed to be a `lite` version so as to serve
the purpose for using with `numpy`. This repository is merely an extended version of the 
official bindings. It mostly just add wrapper functions around the C-API with a number of
unit tests to illustrates the use. It is intentional to have very few logic in the language
wrapper.

## How to use
LLVM is built using CMake. While building it, add a `-DLLVM_BUILD_LLVM_DYLIB=On` option to
the invocation of CMake to make sure that the dynamic library is built.

To add the library to python path. You can either modify the PYTHONPATH environment variable,
or add a `.pth` configuration file to the site-packages directory of your python installation.
