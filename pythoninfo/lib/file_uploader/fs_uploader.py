import logging

from base import Base as Uploader

log = logging.getLogger(__name__)

class FSUploader(Uploader):
    '''
    File System File handler, copy file from one path to another
    '''
    def init(self):
        return dict(status=1, err_str='')
    
    def upload(self, local_path, remote_path, remote_path_is_dir=False):
        import os
        import errno
        import shutil
        
        # change windows style to unix style
        remote_path = remote_path.replace('\\', '/')
        
        if remote_path_is_dir:
            remote_dir = remote_path
            filename = self.extract_file_name(local_path)
            remote_path = os.path.join(remote_path, filename)
        else:
            remote_dir = remote_path.split('/')
            remote_dir.pop()
            remote_dir = '/'.join(remote_dir)
        
        if not os.path.isdir(remote_dir):
            try:
                os.makedirs(remote_dir)
            except OSError as exc:
                if exc.errno == errno.EEXIST and os.path.isdir(remote_dir):
                    pass
                else:
                    log.error('Failed to create folder: "{0}"'.format(remote_dir))
                    return dict(status=0, err_str='Failed to create folder on remote path'.format(remote_dir))

        # do the file copying
        try:
            shutil.copy(local_path, remote_path)
        except:
            log.error('Failed to copy file "{0}" to "{1}"'.format(local_path, remote_path))
            return dict(status=0, err_str="Failed to copy to remote path.")
        
        return dict(status=1, err_str='')