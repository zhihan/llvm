from ctypes import c_ulonglong
from ctypes import c_bool

from .common import LLVMObject
from .common import c_object_p
from .common import get_library

from .core import Type

lib = get_library()

class GenericValue(LLVMObject):
    def __init__(self, ptr):
        LLVMObject.__init__(self, ptr, ownable=True,
                            disposer=lib.LLVMDisposeGenericValue)

    @staticmethod
    def of_int(ty, n, signed):
        return GenericValue(lib.LLVMCreateGenericValueOfInt(ty, n, signed))

    def to_int(self, signed):
        return lib.LLVMGenericValueToInt(self, signed)
        
    

def register_library(library):
    library.LLVMDisposeGenericValue.argtypes = [GenericValue]
    library.LLVMDisposeGenericValue.restype = None

    library.LLVMCreateGenericValueOfInt.argtypes = [Type, c_ulonglong, c_bool]
    library.LLVMCreateGenericValueOfInt.restype = c_object_p

    library.LLVMGenericValueToInt.argtypes = [GenericValue, c_bool]
    library.LLVMGenericValueToInt.restype = c_ulonglong

    
register_library(lib)
