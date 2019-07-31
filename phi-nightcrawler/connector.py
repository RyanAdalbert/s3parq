import paramiko

class Connector():
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