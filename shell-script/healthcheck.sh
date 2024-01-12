#!/bin/bash

# Current date and time
current_date_time=$(date +"%Y-%m-%d %H:%M:%S")
#current_date_time=$(date)
# System uptime
uptime_info=$(uptime)

# Total number of users currently logged in
logged_in_users=$(who | wc -l)

# Memory usage
memory_info=$(free -h | grep Mem)

# Disk usage
disk_info=$(df -h /)

# Display system information
echo "Health Check Report"
echo "-------------------"
echo "Date and Time: $current_date_time"
echo "Uptime: $uptime_info"
echo "Logged in Users: $logged_in_users"
echo "Memory Usage: $memory_info"
echo "Disk Usage: $disk_info"
