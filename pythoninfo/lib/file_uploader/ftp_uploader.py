import logging

from base import Base as Uploader

log = logging.getLogger(__name__)

class FtpUploader(Uploader):
    '''
    FTP Upload handler, see parent class for more info
    '''
    default_port = 21
    ftp = None
    def __del__(self):
        if self.ftp:
            try:
                self.ftp.quit()
                self.ftp.close()
            except:
                log.info('Error when closing FTP connection, ignore this error.')
                #ignore error, no need to handle and we can't handle even if we wanted
    def _mkdirs(self, remote_dir):
        '''
        Create all parent dirs
        '''
        paths = remote_dir.split('/') # ['', 'home', 'user', 'dir', 'dir2', 'dir3', '']
        total_paths = len(paths)
        current_path_index = 1
        while total_paths > current_path_index:
            current_path_index = current_path_index + 1
            path = '/'.join(paths[0: current_path_index])
            try:
                self.ftp.cwd(path)
            except:
                # cwd raise ERROR when path is not found, then we create the path!
                log.info('Remote path "{0}" not exists, create it.'.format(path))
                self.ftp.mkd(path)

    def init(self):
        from ftplib import FTP
        if not self.configs['port']:
            self.configs['port'] = self.default_port
            
        self.ftp = FTP()
        
        retry_count = 0
        while True:
            if retry_count > self.configs['connect_retry']:
                return dict(status='0', err_str='Failed to connect to FTP Server: "{0}:{1}" after {2} attempts'.format(self.configs['host'], self.configs['port'], retry_count))
            
            try:
                self.ftp.connect(self.configs['host'], self.configs['port'], self.configs['connect_timeout'])
            except:
                self.ftp = None
                log.warn('Failed to connect to FTP Server: "{0}:{1}"'.format(self.configs['host'], self.configs['port']))
                retry_count = retry_count + 1
                continue
            
            # no exception, mean connected!
            break

        if self.configs['username']:
            try:
                self.ftp.login(self.configs['username'], self.configs['password'])
            except:
                log.warn('Failed to login to FTP server "{0}" using username: "{1}" and password: "{2}"'.format(self.configs['host'], self.configs['username'], self.configs['password']))
                return dict(status=0, err_str='Failed to login to FTP Server "{0}", check credential or FTP server settings.'.format(self.configs['host']))
        else:
            #anonymous
            try:
                self.ftp.login()
            except:
                log.warn('Failed to login to FTP server "{0}" anonymously.'.format(self.configs['host']))
                return dict(status=0, err_str='Failed to login to FTP server "{0}" anonymously.'.format(self.configs['host']))

        return dict(status=1, err_str='')
    
    def upload(self, local_path, remote_path, remote_path_is_dir=False):
        filename = ''
        if remote_path_is_dir:
            remote_dir = remote_path
            filename = self.extract_file_name(local_path)
        else:
            remote_dir = remote_path.split('/')
            filename = remote_dir.pop()
            remote_dir = '/'.join(remote_dir)
        
        try:
            self._mkdirs(remote_dir)
        except:
            log.error('Failed to create folder: "{0}"'.format(remote_dir))
            return dict(status=0, err_str='Failed to create folder on remote path'.format(remote_dir))
        
        # TODO upload retry
        try:
            self.ftp.cwd(remote_dir)
            with open(local_path, 'rb') as file:
                self.ftp.storbinary('STOR {0}'.format(filename), file)
        except:
            log.error('Error happens when copying file "{0}" to "{1}"'.format(local_path, remote_path))
            return dict(status=0, err_str="Failed to copy file to remote path.")
        
        return dict(status=1, err_str='')