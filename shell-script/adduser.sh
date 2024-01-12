#!/bin/bash

# Check if the script is run as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root"
    exit 1
fi

# Set user information
username="test"
full_name="test acc"
password="pass123"
shell_type="/bin/bash"

# Check if the user already exists
if id "$username" &>/dev/null; then
    echo "User '$username' already exists."
    exit 1
fi

# Add the user with specified information
useradd -m -c "$full_name" -s "$shell_type" "$username"

# Set the password
echo "$username:$password" | chpasswd

echo "User '$username' has been added with the following information:"
echo "Full Name: $full_name"
echo "Password: $password"
echo "Shell Type: $shell_type"
