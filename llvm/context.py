from .common import LLVMObject
from .common import c_object_p
from .common import get_library


lib = get_library()


class Context(LLVMObject):
    """The top-level container for all LLVM global data."""
    def __init__(self, context=None):
        if context is None:
            context = lib.LLVMContextCreate()
            LLVMObject.__init__(self, context, disposer=lib.LLVMContextDispose)
        else:
            LLVMObject.__init__(self, context)

    @classmethod
    def GetGlobalContext(cls):
        return Context(lib.LLVMGetGlobalContext())


def register_library(library):
    # Context declarations.
    library.LLVMContextCreate.argtypes = []
    library.LLVMContextCreate.restype = c_object_p

    library.LLVMContextDispose.argtypes = [Context]
    library.LLVMContextDispose.restype = None

    library.LLVMGetGlobalContext.argtypes = []
    library.LLVMGetGlobalContext.restype = c_object_p

register_library(lib)
