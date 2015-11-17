import unittest

from llvm.core import Type
from llvm.execution import GenericValue
from llvm.execution import ExecutionEngine

from testing import create_timestwo_module
from testing import create_timestwo_module_with_local
from testing import create_timestwo_module_with_global
from testing import create_lessthanzero_module
from testing import create_abs_module
from testing import create_cumsum_module

class ExecutionTest(unittest.TestCase):
    def setUp(self):
        pass

    def testCreateGenericValue(self):
        ty = Type.int8()
        gv = GenericValue.of_int(ty, 4L, True)
        self.assertEquals(4L, gv.to_int(True))

        gv = GenericValue.of_int(ty, 128 + 4, False)
        self.assertEquals(132, gv.to_int(False))
        
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
        
    def testTimesTwoWithGlobal(self):
        mod, _ = create_timestwo_module_with_global()
        ee = ExecutionEngine.create_interpreter(mod)
        ty = Type.int8(context=mod.context)
        f = mod.get_function('timestwo')
        x = GenericValue.of_int(ty, 3L, True)
        y = ee.run_function(f, [x])
        self.assertEquals(6L, y.to_int(True))

    def testTimesTwoWithGlobal(self):
        mod, _ = create_timestwo_module_with_global()
        ee = ExecutionEngine.create_interpreter(mod)
        ty = Type.int8(context=mod.context)
        f = mod.get_function('timestwo')
        x = GenericValue.of_int(ty, 3L, True)
        y = ee.run_function(f, [x])
        self.assertEquals(6L, y.to_int(True))

    def testLessThanZero(self):
        mod, _ = create_lessthanzero_module()
        ee = ExecutionEngine.create_interpreter(mod)
        ty = Type.int8(context=mod.context)
        f = mod.get_function('lessthanzero')
        x = GenericValue.of_int(ty, 3L, True)
        y = ee.run_function(f, [x])
        self.assertEquals(0L, y.to_int(True) & 1L)
        
        x = GenericValue.of_int(ty, -3L, True)
        y = ee.run_function(f, [x])
        self.assertEquals(1L, y.to_int(True) & 1L)
        

    def testAbs(self):
        mod, _ = create_abs_module()
        ee = ExecutionEngine.create_interpreter(mod)
        ty = Type.int8(context=mod.context)
        f = mod.get_function('abs')

        x = GenericValue.of_int(ty, 3L, True)
        y = ee.run_function(f, [x])
        self.assertEquals(3L, y.to_int(True))

        x = GenericValue.of_int(ty, -3L, True)
        y = ee.run_function(f, [x])
        self.assertEquals(3L, y.to_int(True) & 255L)

    def testCumsum(self):
        mod, _ = create_cumsum_module()
        ee = ExecutionEngine.create_interpreter(mod)
        ty = Type.int8(context=mod.context)
        f = mod.get_function('cumsum')
        x = GenericValue.of_int(ty, 10L, True)
        y = ee.run_function(f, [x])
        self.assertEquals(55L, y.to_int(True))

if __name__ == '__main__':
    unittest.main()
