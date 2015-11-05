import unittest

from llvm.core import Context
from llvm.core import Type

class TypeTest(unittest.TestCase):
    def setUp(self):
        self.global_context = Context.GetGlobalContext()
    
    def testCreateInt8(self):
        ty = Type.Int8(self.global_context)
        self.assertEqual('i8', ty.name)


if __name__ == '__main__':
    unittest.main()
