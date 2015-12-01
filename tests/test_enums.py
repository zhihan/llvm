import unittest

from llvm.core import Attribute
from llvm.core import Type
from llvm.common import *
from llvm.common import LLVMObject

class EnumTest(unittest.TestCase):
    def testAttribute(self):
        a = Attribute.Alignment

        self.assertEqual('Attribute.Alignment', str(a))
        self.assertEqual('Alignment', a.name)
        
        b = Attribute.from_value(a.value)
        self.assertEqual(a, b)


class LLVMObjectTest(unittest.TestCase):
    def testEqual(self):
        a = LLVMObject(c_object_p())
        self.assertTrue(a.is_null())

        b = LLVMObject(c_object_p())
        self.assertEqual(a, b)

        c = Type.int8()
        self.assertNotEqual(c, b)
        self.assertFalse(c.__eq__(b))
        self.assertNotEqual(b, c)
        
if __name__ == "__main__":
    unittest.main()
