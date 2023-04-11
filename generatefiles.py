import os
import random

# Define counters for each file size category
bytes_count = 0
kb_count = 0
mb_count = 0

# Define the total number of files to be generated
num_files = 1000#1000000

# Define the total size of all files in bytes
total_size = 100000000#1000000000000

# Define the maximum number of files per directory
max_files_per_dir = 50 #5000

# Define the maximum directory depth
max_depth = 4

total_files_size = 0

# Define the list of file sizes to be randomly selected from
#file_sizes = [1, 1024, 1048576, random.randint(1048577, 104857600)]

def get_rand_file_sizes(bytes_prob, kb_prob, mb_prob):
    global bytes_count,kb_count,mb_count
    # Define the list of file size categories and their corresponding weights
    file_size_cats = [1, 1024, 1048576]
    weights = [bytes_prob, kb_prob, mb_prob]
    
    # Use random.choices() to generate a random file size category based on the weights
    file_size_cat = random.choices(file_size_cats, weights=weights)[0]
    
    # Generate a random file size within the selected category
    if file_size_cat == 1:
        file_size = random.randint(1, 1024)
        bytes_count += 1
    elif file_size_cat == 1024:
        file_size = random.randint(1025, 10240)
        kb_count +=1
    else:
        file_size = random.randint(10241, 104857600)
        mb_count +=1
    
    return file_size

# Define the function to generate a random directory path
def get_random_dir_path(root_dir, depth):
    if depth == 0:
        return root_dir
    else:
        dir_name = "dir_" + str(random.randint(1, max_files_per_dir))
        dir_path = os.path.join(root_dir, dir_name)
        os.makedirs(dir_path, exist_ok=True)
        return get_random_dir_path(dir_path, depth-1)

# Generate the files
for i in range(num_files):
    # Generate a random file size
    file_size = get_rand_file_sizes(0.5,0.4,0.1)#random.choice(file_sizes)
    total_files_size += file_size
    
    # Generate a random directory path
    dir_path = get_random_dir_path(".", random.randint(1, max_depth))
    
    # Generate a random file name
    file_name = "file_" + str(random.randint(1, max_files_per_dir)) + ".txt"
    
    # Generate the full file path
    file_path = os.path.join(dir_path, file_name)
    
    # Generate the file content
    file_content = os.urandom(file_size)
    
    # Write the file
    with open(file_path, "wb") as f:
        f.write(file_content)
    
    # Check if the total size limit has been reached
    if total_files_size >= total_size:
        break
# Calculate the percentage of files generated in each size category
total_files = bytes_count + kb_count + mb_count
bytes_percent = bytes_count / total_files * 100
kb_percent = kb_count / total_files * 100
mb_percent = mb_count / total_files * 100

# Print the results
print(f"Files generated in bytes: {bytes_percent:.2f}%")
print(f"Files generated in kilobytes: {kb_percent:.2f}%")
print(f"Files generated in megabytes: {mb_percent:.2f}%")
# The code generates random files and directories until the total size limit is reached or the number of files generated reaches the specified limit.
# To continue generating files and directories, simply run the script again.