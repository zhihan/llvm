from .common import LLVMObject
from .common import c_object_p
from .common import get_library

from .context import Context
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


class Type(LLVMObject):
    """Represent a bype in LLVM."""
    def __init__(self, ty):
        LLVMObject.__init__(self, ty)

    @property
    def kind(self):
        from .core import TypeKind
        
        """Return the kind of the type"""
        return TypeKind.from_value(lib.LLVMGetTypeKind(self))

    def is_sized(self):
        return lib.LLVMTypeIsSized(self)
    
    @property
    def name(self):
        return lib.LLVMPrintTypeToString(self).decode()

    @classmethod
    def int8(cls, context=None):
        if context is not None:
            return Type(lib.LLVMInt8TypeInContext(context))
        else:
            return Type(lib.LLVMInt8Type())

    @classmethod
    def int1(cls, context=None):
        if context is not None:
            return Type(lib.LLVMInt1TypeInContext(context))
        else:
            return Type(lib.LLVMInt1Type())

    @classmethod
    def int16(cls, context=None):
        if context is not None:
            return Type(lib.LLVMInt16TypeInContext(context))
        else:
            return Type(lib.LLVMInt16Type())

    @classmethod
    def int32(cls, context=None):
        if context is not None:
            return Type(lib.LLVMInt32TypeInContext(context))
        else:
            return Type(lib.LLVMInt32Type())

    @classmethod
    def int64(cls, context=None):
        if context is not None:
            return Type(lib.LLVMInt64TypeInContext(context))
        else:
            return Type(lib.LLVMInt64Type())

    @classmethod
    def int(cls, num_bits, context=None):
        if context is not None:
            return Type(lib.LLVMIntTypeInContext(context, num_bits))
        else:
            return Type(lib.LLVMIntType(num_bits))
        
    @classmethod
    def half(cls, context=None):
        if context is not None:
            return Type(lib.LLVMHalfTypeInContext(context))
        else:
            return Type(lib.LLVMHalfType())

    @classmethod
    def float(cls, context=None):
        if context is not None:
            return Type(lib.LLVMFloatTypeInContext(context))
        else:
            return Type(lib.LLVMFloatType())
        
    @classmethod
    def double(cls, context=None):
        if context is not None:
            return Type(lib.LLVMDoubleTypeInContext(context))
        else:
            return Type(lib.LLVMDoubleType())


    @staticmethod
    def pointer(ty, address_space=0):
        return Type(lib.LLVMPointerType(ty, address_space))

    def pointer_address_space(self):
        return lib.LLVMGetPointerAddressSpace(self)

    @staticmethod
    def array(ty, count):
        return Type(lib.LLVMArrayType(ty, count))

    def array_length(self):
        return lib.LLVMGetArrayLength(self)

    def element_type(self):
        return Type(lib.LLVMGetElementType(self))

    @staticmethod
    def vector(ty, count):
        return Type(lib.LLVMVectorType(ty, count))

    def vector_size(self):
        return lib.LLVMGetVectorSize(self)

    @staticmethod
    def structure(types, packed, context=None):
        count, types_array = util.to_c_array(types)
        if context is None:
            return Type(lib.LLVMStructType(types_array, count, packed))
        else:
            return Type(lib.LLVMStructTypeInContext(
                context, types_array, count, package))

    def num_elements(self):
        return lib.LLVMCountStructElementTypes(self)

    def elements(self):
        elems = pointer(c_object_p())
        count = self.num_elements()
        lib.LLVMGetStructElementTypes(self, elems)
        return [Type(elems[i]) for i in range(count)]

    @staticmethod
    def create_named_structure(context, name):
        """Create a named (empty) structure"""
        return Type(lib.LLVMStructCreateNamed(context, name.encode()))

    def struct_name(self):
        return lib.LLVMGetStructName(self).decode()

    def set_body(self, types, packed):
        count, type_array = util.to_c_array(types)
        lib.LLVMStructSetBody(self, type_array, count, packed)

    def is_packed(self):
        return lib.LLVMIsPackedStruct(self)

    # Function type
    @classmethod
    def function(cls, ret, params, isVarArg):
        count, param_array = util.to_c_array(params)
        return Type(lib.LLVMFunctionType(
            ret, param_array, count, isVarArg))

    def is_function_vararg(self):
        return lib.LLVMIsFunctionVarArg(self)

    def return_type(self):
        return Type(lib.LLVMGetReturnType(self))

    def num_params(self):
        return lib.LLVMCountParamTypes(self)

    def param_types(self):
        dest = pointer(c_object_p())
        count = self.num_params()
        lib.LLVMGetParamTypes(self, dest)
        return [Type(dest[i]) for i in range(count)]

    # Special types
    @staticmethod
    def void(context=None):
        if context is None:
            return Type(lib.LLVMVoidType())
        else:
            return Type(lib.LLVMVoidTypeInContext(context))

    @staticmethod
    def label(context=None):
        if context is None:
            return Type(lib.LLVMLabelType())
        else:
            return Type(lib.LLVMLabelTypeInContext(context))
        
    def dump(self):
        lib.LLVMDumpType(self)

    @property
    def context(self):
        return Context(lib.LLVMGetTypeContext(self))


