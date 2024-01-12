#!/bin/bash

# Check for the number of arguments passed
if [ "$#" -ne 1 ]; then
    echo "Error !! No file name provided"
    exit 1
fi

# fetch and assign filename
log_filename=$1

# !!!!!! Very Important !!!!!!
# g++ server.cpp -o server
# g++ client_file_arg.cpp -o client_arg

# Run the server in background and append its output to the log file
echo "Script started"
echo "Please note !! You wont able to see the client and server console output, As the script is redirecting the output to log file"
./server >> "$log_filename" 2>&1 &
echo "Initiated ./server"
# Wait for the server to start
sleep 2

# List of input files
input_files=("hw6input.txt" "input1.txt" "input2.txt")

# Loop through the input files and run the client for each file
for input_file in "${input_files[@]}"; do
    # Run the client with the current input file and append its output to the same log file
    echo "Running test for $input_file"
    ./client_arg "$input_file" >> "$log_filename" 2>&1
done

echo "Test completed."
