"""Test module to generate simple LLVM modules."""
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

def create_timestwo_module_with_function():
    mod = Module.CreateWithName('module')
    ty = Type.int8(context=mod.context)
    ft = Type.function(ty, [ty], False)
    bldr = Builder.create(mod.context)

    f = mod.add_function('timestwo', ft)
    bb = f.append_basic_block('body')
    bldr.position_at_end(bb)
    x = f.get_param(0)
    two = Value.const_int(ty, 2L, True)
    y = bldr.mul(x, two, 'res')
    bldr.ret(y)

    f2 = mod.add_function('caller', ft)
    bb = f2.append_basic_block('body')
    exit = f2.append_basic_block('exit')
    bldr.position_at_end(bb)
    inv = bldr.invoke(f, [f2.get_param(0)], exit, exit, 'invoke')
    bldr.position_at_end(exit)
    bldr.ret(inv)
    
    return mod


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
    bldr.ret(y)    
    return (mod, f)
    

def create_abs_module():
    mod = Module.CreateWithName('module')

    ty = Type.int8(context=mod.context)
    ft = Type.function(ty, [ty], False)
    
    f = mod.add_function('abs', ft)
    bb1 = f.append_basic_block('body')
    bbt = f.append_basic_block('true')
    bbf = f.append_basic_block('false')
    bbm = f.append_basic_block('merge')

    bldr = Builder.create(mod.context)
    bldr.position_at_end(bb1)
    x = f.get_param(0)
    zero = Value.const_int(ty, 0L, True)
    c = bldr.int_signed_lt(x, zero, 'comp')
    bldr.conditional_branch(c, bbt, bbf)

    # True branch
    bldr.position_at_end(bbt)
    y_t = bldr.neg(x, 'neg_x')
    bldr.branch(bbm)
    
    # False branch
    bldr.position_at_end(bbf)
    bldr.branch(bbm)
    
    bldr.position_at_end(bbm)
    y = bldr.phi(ty, 'y')
    y.add_incoming([y_t, x], [bbt, bbf])
    bldr.ret(y)
    return (mod, f)

def create_cumsum_module():
    mod = Module.CreateWithName('module')

    ty = Type.int8(context=mod.context)
    ft = Type.function(ty, [ty], False)
    
    f = mod.add_function('cumsum', ft)
    bb1 = f.append_basic_block('body')
    bb_hdr = f.append_basic_block('hdr')
    bb_loop = f.append_basic_block('loop')
    bb_exit = f.append_basic_block('exit')

    bldr = Builder.create(mod.context)
    bldr.position_at_end(bb1)
    bldr.branch(bb_hdr)

    bldr.position_at_end(bb_hdr)
    i = bldr.phi(ty, 'i')
    s = bldr.phi(ty, 's')
    zero = Value.const_int(ty, 0L, True)
    c = bldr.int_signed_lt(zero, i, 'comp')
    bldr.conditional_branch(c, bb_loop, bb_exit)

    bldr.position_at_end(bb_loop)
    s1 = bldr.add(s, i, 's1')
    i1 = bldr.sub(i, Value.const_int(ty, 1L, True), 'i1')
    bldr.branch(bb_hdr)

    i.add_incoming([f.get_param(0), i1], [bb1, bb_loop])
    s.add_incoming([Value.const_int(ty, 0L, True), s1], [bb1, bb_loop])
    
    bldr.position_at_end(bb_exit)
    bldr.ret(s)
    return (mod, f)
