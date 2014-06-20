import unittest
from nose.tools import assert_not_equals

from pythoninfo.lib.yaml import yaml

class TestYaml(unittest.TestCase):
    def test_dumps(self):
        # FIXME
        test_data1 = dict(test='data')
        assert_not_equals(len(yaml.dumps(test_data1)), 0)

if __name__ == '__main__':
    unittest.main()