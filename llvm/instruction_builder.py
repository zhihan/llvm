"""Python bindings for Instruction Builder C-API."""
from .common import LLVMObject
from .common import c_object_p
from .common import get_library

from .core import Context
from .core import Value
from .core import BasicBlock

from ctypes import c_char_p

__all__ = ['Builder']
lib = get_library()

class Builder(LLVMObject):
    def __init__(self, obj):
        LLVMObject.__init__(self, obj, disposer=lib.LLVMDisposeBuilder)

    @classmethod
    def create(cls, context=None):
        if context is None:
            return Builder(lib.LLVMCreateBuilder())
        else:
            return Builder(lib.LLVMCreateBuilderInContext(context))

    def add(self, lhs, rhs, name):
        return Value(lib.LLVMBuildAdd(self, lhs, rhs, name))

    def sub(self, lhs, rhs, name):
        return Value(lib.LLVMBuildSub(self, lhs, rhs, name))

    def mul(self, lhs, rhs, name):
        return Value(lib.LLVMBuildMul(self, lhs, rhs, name))

    def load(self, pointer, name):
        return Value(lib.LLVMBuildLoad(self, pointer, name))

    def ret(self, value):
        return Value(lib.LLVMBuildRet(self, value))

    def position_at_end(self, bb):
        lib.LLVMPositionBuilderAtEnd(self, bb)

        

def register_library(library):
    library.LLVMCreateBuilder.argtypes = []
    library.LLVMCreateBuilder.restype = c_object_p

    library.LLVMCreateBuilderInContext.argtypes = [Context]
    library.LLVMCreateBuilderInContext.restype = c_object_p

    library.LLVMBuildAdd.argtypes = [Builder, Value, Value, c_char_p]
    library.LLVMBuildAdd.restype = c_object_p

    library.LLVMBuildSub.argtypes = [Builder, Value, Value, c_char_p]
    library.LLVMBuildSub.restype = c_object_p

    library.LLVMBuildMul.argtypes = [Builder, Value, Value, c_char_p]
    library.LLVMBuildMul.restype = c_object_p

    library.LLVMBuildRet.argtypes = [Builder, Value]
    library.LLVMBuildRet.restype = c_object_p

    library.LLVMBuildLoad.argtypes = [Builder, Value, c_char_p]
    library.LLVMBuildLoad.restype = c_object_p

    library.LLVMDisposeBuilder.argtypes = [Builder]
    library.LLVMDisposeBuilder.restype = None

    library.LLVMPositionBuilderAtEnd.argtypes = [Builder, BasicBlock]
    library.LLVMPositionBuilderAtEnd.restype = None
    
register_library(lib)
