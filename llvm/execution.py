from ctypes import c_ulonglong
from ctypes import c_bool
from ctypes import byref
from ctypes import c_char_p
from ctypes import c_uint
from ctypes import POINTER

from .common import LLVMObject
from .common import c_object_p
from .common import get_library

from .core import Type
from .core import Module
from .core import Value

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
        
class ExecutionEngine(LLVMObject):
    def __init__(self, ptr):
        LLVMObject.__init__(self, ptr, ownable=True,
                            disposer=lib.LLVMDisposeExecutionEngine)
    @staticmethod
    def create_interpreter(module):
        ee = c_object_p()
        out = c_char_p(None)
        result = lib.LLVMCreateInterpreterForModule(byref(ee), module, byref(out))
        if result:
            raise Exception('Error in creating interpreter: %s' % out.value)
        return ExecutionEngine(ee)

    def run_function(self, fn, args):
        count = len(args)
        arg_array = (c_object_p * count)()
        for i in xrange(count):
            arg_array[i] = args[i].from_param()
        return GenericValue(lib.LLVMRunFunction(self, fn, count, arg_array))

def register_library(library):
    library.LLVMDisposeGenericValue.argtypes = [GenericValue]
    library.LLVMDisposeGenericValue.restype = None

    library.LLVMCreateGenericValueOfInt.argtypes = [Type, c_ulonglong, c_bool]
    library.LLVMCreateGenericValueOfInt.restype = c_object_p

    library.LLVMGenericValueToInt.argtypes = [GenericValue, c_bool]
    library.LLVMGenericValueToInt.restype = c_ulonglong

    library.LLVMRunFunction.argtypes = [ExecutionEngine, Value, c_uint, POINTER(c_object_p)]
    library.LLVMRunFunction.restype = c_object_p
        
register_library(lib)
