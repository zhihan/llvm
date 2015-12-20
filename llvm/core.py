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
from ctypes import c_longlong
from ctypes import c_size_t
from ctypes import c_int
from ctypes import c_double
from ctypes import cast
from ctypes import pointer

from . import util  # Only import modules
from .memory_buffer import MemoryBuffer
from .context import Context
from .module import Module
from .type import Type
from .value import Value
from .value import Use
from .function import Function

from .basic_block import BasicBlock
from .basic_block import Instruction
from .basic_block import PhiNode

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
    'PhiNode',
    "VerifierFailureActionTy",
    "IntPredicate",
    "Use",
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

                
    # Pass Registry declarations.
    library.LLVMGetGlobalPassRegistry.argtypes = []
    library.LLVMGetGlobalPassRegistry.restype = c_object_p

    
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

    # Initialize native code generation for Intel Mac target.
    lib.LLVMInitializeX86TargetInfo()
    lib.LLVMInitializeX86Target()
    lib.LLVMInitializeX86TargetMC()
    lib.LLVMLinkInMCJIT()
    lib.LLVMInitializeX86AsmPrinter()
    
def shutdown_llvm():
    lib.LLVMShutdown()

register_library(lib)
Enums = register_enumerations()
initialize_llvm()
# print "Local package llvm is used!"
