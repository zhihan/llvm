import unittest

from llvm.core import Type
from llvm.core import Value
from llvm.core import Module

from llvm.global_variables import Global

class GlobalTest(unittest.TestCase):
    def setUp(self):
        pass

    def testAdd(self):
        ty = Type.int8()
        mod = Module.CreateWithName('module')
        g = Global.add(mod, ty, 'x')
        self.assertEqual('x', g.name)

        g2 = Global.get(mod, 'x')
        self.assertEqual('x', g2.name)
    
if __name__ == "__main__":
    unittest.main()
