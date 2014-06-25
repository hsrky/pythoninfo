import logging

from fs_uploader import FSUploader
from ftp_uploader import FtpUploader
from sftp_uploader import SFtpUploader

log = logging.getLogger(__name__)

class FileUploader(object):
    '''
    Class to handle remote file upload
    Usage: 
    f = FileUploader(@configs)
    result = f.connect()
    if result.status == 1:
        result = f.upload('local path', 'remote path')
        result = f.upload('local path 2', 'remote path 2')
        ...
    
    @configs {dict} - some settings may be optional depends on protocol
        `username' {string} username to login to remote server
        `password' {string} password to login to remote server
        `protocol' {string} transfer method, supports: 'sftp', 'ftp', 'file_system' (default)
        `host' {string} url of remote server
        `port' {int} port of remote server, default port of protocol if no value provided
        `connect_retry' {int} retry connect count in case failed to connect
        `connect_retry_wait' {int} in seconds, time to wait before next connection retry
        `connect_timeout' {int} in seconds, maximum connect time for each attempt
        `upload_retry' {int} retry upload count in case failed to upload
        `upload_retry_wait' {int} in seconds, time to wait before try to upload again
    '''
    uploader = None
    configs = dict( username='',
                    password='',
                    protocol='file_system',
                    host='',
                    port=None,
                    connect_retry=3,
                    connect_retry_wait=5,
                    connect_timeout=60,
                    upload_retry=3,
                    upload_retry_wait=5)
    
    def __init__(self, configs):
        '''
        Construtor
        '''
        self.configs.update(configs) # override user's config with our defaults
    
    def connect(self):
        '''
        connect to remote server
        @return dict() - 
            `status' {int} 1 on success
            `err_str' {string} text that desc error
        '''
        protocol = self.configs['protocol']
        if(protocol == 'ftp'):
            self.uploader = FtpUploader()
        elif(protocol == 'sftp'):
            self.uploader = SFtpUploader()
        elif(protocol == 'file_system'):
            self.uploader = FSUploader()
        else:
            pass
        
        if not self.uploader:
            return dict(status=0, err_str='Transfer protocol "{}" not supported'.format(protocol))
        
        self.uploader.set_configs(self.configs)
        result = self.uploader.init()
        
        if result['status'] == 0:
            # failed to init the uploader
            self.uploader = None
            return result
        
        return result
    
    
    def upload(self, local_path, remote_path, remote_path_is_dir=False):
        '''
        Upload file from `local_path' to `remote_path'
        @remote_path_is_dir True to indicate the remote_path is dir
        @return dict() -
            `status' {int} 1 on success
            `err_str' {string} text that desc error
        '''
        if not self.uploader:
            return dict(status=0, err_str='Connection not established.')
        
        return self.uploader.upload(local_path, remote_path, remote_path_is_dir)