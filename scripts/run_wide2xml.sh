#!/bin/bash

# Check if arguments are provided
if [ -z "$2" ]; then
  echo "Usage: $0 <tables_folder> <output_filepath>"
  exit 1
fi

python3 xmlcsvconvert/wide2xml.py "$1" "$2"