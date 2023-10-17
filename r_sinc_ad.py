import paramiko
import os
import time

# SSH connection parameters for the remote machine
remote_hostname = '172.26.74.230'
remote_port = 22
remote_username = 'pi_controller'
remote_password = 'energypilot'

folder_to_copy = 'ad' # # Sensores
#folder_to_copy = 'tc'# Temperaturas Matrices
#folder_to_copy = 'tc_matrix' # Temperaturas Camera



remote_source_folder = os.path.join("/opt/mequonic/energy-pilot/prod/sensors_backup/",folder_to_copy).replace("\\", "/")
local_destination_folder = os.path.join(os.path.dirname(__file__), "DATA",folder_to_copy).replace("\\", "/")

if not os.path.exists(local_destination_folder):
    os.makedirs(local_destination_folder)

# Create an SSH client for the remote machine
remote_ssh_client = paramiko.SSHClient()
remote_ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

def setup():
    global sftp
    try:
        # Connect to the remote machine using SSH
        remote_ssh_client.connect(hostname=remote_hostname, port=remote_port, username=remote_username,password=remote_password)
        if remote_ssh_client.get_transport() is not None:
            print("SSH connection is active.")

            sftp = remote_ssh_client.open_sftp()

            print("SFTP connection is active.")

        else:
            print("SSH connection is not active.")
    except paramiko.AuthenticationException:
            print("Authentication failed, please check your SSH credentials.")
    except paramiko.SSHException as e:
        print(f"SSH error: {str(e)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


setup()

while True:
    try:
       # List files in the remote source folder
        remote_files = sftp.listdir(remote_source_folder)
        #print(remote_files)

        if folder_to_copy == 'tc_matrix':
            latest_file = None
            latest_mtime = 0

            for remote_file in remote_files:
                try:
                    remote_file_path = os.path.join(remote_source_folder, remote_file).replace("\\", "/")
                    remote_file_stat = sftp.stat(remote_file_path)

                    # Check if this file is newer than the previous latest file
                    if remote_file_stat.st_mtime > latest_mtime:
                        latest_file = remote_file
                        latest_mtime = remote_file_stat.st_mtime
                except:

                    pass

            if latest_file:
                remote_file_path = os.path.join(remote_source_folder, latest_file).replace("\\", "/")
                local_file_path = os.path.join(local_destination_folder, 'matrix_camera.txt').replace("\\", "/")
                try:
                    # Check if the local file does not exist or the remote file is newer
                    if (not os.path.exists(local_file_path) or latest_mtime > os.path.getmtime(local_file_path)):
                        sftp.get(remote_file_path, local_file_path.replace("/", "\\\\").replace("\\", "\\\\"))
                        print(f"Copied {latest_file} to local destination.")
                except:
                    print("ERROR Time")
                    pass

        else:
        # Delete local files not present in remote_files
            for local_file in os.listdir(local_destination_folder):
                try:
                    local_file_path = os.path.join(local_destination_folder, local_file)
                    #print(local_file_path)
                    # Check if the local file is not in remote_files
                    if local_file not in remote_files:
                        os.remove(local_file_path)
                        print(f"Deleted {local_file} from local destination.")
                except:
                    pass
            for remote_file in remote_files:
                try:
                    remote_file_path = os.path.join(remote_source_folder, remote_file).replace("\\", "/")
                    local_file_path = os.path.join(local_destination_folder, remote_file).replace("\\", "/")

                    # Check if the local file does not exist or the remote file is newer
                    #print(local_file_path)
                    if not os.path.exists(local_file_path) or sftp.stat(remote_file_path).st_mtime > os.path.getmtime(local_file_path) or sftp.stat(remote_file_path).st_size != os.path.getsize(local_file_path):
                        sftp.get(remote_file_path, local_file_path.replace("\\", "\\\\"))
                        print(f"Copied {remote_file} to local destination.")
                except:
                    try:
                        sftp.get(remote_file_path, local_file_path.replace("\\", "\\\\"))
                    except:
                        print("Error in ", remote_file)
                        pass
    except:
        try:
            setup()
        except:
            print("ERROR CONNECTION")
            pass
