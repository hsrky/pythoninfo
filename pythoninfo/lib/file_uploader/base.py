import logging
logging.basicConfig()

class Base(object):
    '''
    Base class for uploader
    '''
    configs = dict()

    def __del__(self):
        # destructor, clean up resources: close connection, etc
        pass
    
    def set_configs(self, configs):
        # set connection configurations
        self.configs.update(configs)
        
    def init(self):
        # do something like configurations verification, connect to server
        return dict(status=0, err_str='Not implemented')
    
    def extract_file_name(self, file_path):
        file_path = file_path.replace('\\', '/')
        return file_path.split('/').pop()
    
    def upload(self, local_path, remote_path, remote_path_is_dir=False):
        # do the actual uploading
        return dict(status=0, err_str='Not implemented')

