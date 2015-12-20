from .common import LLVMObject
from .common import c_object_p
from .common import get_library

from .value import Value
from .context import Context

from ctypes import c_char_p
from ctypes import c_uint

lib = get_library()


class Function(Value):
    """LLVM Function"""
    
    def __init__(self, value):
        Value.__init__(self, value)

    @property
    def next(self):
        f = lib.LLVMGetNextFunction(self)
        return f and Function(f)

    @property
    def prev(self):
        f = lib.LLVMGetPreviousFunction(self)
        return f and Function(f)

    @property
    def first(self):
        from .basic_block import BasicBlock
        
        b = lib.LLVMGetFirstBasicBlock(self)
        return b and BasicBlock(b)

    @property
    def last(self):
        from .basic_block import BasicBlock
        
        b = lib.LLVMGetLastBasicBlock(self)
        return b and BasicBlock(b)

    class __bb_iterator(object):
        def __init__(self, function, reverse=False):
            self.function = function
            self.reverse = reverse
            if self.reverse:
                self.bb = function.last
            else:
                self.bb = function.first

        def __iter__(self):
            return self

        def __next__(self):
            from .basic_block import BasicBlock
            
            if not isinstance(self.bb, BasicBlock):
                raise StopIteration("")
            result = self.bb
            if self.reverse:
                self.bb = self.bb.prev
            else:
                self.bb = self.bb.next
            return result

        def next(self):
            return self.__next__()

    def __iter__(self):
        return Function.__bb_iterator(self)

    def __reversed__(self):
        return Function.__bb_iterator(self, reverse=True)

    def __len__(self):
        return lib.LLVMCountBasicBlocks(self)

    def append_basic_block(self, name, context=None):
        from .basic_block import BasicBlock
        
        if context is None:
            return BasicBlock(lib.LLVMAppendBasicBlock(self, name.encode()))
        else:
            return BasicBlock(
                lib.LLVMAppendBasicBlockInContext(context, self, name.encode()))

    def get_param(self, idx):
        return Value(lib.LLVMGetParam(self, idx))

    def verify(self, action=None):
        return lib.LLVMVerifyFunction(self, action)

    
def register_library(library):
    from .basic_block import BasicBlock
    
    library.LLVMGetNextFunction.argtypes = [Function]
    library.LLVMGetNextFunction.restype = c_object_p

    library.LLVMGetPreviousFunction.argtypes = [Function]
    library.LLVMGetPreviousFunction.restype = c_object_p

    library.LLVMAppendBasicBlock.argtypes = [Function, c_char_p]
    library.LLVMAppendBasicBlock.restype = c_object_p

    library.LLVMAppendBasicBlockInContext.argtypes = [Context,
                                                      Function,
                                                      c_char_p]
    library.LLVMAppendBasicBlockInContext.restype = c_object_p

    library.LLVMCountBasicBlocks.argtypes = [Function]
    library.LLVMCountBasicBlocks.restype = c_uint

    library.LLVMGetParam.argtypes = [Function, c_uint]
    library.LLVMGetParam.restype = c_object_p
    
    library.LLVMGetFirstBasicBlock.argtypes = [Function]
    library.LLVMGetFirstBasicBlock.restype = c_object_p

    library.LLVMGetLastBasicBlock.argtypes = [Function]
    library.LLVMGetLastBasicBlock.restype = c_object_p

      
register_library(lib)
