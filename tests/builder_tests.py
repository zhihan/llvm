import unittest

from llvm.core import Type
from llvm.core import Value
from llvm.core import shutdown_llvm

from llvm.instruction_builder import Builder

class InstructionBuilderTest(unittest.TestCase):
    def setUp(self):
        pass

    def testAdd(self):
        ty = Type.int8()
        a = Value.const_int(ty, 1L, True)
        b = Value.const_int(ty, 1L, True)
        bldr = Builder.create()
        c = bldr.add(a, b, "Add to two")

        self.assertEqual(2L, c.get_signext_value())


if __name__ == "__main__":
    unittest.main()
