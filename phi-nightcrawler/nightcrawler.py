import os, logging, time, shutil
import paramiko
from shutil import copyfile

sftp_info = {
    'host': os.getenv('SFTP_HOST'),
    'user': os.getenv('SFTP_USER'),
    'password': os.getenv('SFTP_PASS'),
    'port': int(os.getenv('SFTP_PORT'))
}

phi_columns = os.getenv('PHI_COLUMNS')

 
def connect(creds):
        host = creds['host']
        user = creds['user']
        password = creds['password']
        port = creds['port']
        remote_path = os.getenv('')
        local_path = './test2.txt'

        logging.info(f"Connecting to host: {host} on port: {port}")

        if port is None:
            transport = paramiko.Transport((host), default_window_size=paramiko.common.MAX_WINDOW_SIZE, default_max_packet_size=3276800)
        else:
            transport = paramiko.Transport((host, port), default_window_size=paramiko.common.MAX_WINDOW_SIZE, default_max_packet_size=3276800)
    
        transport.connect(username=user, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)

        try:
            with sftp.open(remote_path, 'rb') as remote:
                start = time.time()
                with open(local_path, 'wb') as local:
                    shutil.copyfileobj(remote, local)
                end = time.time()
                logging.debug(f'It took {end - start} seconds to move {remote_path} to {local_path}')
        except Exception as e: 
            print(e)


connect(sftp_creds)

# def __run__(sftp_creds, phi_columns, directory, notification_emails):
#         with (connect_to_server, sftp_creds) as sftp_srv:
#             files = crawl_dir(directory)
#             bad_dir=create_bad_files_directory(directory)
#             for f in files:
#                 with open('temp_file', 'rw') as temp_f:
#                     sftp_srv.copy(f, temp_f)
#                     has_phi=scan_for_phi(temp_f,phi_columns)
#                     if has_phi:
#                             move_to_bad_dir(f, bad_dir)
#                             send_notifications(notification_emails)
