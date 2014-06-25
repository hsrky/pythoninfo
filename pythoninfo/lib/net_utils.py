class NetUtils(object):
    time_out = 20 # 20 seconds timeout
    def __init__(self, time_out=None):
        if time_out:
            self.time_out = time_out

    def check_port(self, ip, port):
        '''
        return True if port is opened
        '''
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(self.time_out)
        result = -1 # unknown
        try:
            result = sock.connect_ex((str(ip), int(port)))
            sock.close()
        except:
            print('Failed to connect to {}:{} - '.format(ip, port))
            #print traceback.print_exc()
            sock.close()

        if result == 0:
            return True
        else:
            return False

    def get_host_ip(self):
        '''
        Get IP of current host that used to connect to internet
        '''
        host_ip = ''
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(self.time_out)
            try:
                sock.connect(('www.yahoo.com', 80))
                host_ip = sock.getsockname()[0]
                sock.close()
            except:
                sock.close()
        except:
            print('Failed to get host ip.')
        
        return host_ip