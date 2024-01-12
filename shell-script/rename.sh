#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -lt 2 ]; then
	echo "Script expects 2 arguments: path_to_dir prefix : missing arguments "
    exit 1
fi

# Directory path
directory_path="$1"

# Prefix
prefix="$2"

# Check if the directory exists
if [ ! -d "$directory_path" ]; then
    echo "Error: Directory '$directory_path' not found."
    exit 1
fi

# Check if a prefix is provided
if [ -z "$prefix" ]; then
    echo "Error: No prefix provided."
    exit 1
fi

# Navigate to the directory
cd "$directory_path" || exit 1

# Rename files by adding the prefix
for file in *; do
    if [ -f "$file" ]; then
        new_name="${prefix}_${file}"
        mv "$file" "$new_name"
        echo "Renamed: $file to $new_name"
    fi
done

echo "File renaming completed with prefix '$prefix'"
