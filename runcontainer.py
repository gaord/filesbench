import subprocess

# create 400 directories under /mnt
for i in range(1, 401):
    os.makedirs(f"/mnt/dir_{i}")

# mount cephfs file system on each directory
for i in range(1, 401):
    os.system(f"mount -t ceph 10.209.241.165:6789:/volumes/testbench/smallfiles /mnt/dir_{i} -o secret=QVFDdWp6TmtIWCtUTkJBQVZXM2d0WHFqVEYvTXhCSmE3UnlCTlE9PQ==,name=admin")

# run specified python script on each mounted directory
for i in range(1, 401):
#    os.system(f"python3 randrwbench.py /mnt/dir_{i}/10f53653-b7fe-4fd3-9288-c152a0c076fb/20w50g4d")
#异步模拟多客户端访问
    process = subprocess.Popen(["python3", "randrwbench.py", "--working_dir", "/mnt/dir_{}/10f53653-b7fe-4fd3-9288-c152a0c076fb/20w50g4d".format(i)])
