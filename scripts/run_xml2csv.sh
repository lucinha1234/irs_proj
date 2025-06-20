#!/bin/bash

# Check if input file path is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <input_filepath>"
  exit 1
fi

# Call the Python script with the input path
python3 xmlcsvconvert/xml2csv.py "$1"
