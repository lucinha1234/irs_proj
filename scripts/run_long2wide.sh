#!/bin/bash

# Check if arguments are provided
if [ -z "$1" ]; then
  echo "Usage: $0 <tables_folder>"
  exit 1
fi

python3 xmlcsvconvert/long2wide.py "output_csv/file.csv" "$1"
