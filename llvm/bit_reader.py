from .common import LLVMObject
from .common import c_object_p
from .common import get_library

from . import enumerations

from .core import MemoryBuffer
from .core import Module
from .core import Context

from ctypes import POINTER
from ctypes import byref
from ctypes import c_char_p
from ctypes import cast


__all__ = ['parse_bitcode']
lib = get_library()


def parse_bitcode(mem_buffer, context=None):
    """Input is .core.MemoryBuffer"""
    module = c_object_p()
    out = c_char_p(None)
    if context is None:
        result = lib.LLVMParseBitcode(mem_buffer, byref(module), byref(out))
    else:
        result = lib.LLVMParseBitcodeInContext(context,
                                               mem_buffer,
                                               byref(module),
                                               byref(out))
    if result:
        raise RuntimeError('LLVM Error: %s' % out.value)

    if context is None:
        context = Context.GetGlobalContext()
    m = Module(module, context=context)
    context.take_ownership(m)
    m.take_ownership(mem_buffer)
    return m

def register_library(library):
    library.LLVMParseBitcode.argtypes = [MemoryBuffer,
                                         POINTER(c_object_p),
                                         POINTER(c_char_p)]
    library.LLVMParseBitcode.restype = bool

    library.LLVMParseBitcodeInContext.argtypes = [Context,
                                                  MemoryBuffer,
                                                  POINTER(c_object_p),
                                                  POINTER(c_char_p)]
    library.LLVMParseBitcodeInContext.restype = bool

    
register_library(lib)