def register_library(library):
    # Types
    library.LLVMInt1TypeInContext.argtypes = [Context]
    library.LLVMInt1TypeInContext.restype = c_object_p

    library.LLVMInt8TypeInContext.argtypes = [Context]
    library.LLVMInt8TypeInContext.restype = c_object_p

    library.LLVMInt16TypeInContext.argtypes = [Context]
    library.LLVMInt16TypeInContext.restype = c_object_p

    library.LLVMInt32TypeInContext.argtypes = [Context]
    library.LLVMInt32TypeInContext.restype = c_object_p

    library.LLVMInt64TypeInContext.argtypes = [Context]
    library.LLVMInt64TypeInContext.restype = c_object_p

    library.LLVMIntTypeInContext.argtypes = [Context, c_uint]
    library.LLVMIntTypeInContext.restype = c_object_p

    library.LLVMHalfTypeInContext.argtypes = [Context]
    library.LLVMHalfTypeInContext.restype = c_object_p

    library.LLVMFloatTypeInContext.argtypes = [Context]
    library.LLVMFloatTypeInContext.restype = c_object_p

    library.LLVMDoubleTypeInContext.argtypes = [Context]
    library.LLVMDoubleTypeInContext.restype = c_object_p

    library.LLVMInt1Type.argtypes = []
    library.LLVMInt1Type.restype = c_object_p

    library.LLVMInt8Type.argtypes = []
    library.LLVMInt8Type.restype = c_object_p

    library.LLVMInt16Type.argtypes = []
    library.LLVMInt16Type.restype = c_object_p

    library.LLVMInt32Type.argtypes = []
    library.LLVMInt32Type.restype = c_object_p

    library.LLVMInt64Type.argtypes = []
    library.LLVMInt64Type.restype = c_object_p

    library.LLVMIntType.argtypes = [c_uint]
    library.LLVMIntType.restype = c_object_p

    library.LLVMHalfType.argtypes = []
    library.LLVMHalfType.restype = c_object_p

    library.LLVMFloatType.argtypes = []
    library.LLVMFloatType.restype = c_object_p

    library.LLVMDoubleType.argtypes = []
    library.LLVMDoubleType.restype = c_object_p

    library.LLVMPointerType.argtypes = [Type, c_uint]
    library.LLVMPointerType.restype = c_object_p

    library.LLVMGetPointerAddressSpace.argtypes = [Type]
    library.LLVMGetPointerAddressSpace.restype = c_uint

    library.LLVMArrayType.argtypes = [Type, c_uint]
    library.LLVMArrayType.restype = c_object_p

    library.LLVMGetElementType.argtypes = [Type]
    library.LLVMGetElementType.restype = c_object_p

    library.LLVMGetArrayLength.argtypes = [Type]
    library.LLVMGetArrayLength.restype = c_uint
    
    library.LLVMVectorType.argtypes = [Type, c_uint]
    library.LLVMVectorType.restype = c_object_p

    library.LLVMGetVectorSize.argtypes = [Type]
    library.LLVMGetVectorSize.restype = c_uint
    
    library.LLVMStructType.argtypes = [POINTER(c_object_p), c_uint, c_bool]
    library.LLVMStructType.restype = c_object_p
    
    library.LLVMStructTypeInContext.argtypes = [Context,
                                                POINTER(c_object_p),
                                                c_uint,
                                                c_bool]
    library.LLVMStructTypeInContext.restype = c_object_p

    library.LLVMCountStructElementTypes.argtypes = [Type]
    library.LLVMCountStructElementTypes.restype = c_uint

    library.LLVMGetStructElementTypes.argtypes = [Type,
                                                  POINTER(c_object_p)]
    library.LLVMGetStructElementTypes.restype = None

    library.LLVMStructCreateNamed.argtypes = [Context, c_char_p]
    library.LLVMStructCreateNamed.restype = c_object_p

    library.LLVMGetStructName.argtypes = [Type]
    library.LLVMGetStructName.restype = c_char_p

    library.LLVMStructSetBody.argtypes = [Type,
                                          POINTER(c_object_p),
                                          c_uint,
                                          c_bool]
    library.LLVMStructSetBody.restype = None

    library.LLVMIsPackedStruct.argtypes = [Type]
    library.LLVMIsPackedStruct.restype = c_bool

    library.LLVMVoidTypeInContext.argtypes = [Context]
    library.LLVMVoidTypeInContext.restype = c_object_p

    library.LLVMVoidType.argtypes = []
    library.LLVMVoidType.restype = c_object_p
    
    library.LLVMLabelTypeInContext.argtypes = [Context]
    library.LLVMLabelTypeInContext.restype = c_object_p

    library.LLVMLabelType.argtypes = []
    library.LLVMLabelType.restype = c_object_p
    
    library.LLVMPrintTypeToString.argtypes = [Type]
    library.LLVMPrintTypeToString.restype = c_char_p

    library.LLVMGetTypeKind.argtypes = [Type]
    library.LLVMGetTypeKind.restype = c_int

    library.LLVMTypeIsSized.argtypes = [Type]
    library.LLVMTypeIsSized.restype = c_bool

    library.LLVMDumpType.argtype = [Type]
    library.LLVMDumpType.restype = None

    library.LLVMGetTypeContext.argtype = [Type]
    library.LLVMGetTypeContext.restype = c_object_p

    library.LLVMFunctionType.argtype = [Type, POINTER(c_object_p), c_uint, c_bool]
    library.LLVMFunctionType.restype = c_object_p

    library.LLVMIsFunctionVarArg.argtype = [Type]
    library.LLVMIsFunctionVarArg.restype = c_bool

    library.LLVMGetReturnType.argtypes = [Type]
    library.LLVMGetReturnType.restype = c_object_p

    library.LLVMCountParamTypes.argtypes = [Type]
    library.LLVMCountParamTypes.restype = c_uint

    library.LLVMGetParamTypes.argtypes = [Type, POINTER(c_object_p)]
    library.LLVMGetParamTypes.restype = None


register_library(lib)
