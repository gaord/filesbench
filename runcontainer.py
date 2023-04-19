import subprocess
import random
import os

# Set the IP address and port of the Ceph monitor
ceph_mon_ip = "10.209.241.165:6789"

# Set the secret key for the Ceph user
ceph_secret = "QVFDdWp6TmtIWCtUTkJBQVZXM2d0WHFqVEYvTXhCSmE3UnlCTlE9PQ=="

# Set the username for the Ceph user
ceph_user = "admin"

# Set the path to the CephFS volume
cephfs_path = "/volumes/testbench/smallfiles"

# Set the base mount path for the directories
mount_path = "/mnt/dir_"

# Set the root directory for the files
root_dir = "/mnt/dir_1/10f53653-b7fe-4fd3-9288-c152a0c076fb/20w50g4d"

# Set the number of mount points to create
num_mounts = 401

def create_dir_mount(ceph_mon_ip, ceph_secret, ceph_user, cephfs_path, mount_path):
    # Create num_mounts directories under /mnt
    for i in range(1, num_mounts):
        os.makedirs(f"{mount_path}{i}")
    
    # Mount CephFS file system on each directory
    for i in range(1, num_mounts):
        os.system(f"mount -t ceph {ceph_mon_ip}:{cephfs_path} {mount_path}{i} -o secret={ceph_secret},name={ceph_user}")        

def remove_dir_mount(mount_path):
    # Unmount and remove each directory
    for i in range(1, num_mounts):
        os.system(f"umount {mount_path}{i}")
        os.rmdir(f"{mount_path}{i}")

# Create the directories and mount the file system
create_dir_mount(ceph_mon_ip, ceph_secret, ceph_user, cephfs_path, mount_path)

# Get the list of files in the root directory
files = os.listdir(root_dir)
    
# Get the relative paths of the files and directories
relative_paths = [os.path.join(root_dir, f) for f in files]

# Filter out the directories
directories = [f for f in relative_paths if os.path.isdir(f)]

# Select a random sample of directories
selected_directories = random.sample(directories, num_mounts)

# Run specified Python script on each mounted directory
for i in range(1, num_mounts):
    # Asynchronously simulate multiple client accesses
    cmd_to_run = ["python3", "randrwbench.py", "--sample_rate", "1.0", "--working_dir", "{}{}/10f53653-b7fe-4fd3-9288-c152a0c076fb/20w50g4d/{}".format(mount_path, i, os.path.basename(selected_directories[i-1]))]
    process = subprocess.Popen(cmd_to_run)

# Remove the directories and unmount the file system
remove_dir_mount(mount_path)