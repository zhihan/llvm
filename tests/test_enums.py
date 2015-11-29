import unittest

from llvm.core import Attribute

class EnumTest(unittest.TestCase):
    def testAttribute(self):
        a = Attribute.Alignment

        self.assertEqual('Attribute.Alignment', str(a))
        self.assertEqual('Alignment', a.name)
        
        b = Attribute.from_value(a.value)
        self.assertEqual(a, b)
        
if __name__ == "__main__":
    unittest.main()
