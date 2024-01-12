#!/bin/bash
# Check if the directory path argument is provided
if [ $# -eq 0 ]; then
    echo "No Arguments provided"
    exit 1
fi

if [ "$#" -ne 2 ]; then
    echo "Script expects two arguments but only one was provided"
    exit 1
fi

# Input directory path
input_directory="$1"

# Check if the input is a directory
if [ ! -d "$input_directory" ]; then
    echo "Error: '$input_directory' is not a directory."
    exit 1
fi

# Get the current date
current_date=$(date +"%Y_%m_%d")

# Backup file name with current date
backup_filename="backup_${current_date}.tar.gz"

# Backup location
backup_location="$2" 

# Check if the backup is a directory
if [ ! -d "$backup_location" ]; then
    echo "Error: '$backup_location' is not a directory."
    exit 1
fi

# Create a compressed backup of the entire directory
tar -czf "${backup_location}/${backup_filename}" -C "$(dirname "$input_directory")" "$(basename "$input_directory")"

echo "Backup completed. The backup file is stored as: ${backup_location}/${backup_filename}"
