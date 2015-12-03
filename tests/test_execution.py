import unittest

from llvm.core import Type
from llvm.core import VerifierFailureActionTy

from llvm.execution import GenericValue
from llvm.execution import ExecutionEngine

from testing import *

class ExecutionTest(unittest.TestCase):
    def setUp(self):
        pass

    def testCreateGenericIntValue(self):
        ty = Type.int8()
        gv = GenericValue.of_int(ty, 4L, True)
        self.assertEquals(4L, gv.to_int(True))

        gv = GenericValue.of_int(ty, 128 + 4, False)
        self.assertEquals(132, gv.to_int(False))

    def testCreateGenericDouble(self):
        ty = Type.double()
        gv = GenericValue.of_float(ty, 3.5)
        x = gv.to_float(ty)
        self.assertTrue(x - 3.5 < 0.001 and
                        3.5 - x < 0.001)
        
    def testTimesTwo(self):
        mod, _ = create_timestwo_module()
        ee = ExecutionEngine.create_interpreter(mod)
        ty = Type.int8(context=mod.context)
        f = mod.get_function('timestwo')
        x = GenericValue.of_int(ty, 3L, True)
        y = ee.run_function(f, [x])
        self.assertEquals(6L, y.to_int(True))

    def testTimesTwo_JIT(self):
        mod = create_two_module()
        ee = ExecutionEngine.create_jit(mod)
        ty = Type.int8(context=mod.context)
        f = mod.get_function('two')
        y = ee.run_function(f, [])
        self.assertEquals(2L, y.to_int(True))
        
    def testTimesTwo_execution(self):
        mod = create_two_module()
        ee = ExecutionEngine.create_execution_engine(mod)
        ty = Type.int8(context=mod.context)
        f = mod.get_function('two')
        y = ee.run_function(f, [])
        self.assertEquals(2L, y.to_int(True))

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

    def testTimesTwoWithFunction(self):
        mod = create_timestwo_module_with_function()
        ee = ExecutionEngine.create_interpreter(mod)
        ty = Type.int8(context=mod.context)
        f = mod.get_function('caller')
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

    def testGlobalLoadStore(self):
        mod = create_global_load_save_module()
        ee = ExecutionEngine.create_interpreter(mod)
        load = mod.get_function('load')
        x0 = ee.run_function(load, [])
        self.assertEquals(0L, x0.to_int(True))

        ty = Type.int8(context=mod.context)
        y = GenericValue.of_int(ty, 4L, True)
        store = mod.get_function('store')
        ee.run_function(store, [y])
        x = ee.run_function(load, [])
        self.assertEquals(4L, x.to_int(True))

    def testGlobalArrayLoadStore(self):
        mod = create_global_load_save_array_module()
        ee = ExecutionEngine.create_interpreter(mod)
        load = mod.get_function('load')
        ptr_ty = Type.int64(context=mod.context)
        offset = GenericValue.of_int(ptr_ty, 1L, True)
        x0 = ee.run_function(load, [offset])
        self.assertEquals(0L, x0.to_int(True))

        ty = Type.int8(context=mod.context)
        y = GenericValue.of_int(ty, 4L, True)
        store = mod.get_function('store')
        ee.run_function(store, [y, offset])
        x = ee.run_function(load, [offset])
        self.assertEquals(4L, x.to_int(True))


if __name__ == '__main__':
    unittest.main()
