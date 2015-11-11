import unittest

from llvm.core import Type
from llvm.execution import GenericValue

class ExecutionTest(unittest.TestCase):
    def setUp(self):
        pass

    def testCreateGenericValue(self):
        ty = Type.int8()
        gv = GenericValue.of_int(ty, 4L, True)
        self.assertEquals(4L, gv.to_int(True))


if __name__ == '__main__':
    unittest.main()
