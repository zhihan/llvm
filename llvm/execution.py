from ctypes import c_ulonglong
from ctypes import c_bool
from ctypes import byref
from ctypes import c_char_p
from ctypes import c_uint
from ctypes import POINTER
from ctypes import c_double

from .common import LLVMObject
from .common import c_object_p
from .common import get_library

from .core import Type
from .core import Module
from .core import Value

lib = get_library()

class GenericValue(LLVMObject):
    """Wrapper of LLVM generic values."""
    def __init__(self, ptr):
        LLVMObject.__init__(self, ptr, ownable=True,
                            disposer=lib.LLVMDisposeGenericValue)

    @staticmethod
    def of_int(ty, n, signed):
        """Create a generic value from an integer."""
        return GenericValue(lib.LLVMCreateGenericValueOfInt(ty, n, signed))

    def to_int(self, signed):
        """Return the int stored in the generic value."""
        return lib.LLVMGenericValueToInt(self, signed)

    @staticmethod
    def of_float(ty, val):
        return GenericValue(lib.LLVMCreateGenericValueOfFloat(ty, val))

    def to_float(self, ty):
        return lib.LLVMGenericValueToFloat(ty, self)
    
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

    @staticmethod
    def create_execution_engine(module):
        ee = c_object_p()
        out = c_char_p()
        result = lib.LLVMCreateExecutionEngineForModule(byref(ee), module, byref(out))
        if result:
            raise Exception('Error in creating exeuction engine: %s' % out.value)
        return ExecutionEngine(ee)

    @staticmethod
    def create_jit(module):
        ee = c_object_p()
        out = c_char_p()
        result = lib.LLVMCreateJITCompilerForModule(byref(ee), module, 0, byref(out))
        if result:
            raise Exception('Error in creating exeuction engine: %s' % out.value)
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

    library.LLVMCreateGenericValueOfFloat.argtypes = [Type, c_double]
    library.LLVMCreateGenericValueOfFloat.restype = c_object_p

    library.LLVMGenericValueToFloat.argtypes = [Type, GenericValue]
    library.LLVMGenericValueToFloat.restype = c_double

    library.LLVMCreateExecutionEngineForModule.argtypes = [POINTER(c_object_p),
                                                           Module,
                                                           POINTER(c_char_p)]
    library.LLVMCreateExecutionEngineForModule.restype = c_object_p
                                                           
    library.LLVMCreateInterpreterForModule.argtypes = [POINTER(c_object_p),
                                                       Module,
                                                       POINTER(c_char_p)]
    library.LLVMCreateInterpreterForModule.restype = c_object_p
 
    library.LLVMRunFunction.argtypes = [ExecutionEngine, Value, c_uint, POINTER(c_object_p)]
    library.LLVMRunFunction.restype = c_object_p
        
register_library(lib)
