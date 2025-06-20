import csv

def read_csv_as_list(filepath):
    with open(filepath, newline='', encoding='utf-8') as f:
        return list(csv.reader(f))
