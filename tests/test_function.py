import unittest

from llvm.core import Module
from llvm.core import Type
from llvm.core import Function
from llvm.core import Value
from llvm.core import VerifierFailureActionTy
from llvm.core import OpCode
from llvm.core import PhiNode

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
        
        self.assertEquals(mod.first, f)
        self.assertEquals(mod.last, f)
        
        x = [fn for fn in mod]
        self.assertEquals([f], x)

        x = [fn for fn in reversed(mod)]
        self.assertEquals([f], x)

        bbs = [b for b in f]
        self.assertEquals(1, len(bbs))

        ins = [i for i in bbs[0]]
        self.assertEquals(2, len(ins))

    def test_phi(self):
        mod, _  = create_abs_module()
        f = mod.get_function('abs')
        bb = [b for b in f if b.name == 'merge']
        instruction = [i for i in bb[0] if i.name == 'y']
    
        self.assertEqual(OpCode.PHI, instruction[0].opcode)
        phi = PhiNode(instruction[0].from_param())
        self.assertEqual(2, phi.count_incoming())

        values = phi.incoming_values()
        self.assertEqual(2, len(values))

        bb = phi.incoming_blocks()
        self.assertEqual(2, len(bb))


        
if __name__ == '__main__':
    unittest.main()
