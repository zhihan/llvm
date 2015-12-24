from .common import LLVMObject
from .common import c_object_p
from .common import get_library

from .type import Type
from . import util

import ctypes


lib = get_library()


class Value(LLVMObject):
    """Wrapper class for LLVM Value.

    Encloses CoreValueConstant and CoreValue classes."""
    def __init__(self, value):
        LLVMObject.__init__(self, value)

    @staticmethod
    def null(ty):
        """Obtain a constant value referring to the null instance of a type."""
        return Value(lib.LLVMConstNull(ty))

    def is_null(self):
        """Determine whether a value instance is null."""
        return lib.LLVMIsNull(self)

    @staticmethod
    def all_ones(ty):
        """Obtain a constant value consisting of all ones."""
        return Value(lib.LLVMConstAllOnes(ty))

    @staticmethod
    def null_ptr(ty):
        """Obtain a null pointer of a given type."""
        return Value(lib.LLVMConstPointerNull(ty))

    @staticmethod
    def undef(ty):
        """Obtain a constant value referring to an undefined value of a type."""
        return Value(lib.LLVMGetUndef(ty))

    @classmethod
    def const_int(cls, ty, val, sign_extend):
        """Obtain a constant value for an integer type.

        Args:
         - ty: a Type that is an integer type
         - val: the integer value of the constant
         - sign_extend: bool, whether to sign extend the value

        Returns:
        a Value object for the given type and value.
        """
        return Value(lib.LLVMConstInt(ty, val, sign_extend))

    def get_signext_value(self):
        """Get the sign extended value of the integer constant value."""
        return lib.LLVMConstIntGetSExtValue(self)

    def get_zeroext_value(self):
        """Get the zero extended value of the integer constant value."""
        return lib.LLVMConstIntGetZExtValue(self)

    def is_const_int(self):
        """Test whether the value is const int."""
        return bool(lib.LLVMIsAConstantInt(self))

    @staticmethod
    def const_real(ty, val):
        """Obtain a constant for a floating point value."""
        if isinstance(val, str):
            return Value(lib.LLVMConstRealOfString(ty, val.encode()))
        else:
            return Value(lib.LLVMConstReal(ty, val))

    def get_double_value(self):
        """Obtain the double value for a floating point constant."""
        precision_lost = ctypes.c_bool()
        res = lib.LLVMConstRealGetDouble(self, ctypes.byref(precision_lost))
        return (res, precision_lost)

    @staticmethod
    def const_array(ty, vals):
        """Create a ConstantArray from values."""
        count, val_array = util.to_c_array(vals)
        return Value(lib.LLVMConstArray(
            ty, val_array, count))

    def array_elements(self):
        """Get the elements of the constant array and return as a list."""
        ty = self.type
        n = ty.array_length()
        return [Value(lib.LLVMGetElementAsConstant(self, i))
                for i in range(n)]
    
         
    @property
    def name(self):
        """The string name of a value."""
        return lib.LLVMGetValueName(self).decode()

    @name.setter
    def name(self, n):
        """The string name of a value."""
        lib.LLVMSetValueName(self, n.encode())
 
    @property
    def type(self):
        """The type of the value."""
        return Type(lib.LLVMTypeOf(self))

    def is_constant(self):
        """Determine whether a value instance is constant."""
        return lib.LLVMIsConstant(self)

    def is_undef(self):
        """Determine whether a value instance is undefined."""
        return lib.LLVMIsUndef(self)

    def __str__(self):
        """Return a string representation of the value."""
        return lib.LLVMPrintValueToString(self).decode()

    def dump(self):
        """Dump a representation of a value to stderr."""
        lib.LLVMDumpValue(self)

    def replace_uses_with(self, new_val):
        """Replace all uses of a value with another one."""
        lib.LLVMReplaceAllUsesWith(self, new_val)

    @property
    def operands(self):
        """Obtain a list of the operands"""
        n = lib.LLVMGetNumOperands(self)
        return [Value(lib.LLVMGetOperand(self, i))
                for i in range(n)]

    def set_operand(self, i, v):
        """Set an operand at a specific index in a User value"""
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
        """First use of a value"""
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

    library.LLVMGetUndef.argtypes = [Type]
    library.LLVMGetUndef.restype = c_object_p

    library.LLVMConstAllOnes.argtypes = [Type]
    library.LLVMConstAllOnes.restype = c_object_p

    library.LLVMConstPointerNull.argtypes = [Type]
    library.LLVMConstPointerNull.restype = c_object_p
    
    library.LLVMConstInt.argtypes = [Type, ctypes.c_ulonglong, ctypes.c_bool]
    library.LLVMConstInt.restype = c_object_p

    library.LLVMConstIntGetSExtValue.argtypes = [Value]
    library.LLVMConstIntGetSExtValue.restype = ctypes.c_longlong

    library.LLVMConstIntGetZExtValue.argtypes = [Value]
    library.LLVMConstIntGetZExtValue.restype = ctypes.c_longlong
    
    library.LLVMGetValueName.argtypes = [Value]
    library.LLVMGetValueName.restype = ctypes.c_char_p

    library.LLVMSetValueName.argtypes = [Value, ctypes.c_char_p]
    library.LLVMSetValueName.restype = None

    library.LLVMConstReal.argtypes = [Type, ctypes.c_double]
    library.LLVMConstReal.restype = c_object_p

    library.LLVMConstRealOfString.argtypes = [Type, ctypes.c_char_p]
    library.LLVMConstRealOfString.restype = c_object_p

    library.LLVMConstRealGetDouble.argtypes = [Value,
                                               ctypes.POINTER(ctypes.c_bool)]
    library.LLVMConstRealGetDouble.restype = ctypes.c_double

    library.LLVMConstArray.argtypes = [Type,
                                       ctypes.POINTER(c_object_p),
                                       ctypes.c_uint]
    library.LLVMConstArray.restype = c_object_p

    library.LLVMGetElementAsConstant.argtypes = [Value, ctypes.c_uint]
    library.LLVMGetElementAsConstant.restype = c_object_p
    
    library.LLVMTypeOf.argtypes = [Value]
    library.LLVMTypeOf.restype = c_object_p

    library.LLVMIsConstant.argtypes = [Value]
    library.LLVMIsConstant.restype = bool
    
    library.LLVMIsUndef.argtypes = [Value]
    library.LLVMIsUndef.restype = bool

    library.LLVMPrintValueToString.argtypes = [Value]
    library.LLVMPrintValueToString.restype = ctypes.c_char_p

    library.LLVMDumpValue.argtypes = [Value]
    library.LLVMDumpValue.restype = None

    library.LLVMGetOperand.argtypes = [Value, ctypes.c_uint]
    library.LLVMGetOperand.restype = c_object_p

    library.LLVMSetOperand.argtypes = [Value,
                                       ctypes.c_uint,
                                       Value]
    library.LLVMSetOperand.restype = None

    library.LLVMGetNumOperands.argtypes = [Value]
    library.LLVMGetNumOperands.restype = ctypes.c_uint

    library.LLVMGetOperandUse.argtypes = [Value, ctypes.c_uint]
    library.LLVMGetOperandUse.restype = c_object_p

    library.LLVMGetFirstUse.argtypes = [Value]
    library.LLVMGetFirstUse.restype = c_object_p

    library.LLVMGetNextUse.argtypes = [Use]
    library.LLVMGetNextUse.restype = c_object_p

    library.LLVMGetUsedValue.argtypes = [Use]
    library.LLVMGetUsedValue.restype = c_object_p

    library.LLVMGetUser.argtypes = [Use]
    library.LLVMGetUser.restype = c_object_p

    library.LLVMIsAConstantInt.argtypes = [Value]
    library.LLVMIsAConstantInt.restype = c_object_p


register_library(lib)
