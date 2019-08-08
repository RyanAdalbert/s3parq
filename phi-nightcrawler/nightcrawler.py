import os, logging, shutil, sys
import paramiko
from shutil import copyfile
from stat import S_IWUSR, S_IWGRP, S_IWOTH

sftp_info = {
    'host': os.getenv('SFTP_HOST'),
    'user': os.getenv('SFTP_USER'),
    'password': os.getenv('SFTP_PASS'),
    'port': int(os.getenv('SFTP_PORT'))
}

phi_dir = os.getenv('PHI_DIR')


def nightcrawler(creds, new_dir):
        host = creds['host']
        user = creds['user']
        password = creds['password']
        port = creds['port']
        logging.info(f"Connecting to host: {host} on port: {port}")

        print('1')
        if port is None:
            transport = paramiko.Transport((host), default_window_size=paramiko.common.MAX_WINDOW_SIZE, default_max_packet_size=3276800)
        else:
            transport = paramiko.Transport((host, port), default_window_size=paramiko.common.MAX_WINDOW_SIZE, default_max_packet_size=3276800)
        print('2')
        transport.connect(username=user, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        print('3')
        try:
            sftp.mkdir(new_dir, mode=777)
            print('4')
        except Exception as e: 
            logging.error(e)
            raise e

nightcrawler(sftp_info, phi_dir)
