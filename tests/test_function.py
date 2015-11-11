import unittest

from llvm.core import Module
from llvm.core import Type
from llvm.core import Function
from llvm.core import Value
from llvm.core import VerifierFailureActionTy

from llvm.instruction_builder import Builder

class ModuleTest(unittest.TestCase):
    def setUp(self):
        pass

    def testAppendBasicBlock(self):
        mod = Module.CreateWithName('module')
        ty = Type.int8(context=mod.context)
        ft = Type.function(ty, [ty], False)
        f = mod.add_function('timestwo', ft)
        bb = f.append_basic_block('body')
        self.assertEquals('body', bb.name)

    def testCreateFunction(self):
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

        self.assertFalse(f.verify(
            VerifierFailureActionTy.PrintMessageAction.value))

if __name__ == '__main__':
    unittest.main()
