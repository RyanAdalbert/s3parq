import os, logging, shutil, sys
import paramiko
from shutil import copyfile
from stat import S_IWUSR, S_IWGRP, S_IWOTH

# Set loggin level
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

class Nightcrawler:

    # Define env variables, initial set up
    def __init__(self, creds):
        host = creds['host']
        user = creds['user']
        password = creds['password']
        port = creds['port']
        logging.info(f"Connecting to host: {host} on port: {port}")

        # Create paramiko SFTP client object
        if port is None:
            self.transport = paramiko.Transport((host), default_window_size=paramiko.common.MAX_WINDOW_SIZE, default_max_packet_size=3276800)
        else:
            self.transport = paramiko.Transport((host, port), default_window_size=paramiko.common.MAX_WINDOW_SIZE, default_max_packet_size=3276800)

        self.transport.connect(username=user, password=password)
        self.sftp = paramiko.SFTPClient.from_transport(self.transport)



    # Check if remote directory exists
    def remote_dir_exists(self, path):
        try:
            self.sftp.stat(path)
            return True
        except FileNotFoundError:
            return False

    # Create remote_dir if does not exist
    def create_remote_dir(self, sftp, remote_dir):
        try:
            if self.remote_dir_exists(remote_dir):
                logging.info(f"Directory {remote_dir} Already Exists On SFTP Server")
            else:
                self.sftp.mkdir(remote_dir, mode=777)
                logging.info(f"Directory {remote_dir} Created On SFTP Server")
        except Exception as e: 
            logging.error(e)
            raise e


    # Check if temp_dir exists
    def temp_dir_exists(self, path):
        try:
            os.path.exists(path)
        except FileNotFoundError:
            return False

    # Create local temp_dir if does not exist, move files to temp dir, start crawl
    def crawl_files(self, sftp, remote_dir):
        # Create local temp_dir if does not exist
        # try:
        #     if self.temp_dir_exists(temp_dir):
        #         logging.info(f"Directory {temp_dir} Already Exists Locally")
        #     else:
        #         os.mkdir(temp_dir)
        #         logging.info(f"Directory {temp_dir} Created Locally")
        # except Exception as e: 
        #     logging.error(e)
        #     raise e

        # Get list of file names in remote dir
        # file_list = self.sftp.listdir(remote_dir)
        # print(file_list)


        # Open test file, write to it
        test_file = self.sftp.file('/upload/nightcrawler-test/test_file.py')

        test_file.write("Guy has on 3 pairs of sunglasses")

        #Use list of names to open files and crawl for phi
