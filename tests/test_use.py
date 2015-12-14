import unittest

from llvm.core import Module
from llvm.core import Type
from llvm.core import Function
from llvm.core import Value
from llvm.core import Use
from llvm.instruction_builder import Builder

class UseTest(unittest.TestCase):
    def setUp(self):
        mod = Module.CreateWithName('module')
        ty = Type.int8(context=mod.context)
        ft = Type.function(ty, [ty], False)
        f = mod.add_function('timestwo', ft)
        bb = f.append_basic_block('body')
        bldr = Builder.create(mod.context)
        bldr.position_at_end(bb)

        self.bldr = bldr
        self.ty = ty
        self.f = f
        
    def testUse(self):
        x = self.f.get_param(0)
        two = Value.const_int(self.ty, 2, True)
        y = self.bldr.mul(x, two, 'res')
        
        use = Use.first(x)
        self.assertTrue(use.next is None)
        self.assertEqual(y, use.user)
        self.assertEqual(x, use.used_value)

    def testOperands(self):
        x = self.f.get_param(0)
        two = Value.const_int(self.ty, 2, True)
        y = self.bldr.mul(x, two, 'res')

        ops = y.operands
        self.assertEqual(2, len(ops))
        self.assertEqual([x, two], ops)

        uses = y.uses
        self.assertEqual(2, len(uses))
        self.assertEqual(x, uses[0].used_value)
        self.assertEqual(y, uses[0].user)
        self.assertEqual(two, uses[1].used_value)
        self.assertEqual(y, uses[1].user)

        y.set_operand(0, two)
        # y.dump()
        ops = y.operands
        self.assertEqual(2, len(ops))
        self.assertEqual([two, two], ops)


    def test_replace_uses(self):
        x = self.f.get_param(0)
        two = Value.const_int(self.ty, 2, True)
        y = self.bldr.mul(x, two, 'res')

        c = Value.const_int(self.ty, 3, True)
        x.replace_uses_with(c)

        #print(y)
        self.assertEqual(2, len(y.operands))
        self.assertEqual([c, two], y.operands)
        
if __name__ == "__main__":
    unittest.main()
