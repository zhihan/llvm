"""Python bindings for Instruction Builder C-API."""
from .common import LLVMObject
from .common import c_object_p
from .common import get_library

from .core import Context
from .core import Value
from .core import BasicBlock
from .core import Type
from .core import IntPredicate

from ctypes import c_char_p
from ctypes import c_int

__all__ = ['Builder']
lib = get_library()

class Builder(LLVMObject):
    """A Wrapper class for the instruction builder."""
    def __init__(self, obj):
        LLVMObject.__init__(self, obj, disposer=lib.LLVMDisposeBuilder)

    @classmethod
    def create(cls, context=None):
        if context is None:
            return Builder(lib.LLVMCreateBuilder())
        else:
            return Builder(lib.LLVMCreateBuilderInContext(context))

    def add(self, lhs, rhs, name):
        """Add"""
        return Value(lib.LLVMBuildAdd(self, lhs, rhs, name))

    def fadd(self, lhs, rhs, name):
        """Add (floating point)"""
        return Value(lib.LLVMBuildFAdd(self, lhs, rhs, name))

    def sub(self, lhs, rhs, name):
        """Subtract"""
        return Value(lib.LLVMBuildSub(self, lhs, rhs, name))

    def mul(self, lhs, rhs, name):
        """Multiply"""
        return Value(lib.LLVMBuildMul(self, lhs, rhs, name))

    def load(self, pointer, name):
        """Load the content of a pointer"""
        return Value(lib.LLVMBuildLoad(self, pointer, name))

    def ret(self, value):
        """Return"""
        return Value(lib.LLVMBuildRet(self, value))

    def alloca(self, ty, name):
        """Alloca"""
        return Value(lib.LLVMBuildAlloca(self, ty, name))

    def store(self, val, ptr):
        return Value(lib.LLVMBuildStore(self, val, ptr))

    def load(self, val, name):
        return Value(lib.LLVMBuildLoad(self, val, name))

    def int_signed_lt(self, lhs, rhs, name):
        return Value(lib.LLVMBuildICmp(self, IntPredicate.SLT.value, lhs, rhs, name))

    def position_at_end(self, bb):
        lib.LLVMPositionBuilderAtEnd(self, bb)

def register_library(library):
    library.LLVMCreateBuilder.argtypes = []
    library.LLVMCreateBuilder.restype = c_object_p

    library.LLVMCreateBuilderInContext.argtypes = [Context]
    library.LLVMCreateBuilderInContext.restype = c_object_p

    library.LLVMBuildAdd.argtypes = [Builder, Value, Value, c_char_p]
    library.LLVMBuildAdd.restype = c_object_p

    library.LLVMBuildFAdd.argtypes = [Builder, Value, Value, c_char_p]
    library.LLVMBuildFAdd.restype = c_object_p
    
    library.LLVMBuildSub.argtypes = [Builder, Value, Value, c_char_p]
    library.LLVMBuildSub.restype = c_object_p

    library.LLVMBuildMul.argtypes = [Builder, Value, Value, c_char_p]
    library.LLVMBuildMul.restype = c_object_p

    library.LLVMBuildICmp.argtypes = [Builder, c_int, Value, Value, c_char_p]
    library.LLVMBuildICmp.restype = c_object_p
    
    library.LLVMBuildRet.argtypes = [Builder, Value]
    library.LLVMBuildRet.restype = c_object_p

    library.LLVMDisposeBuilder.argtypes = [Builder]
    library.LLVMDisposeBuilder.restype = None

    library.LLVMPositionBuilderAtEnd.argtypes = [Builder, BasicBlock]
    library.LLVMPositionBuilderAtEnd.restype = None

    library.LLVMBuildAlloca.argtypes = [Builder, Type, c_char_p]
    library.LLVMBuildAlloca.restype = c_object_p

    library.LLVMBuildStore.argtypes = [Builder, Value, Value]
    library.LLVMBuildStore.restype = c_object_p

    library.LLVMBuildLoad.argtypes = [Builder, Value, c_char_p]
    library.LLVMBuildLoad.restype = c_object_p
                
register_library(lib)
