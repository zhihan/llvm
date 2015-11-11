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

    def testInit(self):
        ty = Type.int8()
        mod = Module.CreateWithName('module')
        g = Global.add(mod, ty, 'x')
        g.set_initializer(Value.const_int(ty, 4L, True))
        v = g.get_initializer()

        self.assertEqual(4L, v.get_signext_value())
    
