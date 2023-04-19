import subprocess
import random
import os

ceph_mon_ip = "10.209.241.165:6789"
ceph_secret = "QVFDdWp6TmtIWCtUTkJBQVZXM2d0WHFqVEYvTXhCSmE3UnlCTlE9PQ=="
ceph_user = "admin"
cephfs_path = "/volumes/testbench/smallfiles"
mount_path = "/mnt/dir_"
root_dir = "/mnt/dir_1/10f53653-b7fe-4fd3-9288-c152a0c076fb/20w50g4d"
num_mounts = 401

def create_dir_mount(ceph_mon_ip, ceph_secret, ceph_user, cephfs_path, mount_path):
     # create num_mounts directories under /mnt
    for i in range(1, num_mounts):
        os.makedirs(f"{mount_path}{i}")
    
    # mount cephfs file system on each directory
    for i in range(1, num_mounts):
        os.system(f"mount -t ceph {ceph_mon_ip}:{cephfs_path} {mount_path}{i} -o secret={ceph_secret},name={ceph_user}")        

def remove_dir_mount(mount_path):
    for i in range(1, num_mounts):
        os.system(f"umount {mount_path}{i}")
        os.rmdir(f"{mount_path}{i}")

create_dir_mount(ceph_mon_ip, ceph_secret, ceph_user, cephfs_path, mount_path)

files = os.listdir(root_dir)
    
    # Get the relative paths of the files and directories
relative_paths = [os.path.join(root_dir, f) for f in files]

    # Filter out the directories
directories = [f for f in relative_paths if os.path.isdir(f)]

selected_directories = random.sample(directories, num_mounts)

# run specified python script on each mounted directory
for i in range(1, num_mounts):
    #异步模拟多客户端访问
    cmd_to_run = ["python3", "randrwbench.py", "--sample_rate", "1.0", "--working_dir", "{}{}/10f53653-b7fe-4fd3-9288-c152a0c076fb/20w50g4d/{}".format(mount_path, i, os.path.basename(selected_directories[i-1]))]
    process = subprocess.Popen(cmd_to_run)

remove_dir_mount(mount_path)