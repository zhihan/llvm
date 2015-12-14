"""Unit test for bit reader"""
import unittest
import subprocess
from os import path

from llvm import bit_reader
from llvm import core


def generate_bitcode(filename):
    """Call clang to generate bitcode if not found on disc"""
    base, _ = filename.split('.')
    bcfile = base + '.bc'
    if not path.isfile(bcfile):
        cmd = ['clang', '-c', filename, '-emit-llvm', '-o', bcfile]
        subprocess.Popen(cmd).communicate()
    

class ReaderTest(unittest.TestCase):
    def test_timestwo(self):
        p = path.dirname(__file__)
        generate_bitcode(path.join(p, 'timestwo.c'))
        mem = core.MemoryBuffer.fromFile(path.join(p, 'timestwo.bc'))
        mod = bit_reader.parse_bitcode(mem)

        f = mod.get_function('timestwo')
        self.assertTrue(len(str(f)) > 10)

if __name__ == "__main__":
    unittest.main()

