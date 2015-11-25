import unittest

from llvm.core import Module
from llvm.core import Type
from llvm.core import Function
from llvm.core import Value
from llvm.core import VerifierFailureActionTy

from llvm.instruction_builder import Builder

from llvm.global_variables import Global

from testing import *
        
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
        mod, f = create_timestwo_module()

        self.assertFalse(f.verify(
            VerifierFailureActionTy.PrintMessageAction.value))

        x = [fn for fn in mod]
        self.assertEquals([f], x)

        bbs = [b for b in f]
        self.assertEquals(1, len(bbs))

        ins = [i for i in bbs[0]]
        self.assertEquals(2, len(ins))

if __name__ == '__main__':
    unittest.main()
