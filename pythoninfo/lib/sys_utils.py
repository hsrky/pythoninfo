import os
from net_utils import NetUtils
class SysUtils(object):
    @staticmethod
    def get_disk_usage(path, unit='bytes'):
        '''
        Get disk usage on `path'
        @path {string} full path to folder to check disk usage
        @unit {string: [bytes|GB|MB|KB]} convert disk usage to this unit
        return dict(free='xxx GB', total='xx GB', used='x GB')
        '''
        factor = 1
        if unit == 'GB':
            factor = 1024*1024*1024
        elif unit == 'MB':
            factor = 1024*1024
        elif unit == 'KB':
            factor = 1024
            
        free = 0; total = 0; used = 0;
        
        try:
            stat = os.statvfs(os_path)
            free = stat.f_bavail * stat.f_frsize
            total = stat.f_blocks * stat.f_frsize
            used = (stat.f_blocks - stat.f_bfree) * stat.f_frsize
        except:
            print('Unable to get disk usage for path "{}"'.format(os_path))
        
        return dict(free='{}{}'.format(free/factor, convert), 
                    total='{}{}'.format(total/factor, convert), 
                    used='{}{}'.format(used/factor, convert))
    
    @staticmethod
    def get_time_info():
        '''
        Get current time info
        return dict of time
        '''
        results = dict()
        from datetime import datetime
        import time
        try:
            results['datetime'] = str(datetime.now())
            results['Epoch Time'] = str(time.time())
            results['Local Time'] = str(datetime.fromtimestamp(time.mktime(time.localtime())))
            results['UTC Time'] = str(datetime.fromtimestamp(time.mktime(time.gmtime())))
            results['ctime'] = time.ctime()
            results['Daylight'] = time.daylight
            results['Timezone name'] = time.tzname
        except:
            print('Failed to get info on time.')
            
        return results
    
    @staticmethod
    def get_sys_info():
        '''
        Retrieve data from sys variable
        return dictionary of sys data
        '''
        
        results = dict()
        for func_name in dir(os):
            if func_name.startswith('get'):
                try:
                    value = getattr(os, func_name)()
                    results['os.{}'.format(func_name)] = str(value)
                except:
                    pass
        
        for func_name in dir(os.sys):
            if func_name.startswith('get'):
                try:
                    value = getattr(os.sys, func_name)()
                    results['os.sys.{}'.format(func_name)] = str(value)
                except:
                    pass
        

        import platform
        results['platform.uname'] = ', '.join(platform.uname())
        results['platform.platform'] = platform.platform()
        
        import sys
        results['sys.version (Python Version)'] = sys.version
        results['sys.platform'] = sys.platform
        results['sys.executable (Python bin)'] = sys.executable
        results['sys.prefix'] = sys.prefix
        results['sys.path'] = '<br/>\n'.join(sys.path)
        return results
    
    @staticmethod
    def get_package_info():
        '''
        Get all available python package information
        '''
        #TODO
        return dict(TODO='YET TO IMPLEMENT')
    
    @staticmethod
    def get_net_info():
        '''
        Get host information on current machine
        return dictionary of host information
        '''
        import socket
        results = dict()
        try:
            host_infos = socket.gethostbyaddr(socket.gethostname())
            results['hostname'] = host_infos[0]
            results['host_alias'] = ', '.join(host_infos[1])
            results['ip_address_alternate'] = ', '.join(host_infos[2])

            net_util = NetUtils(10)
            results['ip_address'] = net_util.get_host_ip()
        except:
            print('Failed to get net info')
            #print traceback.print_exc()
        return results