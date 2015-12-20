from .common import LLVMObject
from .common import c_object_p
from .common import get_library

from .value import Value
from .function import Function

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


class BasicBlock(LLVMObject):
    def __init__(self, value):
        LLVMObject.__init__(self, value)

    @property
    def next(self):
        b = lib.LLVMGetNextBasicBlock(self)
        return b and BasicBlock(b)

    @property
    def prev(self):
        b = lib.LLVMGetPreviousBasicBlock(self)
        return b and BasicBlock(b)

    @property
    def first(self):
        i = lib.LLVMGetFirstInstruction(self)
        return i and Instruction(i)

    @property
    def last(self):
        i = lib.LLVMGetLastInstruction(self)
        return i and Instruction(i)

    def __as_value(self):
        return Value(lib.LLVMBasicBlockAsValue(self))

    @property
    def name(self):
        return self.__as_value().name

    def dump(self):
        lib.LLVMDumpValue(self.__as_value())

    class __inst_iterator(object):
        def __init__(self, bb, reverse=False):
            self.bb = bb
            self.reverse = reverse
            if self.reverse:
                self.inst = self.bb.last
            else:
                self.inst = self.bb.first

        def __iter__(self):
            return self

        def __next__(self):
            if not isinstance(self.inst, Instruction):
                raise StopIteration("")
            result = self.inst
            if self.reverse:
                self.inst = self.inst.prev
            else:
                self.inst = self.inst.next
            return result

        def next(self):
            return self.__next__()

    def __iter__(self):
        return BasicBlock.__inst_iterator(self)

    def __reversed__(self):
        return BasicBlock.__inst_iterator(self, reverse=True)

class Instruction(Value):

    def __init__(self, value):
        Value.__init__(self, value)

    @property
    def next(self):
        i = lib.LLVMGetNextInstruction(self)
        return i and Instruction(i)

    @property
    def prev(self):
        i = lib.LLVMGetPreviousInstruction(self)
        return i and Instruction(i)

    @property
    def opcode(self):
        from .core import OpCode
        
        return OpCode.from_value(lib.LLVMGetInstructionOpcode(self))

class PhiNode(Value):
    def __init__(self, ptr):
        Value.__init__(self, ptr)

    def add_incoming(self, vals, blocks):
        count = len(vals)
        val_array = (c_object_p * count)()
        block_array = (c_object_p * count)()
        for i in range(count):
            val_array[i] = vals[i].from_param()
            block_array[i] = blocks[i].from_param()
        lib.LLVMAddIncoming(self, val_array, block_array, count)

    def count_incoming(self):
        return lib.LLVMCountIncoming(self)

    def incoming_values(self):
        n = self.count_incoming()
        return [Value(lib.LLVMGetIncomingValue(self, i)) for i in range(n)]

    def incoming_blocks(self):
        n = self.count_incoming()
        return [BasicBlock(lib.LLVMGetIncomingBlock(self, i))
                for i in range(n)]

def register_library(library):
    library.LLVMAddIncoming.argtypes = [PhiNode,
                                        POINTER(c_object_p),
                                        POINTER(c_object_p),
                                        c_int]
    library.LLVMAddIncoming.restype = None

    library.LLVMCountIncoming.argtypes = [PhiNode]
    library.LLVMCountIncoming.restype = c_int

    library.LLVMGetIncomingValue.argtypes = [PhiNode, c_uint]
    library.LLVMGetIncomingValue.restype = c_object_p

    library.LLVMGetIncomingBlock.argtypes = [PhiNode, c_uint]
    library.LLVMGetIncomingBlock.restype = c_object_p

    library.LLVMGetFirstInstruction.argtypes = [BasicBlock]
    library.LLVMGetFirstInstruction.restype = c_object_p

    library.LLVMGetLastInstruction.argtypes = [BasicBlock]
    library.LLVMGetLastInstruction.restype = c_object_p

    library.LLVMBasicBlockAsValue.argtypes = [BasicBlock]
    library.LLVMBasicBlockAsValue.restype = c_object_p

    library.LLVMVerifyFunction.argtypes = [Function, c_int]
    library.LLVMVerifyFunction.restype = bool

    # Instruction Declarations.
    library.LLVMGetNextInstruction.argtypes = [Instruction]
    library.LLVMGetNextInstruction.restype = c_object_p

    library.LLVMGetPreviousInstruction.argtypes = [Instruction]
    library.LLVMGetPreviousInstruction.restype = c_object_p

    library.LLVMGetInstructionOpcode.argtypes = [Instruction]
    library.LLVMGetInstructionOpcode.restype = c_uint
    
    library.LLVMGetNextBasicBlock.argtypes = [BasicBlock]
    library.LLVMGetNextBasicBlock.restype = c_object_p

    library.LLVMGetPreviousBasicBlock.argtypes = [BasicBlock]
    library.LLVMGetPreviousBasicBlock.restype = c_object_p


register_library(lib)
