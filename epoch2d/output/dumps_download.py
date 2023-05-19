import os
import paramiko
import logging
import stat

# Connection details

host = '147.156.161.158'
port = 22
user = 'Juan'
password = 'Nauj123!'

# Logging info

logging.getLogger("paramiko").setLevel(logging.WARNING)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Remote directory to download

remote_dir = '/home/Juan/simulations/aras_comparison'

# Local directory to download to

local_dir = '/home/juan/Documentos/GitHub/epoch/epoch2d/output/dumps/aras_comparison'

# Create SSH client object

def download_directory(remote_dir, local_dir, sftp):
    logging.info(f"Downloading directory {remote_dir} to {local_dir}")
    os.makedirs(local_dir, exist_ok=True)
    for filename in sftp.listdir(remote_dir):
        remote_path = f"{remote_dir}/{filename}"
        local_path = os.path.join(local_dir, filename)
        if stat.S_ISDIR(sftp.stat(remote_path).st_mode):
            download_directory(remote_path, local_path, sftp)
            logging.info(f"Downloaded directory {remote_path} to {local_path}")
        elif filename.endswith('.sdf'):
            sftp.get(remote_path, local_path)
            logging.info(f"Downloaded file {remote_path} to {local_path}")
        else:
            logging.info(f"Skipping file {remote_path}")


# Connect to the SSH server

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=host, port=port, username=user, password=password)

# Open an SFTP session

sftp = ssh.open_sftp()

# Download directories

download_directory(remote_dir, local_dir, sftp)

# Cloase the SFTP session and SSH connection

sftp.close()
ssh.close()

logging.info("Download complete.")