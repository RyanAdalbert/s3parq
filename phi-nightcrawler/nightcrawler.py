import os, logging, shutil, sys
import paramiko
from shutil import copyfile
from stat import S_IWUSR, S_IWGRP, S_IWOTH

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

sftp_info = {
    'host': os.getenv('SFTP_HOST'),
    'user': os.getenv('SFTP_USER'),
    'password': os.getenv('SFTP_PASS'),
    'port': int(os.getenv('SFTP_PORT'))
}

phi_dir = os.getenv('PHI_DIR')

def dir_exists(sftp, path):
    try:
        sftp.stat(path)
        return True
    except FileNotFoundError:
        return False

def nightcrawler(creds, new_dir):
        host = creds['host']
        user = creds['user']
        password = creds['password']
        port = creds['port']
        logging.info(f"Connecting to host: {host} on port: {port}")

        if port is None:
            transport = paramiko.Transport((host), default_window_size=paramiko.common.MAX_WINDOW_SIZE, default_max_packet_size=3276800)
        else:
            transport = paramiko.Transport((host, port), default_window_size=paramiko.common.MAX_WINDOW_SIZE, default_max_packet_size=3276800)

        transport.connect(username=user, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)

        try:
            if dir_exists(sftp, new_dir):
                logging.info(f"Directory {new_dir} Already Exists")
            else:
                sftp.mkdir(new_dir, mode=777)
                logging.info(f"Directory {new_dir} Created")
        except Exception as e: 
            logging.error(e)
            raise e

nightcrawler(sftp_info, phi_dir)
