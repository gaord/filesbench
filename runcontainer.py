import subprocess

# Define the number of containers to create
num_containers = 400

# Define the command to run inside each container
command = "mount -t ceph ceph-mon-0:/ /mnt/cephfs -o name=admin,secretfile=/etc/ceph/secret"

# Loop through and create the containers
for i in range(num_containers):
    # Define the container name
    container_name = "client{}".format(i)
    
    # Define the command to create the container
    create_command = "docker run -d --name {} myimage {}".format(container_name, command)
    
    # Run the command to create the container
    subprocess.run(create_command, shell=True)