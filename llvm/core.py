#===- core.py - Python LLVM Bindings -------------------------*- python -*--===#
#
#                     The LLVM Compiler Infrastructure
#
# This file is distributed under the University of Illinois Open Source
# License. See LICENSE.TXT for details.
#
#===------------------------------------------------------------------------===#

from .common import LLVMObject
from .common import c_object_p
from .common import get_library

from . import enumerations

from ctypes import POINTER
from ctypes import byref
from ctypes import c_bool
from ctypes import c_char_p
from ctypes import c_uint
from ctypes import c_ulonglong
from ctypes import c_size_t
from ctypes import c_int
from ctypes import c_double
from ctypes import cast

__all__ = [
    "lib",
    "Enums",
    "OpCode",
    "MemoryBuffer",
    "Module",
    "Value",
    "Function",
    "BasicBlock",
    "Instruction",
    "Context",
    "PassRegistry",
    "Type",
    "VerifierFailureActionTy",
    "shutdown_llvm",
]

lib = get_library()
Enums = []

class LLVMEnumeration(object):
    """Represents an individual LLVM enumeration."""

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return '%s.%s' % (self.__class__.__name__,
                          self.name)

    @classmethod
    def from_value(cls, value):
        """Obtain an enumeration instance from a numeric value."""
        result = cls._value_map.get(value, None)

        if result is None:
            raise ValueError('Unknown %s: %d' % (cls.__name__,
                                                 value))

        return result

    @classmethod
    def register(cls, name, value):
        """Registers a new enumeration.

        This is called by this module for each enumeration defined in
        enumerations. You should not need to call this outside this module.
        """
        if value in cls._value_map:
            raise ValueError('%s value already registered: %d' % (cls.__name__,
                                                                  value))
        enum = cls(name, value)
        cls._value_map[value] = enum
        setattr(cls, name, enum)

class Attribute(LLVMEnumeration):
    """Represents an individual Attribute enumeration."""

    _value_map = {}

    def __init__(self, name, value):
        super(Attribute, self).__init__(name, value)

class OpCode(LLVMEnumeration):
    """Represents an individual OpCode enumeration."""

    _value_map = {}

    def __init__(self, name, value):
        super(OpCode, self).__init__(name, value)

class TypeKind(LLVMEnumeration):
    """Represents an individual TypeKind enumeration."""

    _value_map = {}

    def __init__(self, name, value):
        super(TypeKind, self).__init__(name, value)

class Linkage(LLVMEnumeration):
    """Represents an individual Linkage enumeration."""

    _value_map = {}

    def __init__(self, name, value):
        super(Linkage, self).__init__(name, value)

class Visibility(LLVMEnumeration):
    """Represents an individual visibility enumeration."""

    _value_map = {}

    def __init__(self, name, value):
        super(Visibility, self).__init__(name, value)

class CallConv(LLVMEnumeration):
    """Represents an individual calling convention enumeration."""

    _value_map = {}

    def __init__(self, name, value):
        super(CallConv, self).__init__(name, value)

class IntPredicate(LLVMEnumeration):
    """Represents an individual IntPredicate enumeration."""

    _value_map = {}

    def __init__(self, name, value):
        super(IntPredicate, self).__init__(name, value)

class RealPredicate(LLVMEnumeration):
    """Represents an individual RealPredicate enumeration."""

    _value_map = {}

    def __init__(self, name, value):
        super(RealPredicate, self).__init__(name, value)

class LandingPadClauseTy(LLVMEnumeration):
    """Represents an individual LandingPadClauseTy enumeration."""

    _value_map = {}

    def __init__(self, name, value):
        super(LandingPadClauseTy, self).__init__(name, value)

class VerifierFailureActionTy(LLVMEnumeration):
    _value_map = {}

    def __init__(self, name, value):
        super(VerifierFailureActionTy, self).__init__(name, value)

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

        result = lib.LLVMCreateMemoryBufferWithContentsOfFile(filename,
                byref(memory), byref(out))

        if result:
            raise Exception("Could not create memory buffer: %s" % out.value)
        return MemoryBuffer(memory)

    @classmethod
    def fromString(cls, s):
        memory = lib.LLVMCreateMemoryBufferWithMemoryRangeCopy(
            s, len(s), "inputBuffer")
        return MemoryBuffer(memory)
        
        
    def __str__(self):
        return lib.LLVMGetBufferStart(self)
        
    def __len__(self):
        return lib.LLVMGetBufferSize(self)

