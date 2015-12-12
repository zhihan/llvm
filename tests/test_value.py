import unittest

from llvm.core import Context
from llvm.core import Type
from llvm.core import Value
from llvm.core import Module

from llvm.global_variables import Global

class ValueTest(unittest.TestCase):
    def setUp(self):
        self.module = Module.CreateWithName('module')

    def testNullInt8(self):
        ty = Type.int8()
        v = Value.null(ty)

        self.assertTrue(v.is_null())

    def testTypeOfInt8(self):
        ty = Type.int8()
        v = Value.const_int(ty, 2, True)

        t = v.type
        self.assertEqual('i8', t.name)

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
