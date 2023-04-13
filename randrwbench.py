import os
import json
import random
import time
import datetime
import struct
import threading
import argparse

# Define the function to read and write files
def read_write_file(file_path):
    # Get the file name and size
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)

    # Read the file and record the time
    start_time = time.time()
    with open(file_path, 'rb') as f:
        f.read()
    read_time = time.time() - start_time

    # Write to the file and record the time
    start_time = time.time()
    with open(file_path, 'ab') as f:
        f.write(struct.pack('f', random.random()))
    write_time = time.time() - start_time

    # Return the file information and read/write time
    return {
        'file_name': file_name,
        'file_path': file_path,
        'file_size': file_size,
        'read_time': read_time,
        'write_time': write_time
    }

# Define the function to get a list of all files in a directory and its subdirectories
def get_all_files(directory):
    # Initialize an empty list to store the file paths
    file_paths = []

    # Walk the directory tree and add the file paths to the list
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_paths.append(file_path)

    # Return the list of file paths
    return file_paths

# Define the function to run the read/write process for a directory
def run_process(directory):
    # Get all the files in the directory
    files = get_all_files(directory)#[os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    # Run the read/write process for each file
    results = []
    for file_path in files:
        result = read_write_file(file_path)
        results.append(result)

    # Calculate the max, min, and average read/write time
    read_times = [r['read_time'] for r in results]
    write_times = [r['write_time'] for r in results]
    max_read_time = max(read_times)
    min_read_time = min(read_times)
    avg_read_time = sum(read_times) / len(read_times)
    max_write_time = max(write_times)
    min_write_time = min(write_times)
    avg_write_time = sum(write_times) / len(write_times)

    
    # Store the results in the thread object
    thread = threading.current_thread()
    thread.result = {
        'directory': directory,
        'results': results,
        'max_read_time': max_read_time,
        'min_read_time': min_read_time,
        'avg_read_time': avg_read_time,
        'max_write_time': max_write_time,
        'min_write_time': min_write_time,
        'avg_write_time': avg_write_time
    }


# Define the function to run the read/write process for multiple directories concurrently
def run_processes_concurrently(directories):
    # Create a thread for each directory
    threads = []
    for directory in directories:
        thread = threading.Thread(target=run_process, args=(directory,))
        threads.append(thread)

    # Start all the threads
    for thread in threads:
        thread.start()

    # Wait for all the threads to finish
    for thread in threads:
        thread.join()

    # Get the results from each thread
    results = []
    for thread in threads:
        results.append(thread.result)

    # Get the current date and time
    now = datetime.datetime.now()
    
    # Format the date and time as a string
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    
    # Use the timestamp in the filename
    log_filename = f"performance_log_{timestamp}.json"

    # Write the results to a log file in JSON format
    with open(log_filename, 'w') as f:
        json.dump(results, f)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--working_dir', metavar='working_dir', type=str, help='the directory to process')
    args = parser.parse_args()

    # Get a list of all files and directories in the current directory
    files = os.listdir(args.working_dir)
    
    # Get the relative paths of the files and directories
    relative_paths = [os.path.join(args.working_dir, f) for f in files]

    # Filter out the directories
    directories = [f for f in relative_paths if os.path.isdir(f)]

    # Select 20% of the directories at random
    num_directories = len(directories)
    num_to_select = int(num_directories * 0.1)
    selected_directories = random.sample(directories, num_to_select)

    run_processes_concurrently(selected_directories)