class Type(LLVMObject):
    """Represent a bype in LLVM."""
    def __init__(self, ty):
        LLVMObject.__init__(self, ty)

    @property
    def name(self):
        return lib.LLVMPrintTypeToString(self)

    @classmethod
    def int8(cls, context=None):
        if context is not None:
            return Type(lib.LLVMInt8TypeInContext(context))
        else:
            return Type(lib.LLVMInt8Type())

    @classmethod
    def int1(cls, context=None):
        if context is not None:
            return Type(lib.LLVMInt1TypeInContext(context))
        else:
            return Type(lib.LLVMInt1Type())

    @classmethod
    def double(cls, context=None):
        if context is not None:
            return Type(lib.LLVMDoubleTypeInContext(context))
        else:
            return Type(lib.LLVMDoubleType())

    @classmethod
    def float(cls, context=None):
        if context is not None:
            return Type(lib.LLVMFloatTypeInContext(context))
        else:
            return Type(lib.LLVMFloatType())
        
    @classmethod
    def function(cls, ret, params, isVarArg):
        count = len(params)
        param_array = (c_object_p * count) ()
        for i in xrange(count):
            param_array[i] = params[i].from_param()
        return Type(lib.LLVMFunctionType(
            ret, param_array, count, isVarArg))


    def dump(self):
        lib.LLVMDumpType(self)

    def get_context(self):
        return Context(lib.LLVMGetTypeContext(self))

class Value(LLVMObject):

    def __init__(self, value):
        LLVMObject.__init__(self, value)

    @classmethod
    def null(self, ty):
        return Value(lib.LLVMConstNull(ty))

    def is_null(self):
        return lib.LLVMIsNull(self)

    @classmethod
    def const_int(self, ty, val, sign_extend):
        return Value(lib.LLVMConstInt(ty, val, sign_extend))

    def get_signext_value(self):
        return lib.LLVMConstIntGetSExtValue(self)

    @classmethod
    def const_real(self, ty, val):
        return Value(lib.LLVMConstReal(ty, val))

    def get_double_value(self):
        precision_lost = c_bool()
        res = lib.LLVMConstRealGetDouble(self, byref(precision_lost))
        return (res, precision_lost)
        
    @property
    def name(self):
        return lib.LLVMGetValueName(self)

    @property
    def type(self):
        return Type(lib.LLVMTypeOf(self))

    def __str__(self):
        return lib.LLVMPrintValueToString(self)

    def dump(self):
        lib.LLVMDumpValue(self)

    def get_operand(self, i):
        return Value(lib.LLVMGetOperand(self, i))

    def set_operand(self, i, v):
        return lib.LLVMSetOperand(self, i, v)

    def __len__(self):
        return lib.LLVMGetNumOperands(self)

class Module(LLVMObject):
    """Represents the top-level structure of an llvm program in an opaque object."""

    def __init__(self, module, name=None, context=None):
        LLVMObject.__init__(self, module, disposer=lib.LLVMDisposeModule)

    @classmethod
    def CreateWithName(cls, module_id):
        m = Module(lib.LLVMModuleCreateWithName(module_id))
        Context.GetGlobalContext().take_ownership(m)
        return m

    @property
    def context(self):
        return Context(lib.LLVMGetModuleContext(self))

    @property
    def datalayout(self):
        return lib.LLVMGetDataLayout(self)

    @datalayout.setter
    def datalayout(self, new_data_layout):
        """new_data_layout is a string."""
        lib.LLVMSetDataLayout(self, new_data_layout)

    @property
    def target(self):
        return lib.LLVMGetTarget(self)

    @target.setter
    def target(self, new_target):
        """new_target is a string."""
        lib.LLVMSetTarget(self, new_target)

    def dump(self):
        lib.LLVMDumpModule(self)

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

        def next(self):
            if not isinstance(self.function, Function):
                raise StopIteration("")
            result = self.function
            if self.reverse:
                self.function = self.function.prev
            else:
                self.function = self.function.next
            return result

    def __iter__(self):
        return Module.__function_iterator(self)

    def __reversed__(self):
        return Module.__function_iterator(self, reverse=True)

    @property
    def first(self):
        return Function(lib.LLVMGetFirstFunction(self))

    @property
    def last(self):
        return Function(lib.LLVMGetLastFunction(self))

    def print_module_to_file(self, filename):
        out = c_char_p(None)
        # Result is inverted so 0 means everything was ok.
        result = lib.LLVMPrintModuleToFile(self, filename, byref(out))
        if result:
            raise RuntimeError("LLVM Error: %s" % out.value)

    def add_function(self, name, fn_ty):
        return Function(lib.LLVMAddFunction(self, name, fn_ty))

    def get_function(self, name):
        return Function(lib.LLVMGetNamedFunction(self, name))

    def get_type(self, name):
        return Type(lib.LLVMGetTypeByName(self, name))
        

