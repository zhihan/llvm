import unittest

from llvm.core import Context
from llvm.core import Type

class TypeTest(unittest.TestCase):
    def setUp(self):
        self.global_context = Context.GetGlobalContext()
    
    def testCreateInt8(self):
        ty = Type.int8(self.global_context)
        self.assertEqual('i8', ty.name)
        ty.dump()

        ty = Type.int8()
        self.assertEqual('i8', ty.name)
        ty.dump()
        
    def testCreateInt1(self):
        ty = Type.int1(self.global_context)
        self.assertEqual('i1', ty.name)
        ty.dump()

        ty = Type.int1()
        self.assertEqual('i1', ty.name)
        ty.dump()
 

if __name__ == '__main__':
    unittest.main()
