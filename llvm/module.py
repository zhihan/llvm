from .common import LLVMObject
from .common import c_object_p
from .common import get_library

from .context import Context
from .type import Type
    
from ctypes import c_char_p
from ctypes import POINTER


lib = get_library()


class Module(LLVMObject):
    
    """Represents the top-level structure of an llvm program in an opaque object."""

    def __init__(self, module, name=None, context=None):
        LLVMObject.__init__(self, module, disposer=lib.LLVMDisposeModule)

    @classmethod
    def CreateWithName(cls, module_id, context=None):
        if not context:
            m = Module(lib.LLVMModuleCreateWithName(module_id.encode()))
            Context.GetGlobalContext().take_ownership(m)
        else:
            m = Module(lib.LLVMModuleCreateWithNameInContext(
                module_id.encode(),
                context))
            context.take_ownership(m)
        return m

    @property
    def context(self):
        return Context(lib.LLVMGetModuleContext(self))

    @property
    def datalayout(self):
        return lib.LLVMGetDataLayout(self).decode()

    @datalayout.setter
    def datalayout(self, new_data_layout):
        """new_data_layout is a string."""
        lib.LLVMSetDataLayout(self, new_data_layout.encode())

    @property
    def target(self):
        return lib.LLVMGetTarget(self).decode()

    @target.setter
    def target(self, new_target):
        """new_target is a string."""
        lib.LLVMSetTarget(self, new_target.encode())

    def dump(self):
        lib.LLVMDumpModule(self)

    def __str__(self):
        return lib.LLVMPrintModuleToString(self).decode()

    class __function_iterator(object):
        def __init__(self, module, reverse=False):
            self.module = module
            self.reverse = reverse
            if self.reverse:
                self.function = self.module.last
            else:
                self.function = self.module.first

        def __iter__(self):
            return self

        def __next__(self):
            from .function import Function

            if not isinstance(self.function, Function):
                raise StopIteration("")
            result = self.function
            if self.reverse:
                self.function = self.function.prev
            else:
                self.function = self.function.next
            return result

        def next(self):
            return self.__next__()
        
    def __iter__(self):
        return Module.__function_iterator(self)

    def __reversed__(self):
        return Module.__function_iterator(self, reverse=True)

    @property
    def first(self):
        from .function import Function
        return Function(lib.LLVMGetFirstFunction(self))

    @property
    def last(self):
        from .function import Function
        return Function(lib.LLVMGetLastFunction(self))

    def print_module_to_file(self, filename):
        out = c_char_p(None)
        # Result is inverted so 0 means everything was ok.
        result = lib.LLVMPrintModuleToFile(
            self, filename.encode(), byref(out))
        if result:
            raise RuntimeError("LLVM Error: %s" % out.value)

    def add_function(self, name, fn_ty):
        from .function import Function

        return Function(lib.LLVMAddFunction(
            self, name.encode(), fn_ty))

    def get_function(self, name):
        from .function import Function

        return Function(lib.LLVMGetNamedFunction(
            self, name.encode()))

    def get_type(self, name):
        from .type import Type
        
        return Type(lib.LLVMGetTypeByName(
            self, name.encode()))


def register_library(library):
    # Module declarations
    library.LLVMModuleCreateWithName.argtypes = [c_char_p]
    library.LLVMModuleCreateWithName.restype = c_object_p

    library.LLVMModuleCreateWithNameInContext.argtypes = [c_char_p,
                                                          Context]
    library.LLVMModuleCreateWithNameInContext.restype = c_object_p

    library.LLVMGetModuleContext.argtypes = [Module]
    library.LLVMGetModuleContext.restype = c_object_p

    library.LLVMDisposeModule.argtypes = [Module]
    library.LLVMDisposeModule.restype = None

    library.LLVMGetDataLayout.argtypes = [Module]
    library.LLVMGetDataLayout.restype = c_char_p

    library.LLVMSetDataLayout.argtypes = [Module, c_char_p]
    library.LLVMSetDataLayout.restype = None

    library.LLVMGetTarget.argtypes = [Module]
    library.LLVMGetTarget.restype = c_char_p

    library.LLVMSetTarget.argtypes = [Module, c_char_p]
    library.LLVMSetTarget.restype = None

    library.LLVMDumpModule.argtypes = [Module]
    library.LLVMDumpModule.restype = None

    library.LLVMPrintModuleToString.argtypes = [Module]
    library.LLVMPrintModuleToString.restype = c_char_p
    
    library.LLVMPrintModuleToFile.argtypes = [Module, c_char_p,
                                              POINTER(c_char_p)]
    library.LLVMPrintModuleToFile.restype = bool

    library.LLVMGetTypeByName.argtypes = [Module, c_char_p]
    library.LLVMGetTypeByName.restype = c_object_p

    library.LLVMAddFunction.argtypes = [Module, c_char_p, Type]
    library.LLVMAddFunction.restype = c_object_p

    library.LLVMGetNamedFunction.argtypes = [Module, c_char_p]
    library.LLVMGetNamedFunction.restype = c_object_p

    library.LLVMGetFirstFunction.argtypes = [Module]
    library.LLVMGetFirstFunction.restype = c_object_p

    library.LLVMGetLastFunction.argtypes = [Module]
    library.LLVMGetLastFunction.restype = c_object_p


register_library(lib)
