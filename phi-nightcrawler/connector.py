import os, logging
import paramiko

class Connector:


    def __init__(self, host, user, password, port):
        host = host
        user = user
        password = password
        port = port
        self.logging.info(f"Connecting to host: {host} on port: {port}")
    
        if port is None:
            self.transport = paramiko.Transport((host), default_window_size=paramiko.common.MAX_WINDOW_SIZE, default_max_packet_size=3276800)
        else:
            self.transport = paramiko.Transport((host, port), default_window_size=paramiko.common.MAX_WINDOW_SIZE, default_max_packet_size=3276800)
    
        self.transport.connect(username=user, password=password)
        self.sftp = paramiko.SFTPClient.from_transport(self.transport)

