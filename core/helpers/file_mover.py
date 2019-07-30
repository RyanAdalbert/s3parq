import os, paramiko, re, stat
from core.secret import Secret
from typing import NamedTuple
from core.raw_contract import RawContract
import time
from core.logging import LoggerMixin, get_logger
import shutil

class FileDestination(NamedTuple):
    regex: str
    file_type: str

class FileMover(LoggerMixin):
    """ Organizes the common methods used to retrieve and push files. 
    """
    def __init__(self, secret: Secret):
        user = secret.user
        password = secret.password
        host = secret.host
        port = secret.port
        mode = secret.mode
        self.logger.debug(f"Connecting to host: {host} on port: {port}")
        
        if port is None:
            self.transport = paramiko.Transport((host), default_window_size=paramiko.common.MAX_WINDOW_SIZE, default_max_packet_size=3276800)
        else:
            self.transport = paramiko.Transport((host, port), default_window_size=paramiko.common.MAX_WINDOW_SIZE, default_max_packet_size=3276800)
        
        self.transport.connect(username=user, password=password)
        self.sftp = paramiko.SFTPClient.from_transport(self.transport)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.sftp.close()
        self.transport.close()

    def get_raw_file(self, remote_path: str, local_path: str):
        """
        Fetch a file from a remote SFTP server and move it to a specified local directory.
        :param remote_path: The full path of the remote file
        :param local_path: The full path of the local file
        """
        # Set local file time to match remote for comparison to S3 modified time
        utime = self.sftp.stat(remote_path).st_mtime 
        try:
            with self.sftp.open(remote_path, 'rb') as remote:
                start = time.time()
                with open(local_path, 'wb') as local:
                    shutil.copyfileobj(remote, local)
                end = time.time()
                self.logger.debug(f'It took {end - start} seconds to move {remote_path} to {local_path}')
        except Exception as e: 
            print(e)
        os.utime(local_path, (utime,utime))

    def put_file(self, remote_path: str, local_path: str):
        self.sftp.put(localpath=local_path, remotepath=remote_path)

    def get_file_type(self, filename: str, file_dest_map: str):
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

logger = get_logger("file_mover")

def list_remote_files(remote_path: str, secret: Secret):
    """
    Generates a list of the files located in the remote path. Allows this list to be accessed in notebook with function call
    :param remote_path: The full path of the remote file
    :param secret: Authentication object 
    :returns: A list of files in the remote path
    """
    # Open SFTP connection
    with FileMover(secret=secret) as fm:
        file_list = fm.list_files(remote_path)
        return file_list

def get_file(tmp_dir: str, prefix: str, remote_path: str, remote_file: str, secret: Secret):
    """
    SFTPs a single file from the remote dir to the local dir given the correct file prefix
    :param tmp_dir: The local path
    :param prefix: Prefix of the file that needs to be moved
    :param remote_path: The full path of the remote file
    :param remote_file: The name of the remote file
    :param secret: Authentication object
    """
    # Set file filtering
    files_dest = [FileDestination(f"^{prefix}.*$","do_move")]

    # Open SFTP connection
    with FileMover(secret=secret) as fm:
        # For every "file" in the remote list, make sure its not a directory and matches filters
        if not (fm.is_dir(remote_file)) and (fm.get_file_type(remote_file.filename, files_dest)!='dont_move'):
            remote_file_path = remote_path + "/" + remote_file.filename
            # Set file name to include the path, in case of duplicate file names in different locations
            local_file_name = remote_file_path.replace("/",".")
            local_file_name = local_file_name.lstrip(".")
            local_file_path = os.path.join(tmp_dir, local_file_name)
            fm.get_raw_file(remote_file_path, local_file_path)

def get_files(tmp_dir: str, prefix: str, remote_path: str, secret: Secret):
    """
    SFTPs multiple files from the remote dir to the local dir given the correct file prefix
    :param tmp_dir: The local path
    :param prefix: Prefix of the files that needs to be moved
    :param remote_path: The full path of the remote files
    :param secret: Authentication object
    """
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
                local_file_name = remote_file_path.replace("/",".")
                local_file_name = local_file_name.lstrip(".")
                local_file_path = os.path.join(tmp_dir, local_file_name)
                fm.get_raw_file(remote_file_path, local_file_path)

def publish_file(local_path: str, remote_path: str, secret: Secret):
    # Open SFTP connection
    with FileMover(secret=secret) as fm:
        local_file = os.path.basename(local_path)
        remote_files = set()
        for file in fm.list_files(remote_path):
            remote_files.add(file.filename)
        if local_file in remote_files: # we don't want to overwrite any existing files on external FTP
            logger.debug("Error: File already exists on remote FTP server.")
            raise ValueError("Error: File already exists on remote FTP server.")
        remote_file = remote_path + "/" + local_file
        fm.put_file(remote_path=remote_file, local_path=local_path)