from .common import LLVMObject
from .common import c_object_p
from .common import get_library

from ctypes import POINTER
from ctypes import byref
from ctypes import c_char_p
from ctypes import c_size_t


lib = get_library()


class MemoryBuffer(LLVMObject):
    """Represents an opaque memory buffer."""
    def __init__(self, memory):
        LLVMObject.__init__(self, memory, disposer=lib.LLVMDisposeMemoryBuffer)

    @classmethod
    def fromFile(cls, filename):
        """Create a new memory buffer.

        Currently, we support creating from the contents of a file at the
        specified filename.
        """
        if filename is None:
            raise Exception("filename argument must be defined")

        memory = c_object_p()
        out = c_char_p(None)

        result = lib.LLVMCreateMemoryBufferWithContentsOfFile(
            filename.encode(), byref(memory), byref(out))

        if result:
            raise Exception("Could not create memory buffer: %s" % out.value)
        return MemoryBuffer(memory)

    @classmethod
    def from_string(cls, s):
        memory = lib.LLVMCreateMemoryBufferWithMemoryRangeCopy(
            s.encode(), len(s), b'inputBuffer')
        return MemoryBuffer(memory)


    def __str__(self):
        return lib.LLVMGetBufferStart(self).decode()

    def __len__(self):
        return lib.LLVMGetBufferSize(self)

def register_library(library):
    # Memory buffer declarations
    library.LLVMCreateMemoryBufferWithContentsOfFile.argtypes = [c_char_p,
            POINTER(c_object_p), POINTER(c_char_p)]
    library.LLVMCreateMemoryBufferWithContentsOfFile.restype = bool

    library.LLVMGetBufferSize.argtypes = [MemoryBuffer]

    library.LLVMGetBufferStart.argtypes = [MemoryBuffer]
    library.LLVMGetBufferStart.restype = c_char_p

    library.LLVMCreateMemoryBufferWithMemoryRangeCopy.argtypes = [c_char_p,
                                                                  c_size_t,
                                                                  c_char_p]
    library.LLVMCreateMemoryBufferWithMemoryRangeCopy.restype = c_object_p

    library.LLVMDisposeMemoryBuffer.argtypes = [MemoryBuffer]

register_library(lib)
