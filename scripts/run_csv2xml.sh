#!/bin/bash

# Check if ouput file path is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <output_filepath>"
  exit 1
fi

# Call the Python script with the input path
python3 src/csv2xml.py "$1" "output_csv/meta.json" "output_csv/file.csv"
