import os
import paramiko

sftp_creds = {
    'host': os.getenv('SFTP_HOST'),
    'user': os.getenv('SFTP_USER'),
    'password': os.getenv('SFTP_PASS'),
    'port': os.getenv('SFTP_PORT') 
}

phi_columns = os.getenv('PHI_COLUMNS')

print(sftp_creds)
print(phi_columns)


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
