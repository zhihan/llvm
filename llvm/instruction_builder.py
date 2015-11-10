"""Python bindings for Instruction Builder C-API."""
from .common import LLVMObject
from .common import c_object_p
from .common import get_library

from .core import Context
from .core import Value

from ctypes import c_char_p

__all__ = ['Builder']
lib = get_library()

class Builder(LLVMObject):
    def __init__(self, obj):
        LLVMObject.__init__(self, obj, disposer=lib.LLVMDisposeModule)

    @classmethod
    def create(cls, context=None):
        if context is None:
            return Builder(lib.LLVMCreateBuilder())
        else:
            return Builder(lib.LLVMCreateBuilderInContext(context))

    def add(self, lhs, rhs, name):
        return Value(lib.LLVMBuildAdd(self, lhs, rhs, name))

    def __del__(self):
        lib.LLVMDisposeBuilder(self)

def register_library(library):
    library.LLVMCreateBuilder.argtypes = []
    library.LLVMCreateBuilder.restype = c_object_p

    library.LLVMCreateBuilderInContext.argtypes = [Context]
    library.LLVMCreateBuilderInContext.restype = c_object_p

    library.LLVMBuildAdd.argtypes = [Builder, Value, Value, c_char_p]
    library.LLVMBuildAdd.restype = c_object_p

    library.LLVMDisposeBuilder.argtypes = [Builder]
    library.LLVMDisposeBuilder.restype = None
    
register_library(lib)
