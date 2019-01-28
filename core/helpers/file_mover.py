import paramiko
import stat
import os
from typing import NamedTuple
import re

class FileDestination(NamedTuple):
    regex: str
    file_type: str


class FileMover():
    def __init__(self,secret):
        user = secret.user
        password = secret.password
        host = secret.host
        port = secret.port
        mode = secret.mode
        self.transport = paramiko.Transport(host, port)
        self.transport.connect(username=user, password=password)
        self.sftp = paramiko.SFTPClient.from_transport(self.transport)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.sftp.close()
        self.transport.close()

    def get_file(self, remote_path: str, local_path: str):
        # Fetch file from remote
        #   Set local file time to match remote for comparison to S3 modified time
        utime = self.sftp.stat(remote_path).st_mtime
        self.sftp.get(remote_path, local_path)
        os.utime(local_path, (utime,utime))

    def get_file_type(self, filename, file_dest_map):
        # Check if file is matching to the prefix, otherwise don't move
        file_type = [x.file_type for x in file_dest_map if re.match(x.regex, filename)]
        if len(file_type) < 1:
            return 'dont_move'
        else:
            return file_type[0]

    def is_dir(self, remote_file) -> bool:
        # Return bool of if 'file' is a directory or not
        return stat.S_ISDIR(remote_file.st_mode)

    def list_files(self, sftp_prefix: str):
        # List all files on remote
        return self.sftp.listdir_attr(sftp_prefix)


def get_files(tmp_dir:str,prefix: str, remote_path: str, secret):
    # Set file filtering
    files_dest = [FileDestination(f"^{prefix}.*$","do_move")]

    # Open SFTP connection
    with FileMover(secret=secret) as fm:
        file_list = fm.list_files(remote_path)
        for remote_file in file_list:
            # For every "file" in the remote list, make sure its not a directory and matches filters
            if not (fm.is_dir(remote_file)) and (fm.get_file_type(remote_file.filename, files_dest)!='dont_move'):
                remote_file_path = remote_path + "/" + remote_file.filename
                # Set file name to include the path, in case of duplicate file names in different locations
                local_file_name = remote_file_path.replace("/",".")[1:]
                local_file_path = os.path.join(tmp_dir, local_file_name)
                
                fm.get_file(remote_file_path, local_file_path)
