import os
from phi_nightcrawler.nightcrawler import Nightcrawler

# Set Environment Variables
sftp_info = {
    'host': os.getenv('SFTP_HOST'),
    'user': os.getenv('SFTP_USER'),
    'password': os.getenv('SFTP_PASS'),
    'port': int(os.getenv('SFTP_PORT'))
}

phi_dir = os.getenv('PHI_DIR')

# Run Crawl
crawler = Nightcrawler(sftp_info)
crawler.create_new_dir(sftp_info, phi_dir)