class Function(Value):

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
        b = lib.LLVMGetFirstBasicBlock(self)
        return b and BasicBlock(b)

    @property
    def last(self):
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

        def next(self):
            if not isinstance(self.bb, BasicBlock):
                raise StopIteration("")
            result = self.bb
            if self.reverse:
                self.bb = self.bb.prev
            else:
                self.bb = self.bb.next
            return result

    def __iter__(self):
        return Function.__bb_iterator(self)

    def __reversed__(self):
        return Function.__bb_iterator(self, reverse=True)

    def __len__(self):
        return lib.LLVMCountBasicBlocks(self)

    def append_basic_block(self, name, context=None):
        if context is None:
            return BasicBlock(lib.LLVMAppendBasicBlock(self, name))
        else:
            return BasicBlock(
                lib.LLVMAppendBasicBlockInContext(context, self, name))

    def get_param(self, idx):
        return Value(lib.LLVMGetParam(self, idx))

    def verify(self, action=None):
        return lib.LLVMVerifyFunction(self, action)


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
        return lib.LLVMGetValueName(self.__as_value())

    def dump(self):
        lib.LLVMDumpValue(self.__as_value())

    def get_operand(self, i):
        return Value(lib.LLVMGetOperand(self.__as_value(),
                                        i))

    def set_operand(self, i, v):
        return lib.LLVMSetOperand(self.__as_value(),
                                  i, v)

    def __len__(self):
        return lib.LLVMGetNumOperands(self.__as_value())

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

        def next(self):
            if not isinstance(self.inst, Instruction):
                raise StopIteration("")
            result = self.inst
            if self.reverse:
                self.inst = self.inst.prev
            else:
                self.inst = self.inst.next
            return result

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
        return OpCode.from_value(lib.LLVMGetInstructionOpcode(self))

class Context(LLVMObject):

    def __init__(self, context=None):
        if context is None:
            context = lib.LLVMContextCreate()
            LLVMObject.__init__(self, context, disposer=lib.LLVMContextDispose)
        else:
            LLVMObject.__init__(self, context)

    @classmethod
    def GetGlobalContext(cls):
        return Context(lib.LLVMGetGlobalContext())

class PassRegistry(LLVMObject):
    """Represents an opaque pass registry object."""

    def __init__(self):
        LLVMObject.__init__(self,
                            lib.LLVMGetGlobalPassRegistry())

