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
from ctypes import c_bool

__all__ = ['Global']
lib = get_library()

class Global(Value):
    def __init__(self, obj):
        LLVMObject.__init__(self, obj)

    @classmethod
    def add(cls, module, ty, name):
        return Global(lib.LLVMAddGlobal(module, ty, name))

    @classmethod
    def get(cls, module, name):
        return Global(lib.LLVMGetNamedGlobal(module, name))

    def set_initializer(self, value):
        lib.LLVMSetInitializer(self, value)

    def get_initializer(self):
        return Value(lib.LLVMGetInitializer(self))

    def set_const(self, tf):
        lib.LLVMSetGlobalConstant(self, tf)

    def is_const(self):
        return lib.LLVMIsGlobalConstant(self)
        

def register_library(library):
    library.LLVMAddGlobal.argtypes = [Module, Type, c_char_p]
    library.LLVMAddGlobal.restype = c_object_p

    library.LLVMGetNamedGlobal.argtypes = [Module, c_char_p]
    library.LLVMGetNamedGlobal.restype = c_object_p

    library.LLVMSetInitializer.argtypes = [Value, Value]
    library.LLVMSetInitializer.restype = None

    library.LLVMGetInitializer.argtypes = [Value]
    library.LLVMGetInitializer.restype = c_object_p

    library.LLVMSetGlobalConstant.argtypes = [Value, c_bool]
    library.LLVMSetGlobalConstant.restype = None

    library.LLVMIsGlobalConstant.argtypes = [Value]
    library.LLVMIsGlobalConstant.restype = bool
        
register_library(lib)
