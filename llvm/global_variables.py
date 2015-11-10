"""Python bindings for GlobalVariables."""
from .common import LLVMObject
from .common import c_object_p
"""GlobalVariable bindings for LLVM."""
from .common import get_library

from .core import Context
from .core import Module
from .core import Type
from .core import Value

from ctypes import c_char_p

__all__ = ['Global']
lib = get_library()

class Global(LLVMObject):
    def __init__(self, obj):
        LLVMObject.__init__(self, obj)

    @classmethod
    def add(cls, module, ty, name):
        return Value(lib.LLVMAddGlobal(module, ty, name))

    @classmethod
    def get(cls, module, name):
        return Value(lib.LLVMGetNamedGlobal(module, name))

def register_library(library):
    library.LLVMAddGlobal.argtypes = [Module, Type, c_char_p]
    library.LLVMAddGlobal.restype = c_object_p

    library.LLVMGetNamedGlobal.argtypes = [Module, c_char_p]
    library.LLVMGetNamedGlobal.restype = c_object_p

        
register_library(lib)
