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
        two = Value.const_int(self.ty, 2L, True)
        y = self.bldr.mul(x, two, 'res')
        
        use = Use.first(x)
        self.assertTrue(use.next is None)
        self.assertEqual(y, use.user)
        self.assertEqual(x, use.used_value)

if __name__ == "__main__":
    unittest.main()
