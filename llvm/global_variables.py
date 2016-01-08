"""Python bindings for GlobalVariables."""
from .common import LLVMObject
from .common import c_object_p
"""GlobalVariable bindings for LLVM."""
from .common import get_library

from .core import Context
from .core import Module
from .core import Type
from .core import Value

from ctypes import c_char_p
from ctypes import c_bool

__all__ = ['Global', 'GlobalIterator']
lib = get_library()

class Global(Value):
    """Wrapper of LLVM Global values"""
    def __init__(self, obj):
        LLVMObject.__init__(self, obj)

    @staticmethod
    def add(module, ty, name):
        """Add a named global to the module"""
        return Global(lib.LLVMAddGlobal(module, ty, name.encode()))

    @staticmethod
    def get(module, name):
        """Get the named global of the module"""
        return Global(lib.LLVMGetNamedGlobal(module, name.encode()))

    @property
    def initializer(self):
        """Get the initializer"""
        return Value(lib.LLVMGetInitializer(self))

    @initializer.setter
    def initializer(self, value):
        """Set initializer"""
        lib.LLVMSetInitializer(self, value)


    def set_const(self, tf):
        """Set the global to be constant"""
        lib.LLVMSetGlobalConstant(self, tf)

    def is_const(self):
        """Whether the global is constant"""
        return lib.LLVMIsGlobalConstant(self)

    @property
    def prev(self):
        """Get previous global"""
        p = lib.LLVMGetPreviousGlobal(self)
        return p and Global(p)

    @property
    def next(self):
        """Get next global"""
        n = lib.LLVMGetNextGlobal(self)
        return n and Global(n)

    def delete(self):
        """Delete the global from the module"""
        lib.LLVMDeleteGlobal(self)

    @staticmethod 
    def add_alias(module, ty, val, name):
        """Add an alias (global pointer) to an existing value"""
        return Value(lib.LLVMAddAlias(module, ty, val, name.encode()))

    
class GlobalIterator(object):
    """An iterator that iterates through globals in a module"""
    def __init__(self, module, reverse=False):
        if not isinstance(module, Module):
            raise ValueError("A Module object is required")
        self.reverse = reverse
        if not reverse:
            self.current = Global(lib.LLVMGetFirstGlobal(module))
        else:
            self.current = Global(lib.LLVMGetLastGlobal(module))

    def __iter__(self):
        return self

    def __next__(self):
        if not isinstance(self.current, Global):
            raise StopIteration("")
        result = self.current
        if not self.reverse:
            self.current = self.current.next
        else:
            self.current = self.current.prev
        return result

    def next(self):
        return self.__next__()


def register_library(library):
    library.LLVMAddGlobal.argtypes = [Module, Type, c_char_p]
    library.LLVMAddGlobal.restype = c_object_p

    library.LLVMGetNamedGlobal.argtypes = [Module, c_char_p]
    library.LLVMGetNamedGlobal.restype = c_object_p

    library.LLVMSetInitializer.argtypes = [Value, Value]
    library.LLVMSetInitializer.restype = None

    library.LLVMGetInitializer.argtypes = [Value]
    library.LLVMGetInitializer.restype = c_object_p

    library.LLVMSetGlobalConstant.argtypes = [Value, c_bool]
    library.LLVMSetGlobalConstant.restype = None

    library.LLVMIsGlobalConstant.argtypes = [Value]
    library.LLVMIsGlobalConstant.restype = bool

    library.LLVMGetFirstGlobal.argtypes = [Module]
    library.LLVMGetFirstGlobal.restype = c_object_p

    library.LLVMGetLastGlobal.argtypes = [Module]
    library.LLVMGetLastGlobal.restype = c_object_p
    
    library.LLVMGetNextGlobal.argtypes = [Global]
    library.LLVMGetNextGlobal.restype = c_object_p

    library.LLVMGetPreviousGlobal.argtypes = [Global]
    library.LLVMGetPreviousGlobal.restype = c_object_p

    library.LLVMDeleteGlobal.argtypes = [Global]
    library.LLVMDeleteGlobal.restype = None

    library.LLVMAddAlias.argtypes = [Module,
                                     Type,
                                     Value,
                                     c_char_p]
    library.LLVMAddAlias.restype = c_object_p
        
register_library(lib)
