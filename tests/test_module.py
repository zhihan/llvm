import unittest

from llvm.core import Module
from llvm.core import Type
from llvm.core import Function
from llvm.core import Context

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

        self.assertTrue('timestwo' in str(mod))

    def testDataLayout(self):
        context = Context()
        mod = Module.CreateWithName('module', context)
        mod.datalayout = 'E-p:32:32'

        self.assertEqual('E-p:32:32', mod.datalayout)

    def testTarget(self):
        context = Context()
        mod = Module.CreateWithName('module', context)
        mod.target = 'i686-apple-darwin9'

        self.assertEqual('i686-apple-darwin9', mod.target)
        
if __name__ == '__main__':
    unittest.main()
