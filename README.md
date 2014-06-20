PythonInfo
==========
Python environment information for debugging

Usage
-----
As a libary
```python
from pythoninfo import PythonInfo
p = PythonInfo()
# YAML style output
p.info().yaml()

# JSON output
p.info().json()
```

As executable (output YAML style)
```
cd pythoninfo && python pythoninfo.py
```

Example YAML style output:
```
System:
  Net Info:
    - host_alias = 
    - hostname = XXXX.local
    - ip_address = 192.168.1.167
    - ip_address_alternate = 
  Time Info:
    - Epoch Time = 1403258818.62
    - Local Time = 2014-06-20 18:06:58
    - ctime = Fri Jun 20 18:06:58 2014
    - Timezone name = ('xxx', 'xxx')
    - datetime = 2014-06-20 18:06:58.616000
    - Daylight = 0
    - UTC Time = 2014-06-20 10:06:58
  Sys Info:
    - sys.path = C:\Users\user\pythoninfo\pythoninfo;C:\Python27\lib\site-packages\pip-1.4.1-py2.7.egg
    - platform.uname = Windows, XXXX, 7, 6.1.7601, AMD64, Intel64 Family 6 Model 45 Stepping 7, GenuineIntel
    - platform.platform = Windows-7-6.1.7601-SP1
    - os.sys.getcheckinterval = 100
    - os.sys.getrecursionlimit = 1000
    - sys.prefix = C:\Python27
    - os.sys.getdefaultencoding = ascii
    - sys.platform = win32
    - os.sys.getwindowsversion = sys.getwindowsversion(major=6, minor=1, build=7601, platform=2, service_pack='Service Pack 1')
    - os.sys.getprofile = None
    - os.sys.getfilesystemencoding = mbcs
    - sys.version (Python Version) = 2.7.5 (default, May 15 2013, 22:43:36) [MSC v.1500 32 bit (Intel)]
    - sys.executable (Python bin) = C:\Python27\python.exe
    - os.sys.gettrace = None
    - os.getcwdu = C:\Users\user\pythoninfo\pythoninfo
    - os.getpid = 7256
    - os.getcwd = C:\Users\user\pythoninfo\pythoninfo
```

Build
-----
```
$> python setup.py build_py
```

Package
-------
```
$> python setup.py sdist
```

Test
----
* Required nosetests
```
$> nosetests
```