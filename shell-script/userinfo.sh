#!/bin/bash

# Check if the username argument is provided
if [ $# -ne 1 ]; then
    echo "No Arguments supplied, Please provide the username"
    exit 1
fi

# Get user information
username=$1
user_info=$(getent passwd "$username")

# Check if the user is found
if [ -z "$user_info" ]; then
    echo "User not found: $username"
    exit 1
fi

# Extract user details
full_name=$(echo "$user_info" | cut -d: -f5 | cut -d, -f1)
home_directory=$(echo "$user_info" | cut -d: -f6)
shell_type=$(echo "$user_info" | cut -d: -f7)

# Display user information
echo "User: $username"
echo "Full Name: $full_name"
echo "Home Directory: $home_directory"
echo "Shell Type: $shell_type"