def register_library(library):
    # Initialization/Shutdown declarations.
    library.LLVMInitializeCore.argtypes = [PassRegistry]
    library.LLVMInitializeCore.restype = None

    library.LLVMInitializeTransformUtils.argtypes = [PassRegistry]
    library.LLVMInitializeTransformUtils.restype = None

    library.LLVMInitializeScalarOpts.argtypes = [PassRegistry]
    library.LLVMInitializeScalarOpts.restype = None

    library.LLVMInitializeObjCARCOpts.argtypes = [PassRegistry]
    library.LLVMInitializeObjCARCOpts.restype = None

    library.LLVMInitializeVectorization.argtypes = [PassRegistry]
    library.LLVMInitializeVectorization.restype = None

    library.LLVMInitializeInstCombine.argtypes = [PassRegistry]
    library.LLVMInitializeInstCombine.restype = None

    library.LLVMInitializeIPO.argtypes = [PassRegistry]
    library.LLVMInitializeIPO.restype = None

    library.LLVMInitializeInstrumentation.argtypes = [PassRegistry]
    library.LLVMInitializeInstrumentation.restype = None

    library.LLVMInitializeAnalysis.argtypes = [PassRegistry]
    library.LLVMInitializeAnalysis.restype = None

    library.LLVMInitializeIPA.argtypes = [PassRegistry]
    library.LLVMInitializeIPA.restype = None

    library.LLVMInitializeCodeGen.argtypes = [PassRegistry]
    library.LLVMInitializeCodeGen.restype = None

    library.LLVMInitializeTarget.argtypes = [PassRegistry]
    library.LLVMInitializeTarget.restype = None

    library.LLVMShutdown.argtypes = []
    library.LLVMShutdown.restype = None

    # Types
    library.LLVMInt1TypeInContext.argtypes = [Context]
    library.LLVMInt1TypeInContext.restype = c_object_p
    library.LLVMInt8TypeInContext.argtypes = [Context]
    library.LLVMInt8TypeInContext.restype = c_object_p
    library.LLVMDoubleTypeInContext.argtypes = [Context]
    library.LLVMDoubleTypeInContext.restype = c_object_p
    library.LLVMFloatTypeInContext.argtypes = [Context]
    library.LLVMFloatTypeInContext.restype = c_object_p

    
    library.LLVMInt1Type.argtypes = []
    library.LLVMInt1Type.restype = c_object_p
    library.LLVMInt8Type.argtypes = []
    library.LLVMInt8Type.restype = c_object_p
    library.LLVMDoubleType.argtypes = []
    library.LLVMDoubleType.restype = c_object_p
    library.LLVMFloatType.argtypes = []
    library.LLVMFloatType.restype = c_object_p

    library.LLVMPrintTypeToString.argtypes = [Type]
    library.LLVMPrintTypeToString.restype = c_char_p

    library.LLVMDumpType.argtype = [Type]
    library.LLVMDumpType.restype = None

    library.LLVMGetTypeContext.argtype = [Type]
    library.LLVMGetTypeContext.restype = c_object_p

    library.LLVMFunctionType.argtype = [Type, POINTER(c_object_p), c_uint, c_bool]
    library.LLVMFunctionType.restype = c_object_p

    # Pass Registry declarations.
    library.LLVMGetGlobalPassRegistry.argtypes = []
    library.LLVMGetGlobalPassRegistry.restype = c_object_p

    # Context declarations.
    library.LLVMContextCreate.argtypes = []
    library.LLVMContextCreate.restype = c_object_p

    library.LLVMContextDispose.argtypes = [Context]
    library.LLVMContextDispose.restype = None

    library.LLVMGetGlobalContext.argtypes = []
    library.LLVMGetGlobalContext.restype = c_object_p

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

    # Module declarations
    library.LLVMModuleCreateWithName.argtypes = [c_char_p]
    library.LLVMModuleCreateWithName.restype = c_object_p

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

    library.LLVMPrintModuleToFile.argtypes = [Module, c_char_p,
                                              POINTER(c_char_p)]
    library.LLVMPrintModuleToFile.restype = bool

    library.LLVMGetFirstFunction.argtypes = [Module]
    library.LLVMGetFirstFunction.restype = c_object_p

    library.LLVMGetLastFunction.argtypes = [Module]
    library.LLVMGetLastFunction.restype = c_object_p

    library.LLVMGetNextFunction.argtypes = [Function]
    library.LLVMGetNextFunction.restype = c_object_p

    library.LLVMGetPreviousFunction.argtypes = [Function]
    library.LLVMGetPreviousFunction.restype = c_object_p

    library.LLVMAddFunction.argtypes = [Module, c_char_p, Type]
    library.LLVMAddFunction.restype = c_object_p

    library.LLVMGetNamedFunction.argtypes = [Module, c_char_p]
    library.LLVMGetNamedFunction.restype = c_object_p

    library.LLVMGetTypeByName.argtypes = [Module, c_char_p]
    library.LLVMGetTypeByName.restype = c_object_p

    # Value declarations.
    library.LLVMConstNull.argtypes = [Type]
    library.LLVMConstNull.restype = c_object_p

    library.LLVMIsNull.argtypes = [Value]
    library.LLVMIsNull.restype = bool

    library.LLVMConstInt.argtypes = [Type, c_ulonglong, c_bool]
    library.LLVMConstInt.restype = c_object_p

    library.LLVMConstIntGetSExtValue.argtypes = [Value]
    library.LLVMConstIntGetSExtValue.restype = long

    library.LLVMGetValueName.argtypes = [Value]
    library.LLVMGetValueName.restype = c_char_p

    library.LLVMConstReal.argtypes = [Type, c_double]
    library.LLVMConstReal.restype = c_object_p

    library.LLVMConstRealGetDouble.argtypes = [Value, POINTER(c_bool)]
    library.LLVMConstRealGetDouble.restype = c_double

    library.LLVMTypeOf.argtypes = [Value]
    library.LLVMTypeOf.restype = c_object_p

    library.LLVMPrintValueToString.argtypes = [Value]
    library.LLVMPrintValueToString.restype = c_char_p

    library.LLVMDumpValue.argtypes = [Value]
    library.LLVMDumpValue.restype = None

    library.LLVMGetOperand.argtypes = [Value, c_uint]
    library.LLVMGetOperand.restype = c_object_p

    library.LLVMSetOperand.argtypes = [Value, Value, c_uint]
    library.LLVMSetOperand.restype = None

    library.LLVMGetNumOperands.argtypes = [Value]
    library.LLVMGetNumOperands.restype = c_uint

    # Basic Block Declarations.
    library.LLVMGetFirstBasicBlock.argtypes = [Function]
    library.LLVMGetFirstBasicBlock.restype = c_object_p

    library.LLVMGetLastBasicBlock.argtypes = [Function]
    library.LLVMGetLastBasicBlock.restype = c_object_p

    library.LLVMGetNextBasicBlock.argtypes = [BasicBlock]
    library.LLVMGetNextBasicBlock.restype = c_object_p

    library.LLVMAppendBasicBlock.argtypes = [Function, c_char_p]
    library.LLVMAppendBasicBlock.restype = c_object_p

    library.LLVMAppendBasicBlockInContext.argtypes = [Context,
                                                      Function,
                                                      c_char_p]
    library.LLVMAppendBasicBlockInContext.restype = c_object_p
    
    library.LLVMGetPreviousBasicBlock.argtypes = [BasicBlock]
    library.LLVMGetPreviousBasicBlock.restype = c_object_p

    library.LLVMGetFirstInstruction.argtypes = [BasicBlock]
    library.LLVMGetFirstInstruction.restype = c_object_p

    library.LLVMGetLastInstruction.argtypes = [BasicBlock]
    library.LLVMGetLastInstruction.restype = c_object_p

    library.LLVMBasicBlockAsValue.argtypes = [BasicBlock]
    library.LLVMBasicBlockAsValue.restype = c_object_p

    library.LLVMCountBasicBlocks.argtypes = [Function]
    library.LLVMCountBasicBlocks.restype = c_uint

    library.LLVMGetParam.argtypes = [Function, c_uint]
    library.LLVMGetParam.restype = c_object_p

    library.LLVMVerifyFunction.argtypes = [Function, c_int]
    library.LLVMVerifyFunction.restype = bool

    # Instruction Declarations.
    library.LLVMGetNextInstruction.argtypes = [Instruction]
    library.LLVMGetNextInstruction.restype = c_object_p

    library.LLVMGetPreviousInstruction.argtypes = [Instruction]
    library.LLVMGetPreviousInstruction.restype = c_object_p

    library.LLVMGetInstructionOpcode.argtypes = [Instruction]
    library.LLVMGetInstructionOpcode.restype = c_uint

