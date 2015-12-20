from .common import LLVMObject
from .common import c_object_p
from .common import get_library

from .type import Type
from . import util

from ctypes import POINTER
from ctypes import byref
from ctypes import c_bool
from ctypes import c_char_p
from ctypes import c_uint
from ctypes import c_ulonglong
from ctypes import c_longlong
from ctypes import c_size_t
from ctypes import c_int
from ctypes import c_double
from ctypes import cast
from ctypes import pointer

lib = get_library()

class Value(LLVMObject):
    
    """Wrapper class for LLVM Value"""
    def __init__(self, value):
        LLVMObject.__init__(self, value)

    @classmethod
    def null(cls, ty):
        return Value(lib.LLVMConstNull(ty))

    def is_null(self):
        return lib.LLVMIsNull(self)

    @staticmethod
    def all_ones(ty):
        return Value(lib.LLVMConstAllOnes(ty))

    @staticmethod
    def null_ptr(ty):
        return Value(lib.LLVMConstPointerNull(ty))

    @classmethod
    def const_int(cls, ty, val, sign_extend):
        return Value(lib.LLVMConstInt(ty, val, sign_extend))

    def get_signext_value(self):
        return lib.LLVMConstIntGetSExtValue(self)

    def get_zeroext_value(self):
        return lib.LLVMConstIntGetZExtValue(self)

    @classmethod
    def const_real(cls, ty, val):
        if isinstance(val, str):
            return Value(lib.LLVMConstRealOfString(ty, val.encode()))
        else:
            return Value(lib.LLVMConstReal(ty, val))

    def get_double_value(self):
        precision_lost = c_bool()
        res = lib.LLVMConstRealGetDouble(self, byref(precision_lost))
        return (res, precision_lost)

    @staticmethod
    def const_array(ty, vals, packed=False):
        count, val_array = util.to_c_array(vals)
        return Value(lib.LLVMConstArray(
            ty, val_array, count, packed))

    def array_elements(self):
        ty = self.type
        n = ty.array_length()
        return [Value(lib.LLVMGetElementAsConstant(self, i))
                for i in range(n)]
    
    @property
    def name(self):
        return lib.LLVMGetValueName(self).decode()

    @name.setter
    def name(self, n):
        lib.LLVMSetValueName(self, n.encode())
 
    @property
    def type(self):
        return Type(lib.LLVMTypeOf(self))

    def is_constant(self):
        return lib.LLVMIsConstant(self)

    def is_undef(self):
        return lib.LLVMIsUndef(self)

    def __str__(self):
        return lib.LLVMPrintValueToString(self).decode()

    def dump(self):
        lib.LLVMDumpValue(self)

    def replace_uses_with(self, new_val):
        lib.LLVMReplaceAllUsesWith(self, new_val)

    # Related to User
    @property
    def operands(self):
        n = lib.LLVMGetNumOperands(self)
        return [Value(lib.LLVMGetOperand(self, i))
                for i in range(n)]

    def set_operand(self, i, v):
        lib.LLVMSetOperand(self, i, v)

    @property
    def operand_uses(self):
        n = lib.LLVMGetNumOperands(self)
        return [Use(lib.LLVMGetOperandUse(self, i))
                for i in range(n)]

    class __use_iterator__(object):
        """An iterator that iterates through the uses"""
        def __init__(self, value):
            self.current = Use.first(value)

        def __iter__(self):
            return self

        def __next__(self):
            if not isinstance(self.current, Use):
                raise StopIteration("")
            result = self.current
            self.current = Use.next
            return result

        def next(self):
            return self.__next__()

    def uses_iter(self):
        return Value.__use_iterator__(self)
    



class Use(LLVMObject):
    """Wrapper for LLVMUseRef"""
    def __init__(self, ptr):
        LLVMObject.__init__(self, ptr)

    @staticmethod
    def first(val):
        return Use(lib.LLVMGetFirstUse(val))

    @property
    def next(self):
        u = lib.LLVMGetNextUse(self)
        result = Use(u) if u else None
        return result

    @property
    def used_value(self):
        return Value(lib.LLVMGetUsedValue(self))

    @property
    def user(self):
        return Value(lib.LLVMGetUser(self))

    
def register_library(library):    
    # Value declarations.
    library.LLVMConstNull.argtypes = [Type]
    library.LLVMConstNull.restype = c_object_p

    library.LLVMIsNull.argtypes = [Value]
    library.LLVMIsNull.restype = bool

    library.LLVMConstAllOnes.argtypes = [Type]
    library.LLVMConstAllOnes.restype = c_object_p

    library.LLVMConstPointerNull.argtypes = [Type]
    library.LLVMConstPointerNull.restype = c_object_p
    
    library.LLVMConstInt.argtypes = [Type, c_ulonglong, c_bool]
    library.LLVMConstInt.restype = c_object_p

    library.LLVMConstIntGetSExtValue.argtypes = [Value]
    library.LLVMConstIntGetSExtValue.restype = c_longlong

    library.LLVMConstIntGetZExtValue.argtypes = [Value]
    library.LLVMConstIntGetZExtValue.restype = c_longlong
    
    library.LLVMGetValueName.argtypes = [Value]
    library.LLVMGetValueName.restype = c_char_p

    library.LLVMSetValueName.argtypes = [Value, c_char_p]
    library.LLVMSetValueName.restype = None

    library.LLVMConstReal.argtypes = [Type, c_double]
    library.LLVMConstReal.restype = c_object_p

    library.LLVMConstRealOfString.argtypes = [Type, c_char_p]
    library.LLVMConstRealOfString.restype = c_object_p

    library.LLVMConstRealGetDouble.argtypes = [Value, POINTER(c_bool)]
    library.LLVMConstRealGetDouble.restype = c_double

    library.LLVMConstArray.argtypes = [Type, POINTER(c_object_p), c_uint, c_bool]
    library.LLVMConstArray.restype = c_object_p

    library.LLVMGetElementAsConstant.argtypes = [Value, c_uint]
    library.LLVMGetElementAsConstant.restype = c_object_p
    
    library.LLVMTypeOf.argtypes = [Value]
    library.LLVMTypeOf.restype = c_object_p

    library.LLVMIsConstant.argtypes = [Value]
    library.LLVMIsConstant.restype = c_bool
    
    library.LLVMIsUndef.argtypes = [Value]
    library.LLVMIsUndef.restype = c_bool

    library.LLVMPrintValueToString.argtypes = [Value]
    library.LLVMPrintValueToString.restype = c_char_p

    library.LLVMDumpValue.argtypes = [Value]
    library.LLVMDumpValue.restype = None

    library.LLVMGetOperand.argtypes = [Value, c_uint]
    library.LLVMGetOperand.restype = c_object_p

    library.LLVMSetOperand.argtypes = [Value, c_uint, Value]
    library.LLVMSetOperand.restype = None

    library.LLVMGetNumOperands.argtypes = [Value]
    library.LLVMGetNumOperands.restype = c_uint

    library.LLVMGetOperandUse.argtypes = [Value, c_uint]
    library.LLVMGetOperandUse.restype = c_object_p

    # Use
    library.LLVMGetFirstUse.argtypes = [Value]
    library.LLVMGetFirstUse.restype = c_object_p

    library.LLVMGetNextUse.argtypes = [Use]
    library.LLVMGetNextUse.restype = c_object_p

    library.LLVMGetUsedValue.argtypes = [Use]
    library.LLVMGetUsedValue.restype = c_object_p

    library.LLVMGetUser.argtypes = [Use]
    library.LLVMGetUser.restype = c_object_p


register_library(lib)
