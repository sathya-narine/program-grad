#!/bin/bash

# Check if the process name argument is provided
if [ $# -eq 0 ]; then
    echo "Script expects one argument but none provided"
    exit 1
fi

# Process name
process_name=$1

# Check if the process is running
if pgrep -x "$process_name" > /dev/null; then
    # Process is running, get memory and CPU usage
    memory_usage=$(ps -e -o pid,%mem,cmd | awk -v process="$process_name" '$NF==process {print $2}')
    cpu_usage=$(ps -e -o pid,%cpu,cmd | awk -v process="$process_name" '$NF==process {print $2}')

    echo "Process '$process_name' is running."
    echo "Memory Usage: $memory_usage%"
    echo "CPU Usage: $cpu_usage%"
else
    # Process is not running, start it and log the event
    echo "Process '$process_name' is not running. Starting the process..."
    "$process_name" &

    # Log the event
    echo "$(date): Process '$process_name' started." >> process_monitor.log
fi
