############################################################################
#
# Get information that might be useful regarding system and libraries
# for debugging purpose
#
# Usage:
# import PythonInfo
# print PythonInfo('pythoninfo.cfg').info().yaml()
#
############################################################################
import sys
import json
from lib import SysUtils
#from lib import DbUtils
#from lib import NetUtils

class PythonInfo(object):

    class ResultStruct(object):
        # result storage n converter
        data = dict()

        def __str__(self):
            return self.yaml()

        def add(self, section, info):
            self.data[section] = info

        def json(self):
            return json.dumps(self.data)

        def yaml(self):
            from lib import yaml
            return yaml.dumps(self.data)

    data = ResultStruct()

    def _retrieve_basic_data(self):
        # get sys info from python API
        sys_result = dict()
        for func_name in dir(SysUtils):
            if not func_name.startswith('get'):
                continue
                
            try:
                display_func_name = func_name.replace('get_', '').replace('_', ' ').title()
                sys_result[display_func_name] = getattr(SysUtils, func_name)()
            except:
                pass #ignore error

        self.data.add('System', sys_result)
        
    def __init__(self, cfg_file=None):
        #TODO - use cfg_file variable
        self._retrieve_basic_data()

    def info(self):
        return self.data

if __name__ == "__main__":
    cfg_file = sys.argv[1] if len(sys.argv) > 1 else None
    p = PythonInfo(cfg_file)
    print(p.info())
