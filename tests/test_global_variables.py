import unittest

from llvm.core import Context
from llvm.core import Type
from llvm.core import Value
from llvm.core import Module

from llvm.global_variables import Global
from llvm.global_variables import GlobalIterator

class GlobalTest(unittest.TestCase):
    def setUp(self):
        self.context = Context()
        self.module = Module.CreateWithName('module', context=self.context)
        

    def testAdd(self):
        ty = Type.int8()
        mod = self.module
        g = Global.add(mod, ty, 'x')
        self.assertEqual('x', g.name)

        g2 = Global.get(mod, 'x')
        self.assertEqual('x', g2.name)

    def testInit(self):
        ty = Type.int8()
        mod = self.module
        g = Global.add(mod, ty, 'x')
        g.set_initializer(Value.const_int(ty, 4, True))
        v = g.get_initializer()

        self.assertEqual(4, v.get_signext_value())

    def testIter(self):
        ty = Type.int8()
        x = Global.add(self.module, ty, 'x')
        x.set_initializer(Value.const_int(ty, 1, True))
        y = Global.add(self.module, ty, 'y')
        y.set_initializer(Value.const_int(ty, 2, True))

        g = list(GlobalIterator(self.module))
        self.assertEqual([x, y], g)

        g = list(GlobalIterator(self.module, reverse=True))
        self.assertEqual([y, x], g)
    
if __name__ == '__main__':
    unittest.main()
    
