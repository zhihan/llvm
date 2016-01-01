import unittest
import sys

from llvm.core import Context
from llvm.core import Type
from llvm.core import Value
from llvm.core import Module

from llvm.global_variables import Global

class ValueTest(unittest.TestCase):
    def setUp(self):
        self.context = Context()
        self.module = Module.CreateWithName('module', context=self.context)

    def testNullInt8(self):
        ty = Type.int8()
        v = Value.null(ty)

        self.assertTrue(v.is_null())
        self.assertTrue(v.is_const_int())
        v.dump()

    def testUndefInt8(self):
        ty = Type.int8()
        v = Value.undef(ty)

        self.assertTrue(v.is_undef())
    
    def testAllOnesInt8(self):
        ty = Type.int8()
        v = Value.all_ones(ty)

        self.assertEqual(-1, v.get_signext_value())

    def testNullPtr(self):
        ty = Type.int8()
        v = Value.null_ptr(Type.pointer(ty))

        self.assertTrue(v.is_null())
        self.assertFalse(v.is_const_int())

    def testTypeOfInt8(self):
        ty = Type.int8()
        v = Value.const_int(ty, 2, True)

        t = v.type
        self.assertEqual('i8', t.name)

    def testZeroExt(self):
        ty = Type.int8()
        v = Value.all_ones(ty)

        self.assertEqual(255, v.get_zeroext_value())

    def testConstInt8(self):
        ty = Type.int8()
        v = Value.const_int(ty, 3, True)

        self.assertEqual(3, v.get_signext_value())
        self.assertEqual('i8 3', str(v))
        self.assertEqual('i8', v.type.name)
        self.assertFalse(v.is_undef())

    def testConstInt8Array(self):
        ty = Type.int8()
        v = Value.const_int(ty, 3, True)
        arr = Value.const_array(ty, [v, v])

        arr_ty = arr.type
        self.assertEqual(2, arr_ty.array_length())
        self.assertEqual([v, v], arr.array_elements())
        self.assertFalse(v.is_const_array())
        self.assertTrue(arr.is_const_array())

    def testStruct(self):
        ty = Type.int8()
        sty = Type.structure([ty, ty], False)
        x = Value.const_int(ty, 1, True)
        y = Value.const_int(ty, 2, True)
        xy = Value.const_struct([x, y])

        self.assertTrue(xy.is_const_struct())
        
    def testConstantCannotBeNamed(self):
        ty = Type.int8()
        v = Value.const_int(ty, 3, True)
        self.assertEqual('', v.name)
        v.name = 'something'
        self.assertEqual('', v.name)
        
    def testName(self):
        # constants cannot be named. 
        ty = Type.int8(context=self.module.context)
        v = Global.add(self.module, ty, 'x')

        self.assertEqual('x', v.name)
        v.name = 'one'
        self.assertEqual('one', v.name)
        self.assertTrue(v.is_constant())
        self.assertFalse(v.is_undef())


if __name__ == "__main__":
    unittest.main()
