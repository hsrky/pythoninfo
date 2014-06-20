import unittest
from nose.tools import assert_not_equals
from pythoninfo import PythonInfo


class TestPythonInfo(unittest.TestCase):
    def test_info(self):
        # FIXME
        value = PythonInfo().info().json()
        assert_not_equals(len(value), 0)

if __name__ == '__main__':
    unittest.main()