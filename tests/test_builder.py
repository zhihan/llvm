import unittest

from llvm.core import Type
from llvm.core import Value
from llvm.core import Module

from llvm.instruction_builder import Builder

from llvm.global_variables import Global

class InstructionBuilderTest(unittest.TestCase):
    def setUp(self):
        pass

    def testAdd(self):
        ty = Type.int8()
        a = Value.const_int(ty, 1L, True)
        b = Value.const_int(ty, 1L, True)
        bldr = Builder.create()
        c = bldr.add(a, b, "tmp1")

        self.assertEqual(2L, c.get_signext_value())

    def testAddGlobal(self):
        mod = Module.CreateWithName('module')
        ty = Type.int8(context=mod.context)
        a = Value.const_int(ty, 1L, True)
        g = Global.add(mod, ty, 'x')
        g.set_initializer(Value.const_int(ty, 4L, True))        
        bldr = Builder.create()
        c = bldr.add(g.get_initializer(), a, 'tmp1')
        self.assertEqual(5L, c.get_signext_value())
        
    def testAddGlobalVal(self):
        mod = Module.CreateWithName('module')
        ty = Type.int8(context=mod.context)
        a = Value.const_int(ty, 1L, True)
        g = Global.add(mod, ty, 'x')
        g.set_initializer(Value.const_int(ty, 4L, True))
        g.set_const(True)

        t = g.type
        self.assertTrue(g.is_const())
        
        bldr = Builder.create()
        # Build instruction  %tmp1 = add i8 %tmp0, 1
        c = bldr.add(bldr.load(g, "tmp0"), a, 'tmp1')
        self.assertEqual('i8', c.type.name)
        self.assertEqual('tmp1', c.name)

    def testFAdd(self):
        ty = Type.double()
        a = Value.const_real(ty, 1.0)
        b = Value.const_real(ty, 1.0)
        bldr = Builder.create()
        c = bldr.fadd(a, b, "tmp1")

        x, l = c.get_double_value()
        print x
        print l
        self.assertTrue(x - 2.0 < 0.01 and
                        2.0 - x > -0.01)

        
        
if __name__ == "__main__":
    unittest.main()