def register_enumerations():
    if Enums:
        return None
    enums = [
        (Attribute, enumerations.Attributes),
        (OpCode, enumerations.OpCodes),
        (TypeKind, enumerations.TypeKinds),
        (Linkage, enumerations.Linkages),
        (Visibility, enumerations.Visibility),
        (CallConv, enumerations.CallConv),
        (IntPredicate, enumerations.IntPredicate),
        (RealPredicate, enumerations.RealPredicate),
        (LandingPadClauseTy, enumerations.LandingPadClauseTy),
        (VerifierFailureActionTy, enumerations.VerifierFailureActionTy),
    ]

    for enum_class, enum_spec in enums:
        for name, value in enum_spec:
            enum_class.register(name, value)
    return enums

def initialize_llvm():
    Context.GetGlobalContext()
    p = PassRegistry()
    lib.LLVMInitializeCore(p)
    lib.LLVMInitializeTransformUtils(p)
    lib.LLVMInitializeScalarOpts(p)
    lib.LLVMInitializeObjCARCOpts(p)
    lib.LLVMInitializeVectorization(p)
    lib.LLVMInitializeInstCombine(p)
    lib.LLVMInitializeIPO(p)
    lib.LLVMInitializeInstrumentation(p)
    lib.LLVMInitializeAnalysis(p)
    lib.LLVMInitializeIPA(p)
    lib.LLVMInitializeCodeGen(p)
    lib.LLVMInitializeTarget(p)

def shutdown_llvm():
    lib.LLVMShutdown()

register_library(lib)
Enums = register_enumerations()
initialize_llvm()
# print "Local package llvm is used!"
