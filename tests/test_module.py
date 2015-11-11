import unittest

from llvm.core import Module
from llvm.core import Type
from llvm.core import Function

class ModuleTest(unittest.TestCase):
    def setUp(self):
        pass

    def testAddFunction(self):
        mod = Module.CreateWithName('module')
        ty = Type.int8(context=mod.context)
        ft = Type.function(ty, [ty], False)
        f = mod.add_function('timestwo', ft)
        
        self.assertEquals('timestwo', f.name)
        f1 = mod.first
        self.assertEquals('timestwo', f1.name)

        fcns = [fn for fn in mod]
        self.assertEquals(1, len(fcns))

if __name__ == '__main__':
    unittest.main()
