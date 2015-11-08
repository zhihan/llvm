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

if __name__ == "__main__":
    unittest.main()
