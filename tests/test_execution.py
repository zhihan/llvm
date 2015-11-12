import unittest

from llvm.core import Type
from llvm.execution import GenericValue
from llvm.execution import ExecutionEngine

from test_function import create_timestwo_module
from test_function import create_timestwo_module_with_local

class ExecutionTest(unittest.TestCase):
    def setUp(self):
        pass

    def testCreateGenericValue(self):
        ty = Type.int8()
        gv = GenericValue.of_int(ty, 4L, True)
        self.assertEquals(4L, gv.to_int(True))

    def testTimesTwo(self):
        mod, _ = create_timestwo_module()
        ee = ExecutionEngine.create_interpreter(mod)
        ty = Type.int8(context=mod.context)
        f = mod.get_function('timestwo')
        x = GenericValue.of_int(ty, 3L, True)
        y = ee.run_function(f, [x])
        self.assertEquals(6L, y.to_int(True))

    def testTimesTwoWithLocal(self):
        mod, _ = create_timestwo_module_with_local()
        ee = ExecutionEngine.create_interpreter(mod)
        ty = Type.int8(context=mod.context)
        f = mod.get_function('timestwo')
        x = GenericValue.of_int(ty, 3L, True)
        y = ee.run_function(f, [x])
        self.assertEquals(6L, y.to_int(True))
        

if __name__ == '__main__':
    unittest.main()
