import unittest

from llvm.core import Context
from llvm.core import Type
from llvm.core import Value

class ValueTest(unittest.TestCase):
    def setUp(self):
        pass

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

        self.assertEquals(3L, v.get_signext_value())
        self.assertEquals('i8 3', str(v))

    def testName(self):
        ty = Type.int8()
        v = Value.const_int(ty, 1, True)

        self.assertEqual('', v.name)
        v.name = 'one'
        # self.assertEqual('one', v.name)


if __name__ == "__main__":
    unittest.main()
