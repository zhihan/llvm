from llvm.core import Module
from llvm.core import Type
from llvm.core import Function
from llvm.core import Value
from llvm.core import VerifierFailureActionTy

from llvm.instruction_builder import Builder

from llvm.global_variables import Global

def create_timestwo_module():
    mod = Module.CreateWithName('module')
    ty = Type.int8(context=mod.context)
    ft = Type.function(ty, [ty], False)
    f = mod.add_function('timestwo', ft)
    bb = f.append_basic_block('body')
    bldr = Builder.create(mod.context)
    bldr.position_at_end(bb)
    x = f.get_param(0)
    two = Value.const_int(ty, 2L, True)
    y = bldr.mul(x, two, 'res')
    bldr.ret(y)    
    return (mod, f)

def create_timestwo_module_with_local():
    mod = Module.CreateWithName('module')
    ty = Type.int8(context=mod.context)
    ft = Type.function(ty, [ty], False)
    f = mod.add_function('timestwo', ft)
    bb = f.append_basic_block('body')
    bldr = Builder.create(mod.context)
    bldr.position_at_end(bb)

    two_ptr = bldr.alloca(ty, "two_ptr")
    bldr.store(Value.const_int(ty, 2L, True), two_ptr)
    two = bldr.load(two_ptr, "two")

    x = f.get_param(0)
    y = bldr.mul(x, two, 'res')
    bldr.ret(y)
    return (mod, f)
    
def create_timestwo_module_with_global():
    mod = Module.CreateWithName('module')
    ty = Type.int8(mod.context)
    k = Global.add(mod, ty, 'k')
    k.set_initializer(Value.const_int(ty, 2L, True))
    
    ft = Type.function(ty, [ty], False)
    f = mod.add_function('timestwo', ft)
    bb = f.append_basic_block('body')
    bldr = Builder.create(mod.context)
    bldr.position_at_end(bb)

    x = f.get_param(0)
    two = bldr.load(k, "two")
    y = bldr.mul(x, two, 'res')
    bldr.ret(y)    
    return (mod, f)

def create_lessthanzero_module():
    mod = Module.CreateWithName('module')

    ty = Type.int8(context=mod.context)
    bool_t = Type.int1(context=mod.context)
    ft = Type.function(bool_t, [ty], False)
    
    f = mod.add_function('lessthanzero', ft)
    bb = f.append_basic_block('body')
    bldr = Builder.create(mod.context)
    bldr.position_at_end(bb)
    x = f.get_param(0)
    zero = Value.const_int(ty, 0L, True)
    y = bldr.int_signed_lt(x, zero, 'res')
    bldr.ret(zero)    
    return (mod, f)
    
