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
        a = Value.const_int(ty, 1, True)
        b = Value.const_int(ty, 1, True)
        bldr = Builder.create()
        c = bldr.add(a, b, "tmp1")

        self.assertEqual(2, c.get_signext_value())

    def testAddGlobal(self):
        mod = Module.CreateWithName('module')
        ty = Type.int8(context=mod.context)
        a = Value.const_int(ty, 1, True)
        g = Global.add(mod, ty, 'x')
        g.initializer = Value.const_int(ty, 4, True)
        bldr = Builder.create()
        c = bldr.add(g.initializer, a, 'tmp1')
        self.assertEqual(5, c.get_signext_value())

    def testAddGlobalVal(self):
        mod = Module.CreateWithName('module')
        ty = Type.int8(context=mod.context)
        a = Value.const_int(ty, 1, True)
        g = Global.add(mod, ty, 'x')
        g.initializer = Value.const_int(ty, 4, True)
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
        self.assertTrue(x - 2.0 < 0.01 and
                        2.0 - x > -0.01)

    def testFAdd_float(self):
        ty = Type.float()
        a = Value.const_real(ty, 1.0)
        b = Value.const_real(ty, 1.0)
        bldr = Builder.create()
        c = bldr.fadd(a, b, "tmp1")

        x, l = c.get_double_value()
        self.assertTrue(x - 2.0 < 0.01 and
                        2.0 - x > -0.01)
        self.assertFalse(l)

    def testValueFromString(self):
        ty = Type.double()
        a = Value.const_real(ty, 1.0)
        b = Value.const_real(ty, "1.0")

        x, _ = a.get_double_value()
        y, _ = b.get_double_value()
        self.assertEqual(x, y)

    def testIntSLT(self):
        ty = Type.int8()
        a = Value.const_int(ty, 1, True)
        b = Value.const_int(ty, 2, True)
        bldr = Builder.create()

        c = bldr.int_signed_lt(a, b, "tmp1")
        self.assertEqual(1, c.get_zeroext_value())

        d = bldr.int_signed_lt(b, a, "tmp2")
        self.assertEqual(0, d.get_zeroext_value())

        e = bldr.int_signed_lt(a, a, "tmp3")
        self.assertEqual(0, e.get_zeroext_value())

    def testIntSGT(self):
        ty = Type.int8()
        a = Value.const_int(ty, 1, True)
        b = Value.const_int(ty, 2, True)
        bldr = Builder.create()

        c = bldr.int_signed_gt(a, b, "tmp1")
        self.assertEqual(0, c.get_zeroext_value())

        d = bldr.int_signed_gt(b, a, "tmp2")
        self.assertEqual(1, d.get_zeroext_value())

        e = bldr.int_signed_gt(a, a, "tmp3")
        self.assertEqual(0, e.get_zeroext_value())

    def testIntEQ(self):
        ty = Type.int8()
        a = Value.const_int(ty, 1, True)
        b = Value.const_int(ty, 2, True)
        bldr = Builder.create()

        c = bldr.int_eq(a, b, "tmp1")
        self.assertEqual(0, c.get_zeroext_value())

        d = bldr.int_eq(a, a, "tmp3")
        self.assertEqual(1, d.get_zeroext_value())

    def testIntNE(self):
        ty = Type.int8()
        a = Value.const_int(ty, 1, True)
        b = Value.const_int(ty, 2, True)
        bldr = Builder.create()

        c = bldr.int_ne(a, b, "tmp1")
        self.assertEqual(1, c.get_zeroext_value())

        d = bldr.int_ne(a, a, "tmp3")
        self.assertEqual(0, d.get_zeroext_value())

    def testAlloca(self):
        ty = Type.int8()
        bldr = Builder.create()

        a = bldr.alloca(ty, 'a')
        self.assertEqual('  %a = alloca i8', str(a))

        arr = Type.array(ty, 2)
        b = bldr.alloca(arr, 'b')
        self.assertEqual('  %b = alloca [2 x i8]', str(b))
        
    def testLoad(self):
        ty = Type.int8()
        pt = Type.pointer(ty)
        bldr = Builder.create()

        a = bldr.alloca(ty, 'a')
        b = bldr.load(a, 'b')
        self.assertEqual('  %b = load i8* %a', str(b))

    def testInsertValue(self):
        ty = Type.int8()
        v = Value.const_int(ty, 1, True)
        n = Value.const_int(ty, 2, True)
        arr_ty = Type.array(ty, 2)
        bldr = Builder.create()

        a = bldr.alloca(arr_ty, 'a')
        a_content = bldr.load(a, 'content')
        b = bldr.insert_value(a_content, v, 0, 'b')
        self.assertEqual('  %b = insertvalue [2 x i8] %content, i8 1, 0', str(b))

        c = bldr.extract_value(a_content, 0, 'c')
        self.assertEqual('  %c = extractvalue [2 x i8] %content, 0', str(c))
        

    def testGEP(self):
        ty = Type.int64()
        ptr_ty = Type.int64()
        bldr = Builder.create()
        arr_ty = Type.array(ty, 2)
        
        a = bldr.alloca(arr_ty, 'a')
        offset = Value.const_int(ptr_ty, 0, True)
        b = bldr.gep(a, [offset, offset], 'gep')
        self.assertEqual('  %gep = getelementptr [2 x i64]* %a, i64 0, i64 0',
                         str(b))
        
if __name__ == "__main__":
    unittest.main()
