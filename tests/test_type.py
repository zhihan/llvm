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
 
    def testCreateFunction(self):
        ty = Type.int8()
        f = Type.function(ty, [ty], False)

        self.assertEqual('i8 (i8)', f.name)

    def testCreatePointer(self):
        ty = Type.int8()
        p = Type.pointer(ty)
    
        self.assertEqual('i8*', p.name)

        t = p.element_type()
        self.assertEqual('i8', t.name)

    def testCreateStruct(self):
        ty = Type.int8()
        p = Type.structure([ty, ty], False)

        self.assertEqual('{ i8, i8 }', p.name)
        self.assertEqual(2, p.num_elements())

        elems = p.elements()
        t1 = elems[0]
        self.assertEqual('i8', t1.name)
        t2 = elems[1]
        self.assertEqual('i8', t2.name)
        
if __name__ == '__main__':
    unittest.main()
