import unittest

from llvm.core import MemoryBuffer

class MemoryBufferTest(unittest.TestCase):
    def setUp(self):
        pass

    def testFromString(self):
        content = 'abcd'
        mem = MemoryBuffer.from_string(content)

        self.assertEqual(content, str(mem))
        self.assertEqual(4, len(mem))


    def testFromFile(self):
        filename = __file__
        mem = MemoryBuffer.fromFile(filename)

        self.assertTrue(len(mem) > 10)

    def testFromFileNone(self):
        filename = None
        with self.assertRaises(Exception):
            mem = MemoryBuffer.fromFile(filename)
        

if __name__ == "__main__":
    unittest.main()
