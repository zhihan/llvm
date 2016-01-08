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
        g.initializer = Value.const_int(ty, 4, True)
        v = g.initializer

        self.assertEqual(4, v.get_signext_value())

    def testIter(self):
        ty = Type.int8()
        x = Global.add(self.module, ty, 'x')
        x.initializer = Value.const_int(ty, 1, True)
        y = Global.add(self.module, ty, 'y')
        y.initializer = Value.const_int(ty, 2, True)

        g = list(GlobalIterator(self.module))
        self.assertEqual([x, y], g)

        g = list(GlobalIterator(self.module, reverse=True))
        self.assertEqual([y, x], g)

    def testDelete(self):
        ty = Type.int8()
        x = Global.add(self.module, ty, 'x')
        x.initializer = Value.const_int(ty, 1, True)
        y = Global.add(self.module, ty, 'y')
        y.initializer = Value.const_int(ty, 2, True)   

        y.delete()
        g = list(GlobalIterator(self.module))
        self.assertEqual([x], g)
        
    def testAddAlias(self):
        ty = Type.int8()
        x = Global.add(self.module, ty, 'x')
        x.initializer = Value.const_int(ty, 1, True)
        pty = Type.pointer(ty)
        y = Global.add_alias(self.module, pty, x, 'y')

        g = list(GlobalIterator(self.module))
        self.assertEqual([x], g)

if __name__ == '__main__':
    unittest.main()
    
