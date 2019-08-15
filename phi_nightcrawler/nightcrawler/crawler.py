import os, logging, shutil, sys
import paramiko
from shutil import copyfile
from stat import S_IWUSR, S_IWGRP, S_IWOTH

# Set loggin level
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

# Main Function
class Nightcrawler:
    def __init__(self, creds):
        host = creds['host']
        user = creds['user']
        password = creds['password']
        port = creds['port']
        logging.info(f"Connecting to host: {host} on port: {port}")

        # Create Paramiko Client Object
        if port is None:
            self.transport = paramiko.Transport((host), default_window_size=paramiko.common.MAX_WINDOW_SIZE, default_max_packet_size=3276800)
        else:
            self.transport = paramiko.Transport((host, port), default_window_size=paramiko.common.MAX_WINDOW_SIZE, default_max_packet_size=3276800)

        self.transport.connect(username=user, password=password)
        self.sftp = paramiko.SFTPClient.from_transport(self.transport)

    def crawl_files(self):
        temp_dir_path = 'phi_nightcrawler/tem_directory'
        # Create local temp directory
        os.mkdir(temp_dir_path)

    # Check if remote directory exists
    def dir_exists(self, path):
        try:
            self.sftp.stat(path)
            return True
        except FileNotFoundError:
            return False

    # Create remote_dir if does not exist
    def create_remote_dir(self, sftp, remote_dir):
        try:
            if self.dir_exists(remote_dir):
                logging.info(f"Directory {remote_dir} Already Exists")
            else:
                self.sftp.mkdir(remote_dir, mode=777)
                logging.info(f"Directory {remote_dir} Created")
        except Exception as e: 
            logging.error(e)
            raise e

 


    # with self.sftp