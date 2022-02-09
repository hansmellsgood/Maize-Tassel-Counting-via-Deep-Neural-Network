import unittest
#import pytest
from main2 import *

class MyTestCase(unittest.TestCase):
    def test_1(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
