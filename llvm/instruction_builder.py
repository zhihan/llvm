"""Python bindings for Instruction Builder C-API."""
from .common import LLVMObject
from .common import c_object_p
from .common import get_library

from .core import Context
from .core import Value
from .core import BasicBlock
from .core import Type
from .core import IntPredicate
from .core import PhiNode
from .core import Function

from . import util

from ctypes import c_char_p
from ctypes import c_int
from ctypes import POINTER
from ctypes import c_uint
from ctypes import c_void_p


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
        return Value(lib.LLVMBuildAdd(self, lhs, rhs, name.encode()))

    def fadd(self, lhs, rhs, name):
        """Add (floating point)"""
        return Value(lib.LLVMBuildFAdd(self, lhs, rhs, name.encode()))

    def sub(self, lhs, rhs, name):
        """Subtract"""
        return Value(lib.LLVMBuildSub(self, lhs, rhs, name.encode()))

    def mul(self, lhs, rhs, name):
        """Multiply"""
        return Value(lib.LLVMBuildMul(self, lhs, rhs, name.encode()))

    def ret(self, value):
        """Return"""
        return Value(lib.LLVMBuildRet(self, value))
    
    def ret_void(self):
        return Value(lib.LLVMBuildRetVoid(self))
    
    def alloca(self, ty, name):
        """Alloca"""
        return Value(lib.LLVMBuildAlloca(self, ty, name.encode()))

    def alloca_array(self, ty, val, name):
        return Value(lib.LLVMBuildArrayAlloca(self, ty, val, name.encode()))

    def store(self, val, ptr):
        """Store the value in a pointer"""
        return Value(lib.LLVMBuildStore(self, val, ptr))

    def load(self, val, name):
        """Load the content of a pointer into a temp value"""
        return Value(lib.LLVMBuildLoad(self, val, name.encode()))

    def branch(self, dest):
        """Goto a block"""
        return Value(lib.LLVMBuildBr(self, dest))

    def conditional_branch(self, cond, true_branch, false_branch):
        return Value(lib.LLVMBuildCondBr(self, cond, true_branch, false_branch))

    def int_signed_lt(self, lhs, rhs, name):
        return Value(
            lib.LLVMBuildICmp(
                self, IntPredicate.SLT.value, lhs, rhs, name.encode()))

    def neg(self, val, name):
        return Value(lib.LLVMBuildNeg(self, val, name.encode()))

    def phi(self, ty, name):
        return PhiNode(lib.LLVMBuildPhi(self, ty, name.encode()))

    def call(self, fn, args, name):
        count, args_array = util.to_c_array(args)
        return Value(
            lib.LLVMBuildCall(
                self, fn, args_array, count, name.encode()))
    
    def insert_value(self, arr, val, idx, name):
        return Value(lib.LLVMBuildInsertValue(
            self, arr, val, idx, name.encode()))
    
    def extract_value(self, arr, idx, name):
        return Value(lib.LLVMBuildExtractValue(
            self, arr, idx, name.encode()))

    def gep(self, ptr, indices, name):
        """getelementptr instruction"""
        count, idx_array = util.to_c_array(indices)
        r = Value(lib.LLVMBuildGEP(
            self, ptr, idx_array, count, name.encode())) 
        return r
    
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

    library.LLVMBuildRetVoid.argtypes = [Builder]
    library.LLVMBuildRetVoid.restype = c_object_p

    library.LLVMDisposeBuilder.argtypes = [Builder]
    library.LLVMDisposeBuilder.restype = None

    library.LLVMBuildBr.argtypes = [Builder, BasicBlock]
    library.LLVMBuildBr.restype = c_object_p
                     
    library.LLVMBuildCondBr.argtypes = [Builder, Value, BasicBlock, BasicBlock]
    library.LLVMBuildCondBr.restype = c_object_p

    library.LLVMBuildNeg.argtypes = [Builder, Value, c_char_p]
    library.LLVMBuildNeg.restype = c_object_p

    library.LLVMBuildPhi.argtypes = [Builder, Type, c_char_p]
    library.LLVMBuildPhi.restype = c_object_p
    
    library.LLVMPositionBuilderAtEnd.argtypes = [Builder, BasicBlock]
    library.LLVMPositionBuilderAtEnd.restype = None

    library.LLVMBuildAlloca.argtypes = [Builder, Type, c_char_p]
    library.LLVMBuildAlloca.restype = c_object_p

    library.LLVMBuildArrayAlloca.argtypes = [Builder, Type, Value, c_char_p]
    library.LLVMBuildArrayAlloca.restype = c_object_p

    library.LLVMBuildStore.argtypes = [Builder, Value, Value]
    library.LLVMBuildStore.restype = c_object_p

    library.LLVMBuildLoad.argtypes = [Builder, Value, c_char_p]
    library.LLVMBuildLoad.restype = c_object_p

    library.LLVMBuildCall.argtypes = [Builder,
                                      Function,
                                      POINTER(c_object_p),
                                      c_uint,
                                      c_char_p]
    library.LLVMBuildCall.restype = c_object_p

    library.LLVMBuildInsertValue.argtypes = [Builder,
                                             Value,
                                             Value,
                                             c_uint,
                                             c_char_p]
    library.LLVMBuildInsertValue.restype = c_object_p

    library.LLVMBuildGEP.argtypes = [Builder, Value,
                                     POINTER(c_object_p),
                                     c_uint, c_char_p]
    library.LLVMBuildGEP.restype = c_object_p

    library.LLVMBuildExtractValue.argtypes = [Builder,
                                              Value,
                                              c_uint,
                                              c_char_p]
    library.LLVMBuildExtractValue.restype = c_object_p
    
register_library(lib)
