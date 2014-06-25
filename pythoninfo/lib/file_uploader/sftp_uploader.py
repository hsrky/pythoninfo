import time
import logging

from base import Base as Uploader

log = logging.getLogger(__name__)

class SFtpUploader(Uploader):
    '''
    SFTP Upload handler, see parent class for more info
    '''
    default_port = 22
    connect_attempt_count = 0
    upload_attempt_count = 0
    sftp = None
    ssh_client = None
    def _cleanup(self):
        if self.sftp:
            self.sftp.close()
            
        if self.ssh_client:
            self.ssh_client.close()
            
    def __del__(self):
        self._cleanup()
            
    def _connect(self, paramiko):
        self._cleanup()
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        self.ssh_client.connect(hostname=self.configs['host'],
                                port=self.configs['port'],
                                username=self.configs['username'], 
                                password=self.configs['password'],
                                timeout=self.configs['connect_timeout'])
        
        self.sftp = self.ssh_client.open_sftp()
        
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
                self.sftp.lstat(path)
            except:
                # lstat raise ERROR when path is not found, then we create the path!
                log.info('Remote path "{0}" not exists, create it.'.format(path))
                self.sftp.mkdir(path)
    
    def init(self):
        if not self.configs['port']:
            self.configs['port'] = 22

        #print 'Configs for SFTP:', self.configs
        
        result = dict(status=1, err_str='')
        
        try:
            import paramiko
        except ImportError:
            result['status'] = 0
            result['err_str'] = 'Init error: Required package "paramiko" is not installed.'
            log.warn(result['err_str'])
            return result
        
        while True:
            self.connect_attempt_count += 1
            connected = False
            try:
                self._connect(paramiko)
                connected = True
            except:
                log.warn('Failed to connect to server on attempt #{0}.'.format(self.connect_attempt_count))

            if connected or self.connect_attempt_count > self.configs['connect_retry']:
                # stop trying if connected or exceed max attempt count
                break
            else:
                time.sleep(self.configs['connect_retry_wait'])
                
        return result
    
    def upload(self, local_path, remote_path, remote_path_is_dir=False):
        '''
        Upload file from @local_path to @remote_path
        @remote_path_is_dir {boolean}  if remote_path is directory path (not file path), 
                                        set this argument to True. This will create only 
                                        empty directory in remote server
        @return dict():
            - `status' 1 if success, other number indicated error
            - `err_str' error string
        '''
        log.info('Upload file from "{0}" to "{1}"'.format(local_path, remote_path))
        self.upload_count = 0 #reset
        
        #print self.sftp.listdir()
        if not self.sftp:
            return dict(status=0, err_str='Connection not established.')
        
        if remote_path_is_dir:
            # already a dir path
            remote_dir = remote_path
            remote_filename = self.extract_file_name(local_path)
        else:
            remote_dir = remote_path.split('/')
            remote_filename = remote_dir.pop()
            remote_dir = '/'.join(remote_dir)
        
        log.info('remote dir: "{0}", remote file name: "{1}"'.format(remote_dir, remote_filename))
        try:
            self._mkdirs(remote_dir)
            if local_path and remote_filename:
                self.sftp.chdir(remote_dir)
                # TODO retry
                self.sftp.put(local_path, remote_filename)
        except:
            log.warn('Failed to copy file "{0}" to remote path: "{1}"'.format(local_path, remote_path))
            return dict(status=0, err_str='Failed to copy file to remote path.')
        
        return dict(status=1, err_str='')