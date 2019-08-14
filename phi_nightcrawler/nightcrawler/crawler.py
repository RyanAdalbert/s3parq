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
    
    # Check if Directory Exists
    def dir_exists(self, path):
        try:
            self.sftp.stat(path)
            return True
        except FileNotFoundError:
            return False

    # Create new_dir if does not exist
    def create_new_dir(self, sftp, new_dir):
        try:
            if self.dir_exists(new_dir):
                logging.info(f"Directory {new_dir} Already Exists")
            else:
                self.sftp.mkdir(new_dir, mode=777)
                logging.info(f"Directory {new_dir} Created")
        except Exception as e: 
            logging.error(e)
            raise e
