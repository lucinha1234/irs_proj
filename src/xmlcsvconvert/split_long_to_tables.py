import csv
from collections import defaultdict
import sys
import os

def split_long_to_tables(input_path, output_folder):
    grouped_data = defaultdict(lambda: defaultdict(dict))

    with open(input_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) < 6:
                continue
            key = tuple(row[:3])  # (Anexo, Quadro, SubQuadro)
            linha_raw = row[3]
            field = row[4]
            value = row[5]

            # Only process lines with "numero=X"
            if "numero=" in linha_raw:
                numero = linha_raw.split("numero=")[-1].split("]")[0]
                grouped_data[key][numero][field] = value

    # Save each table to a CSV file
    for key, lines in grouped_data.items():
        with open(f"{output_folder}/table_{'_'.join(key)}.csv", 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = list(list(lines.values())[0].keys())
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for linha, fields in lines.items():
                writer.writerow({'NLinha': linha, **fields})
        print(f"Saved: {csvfile.name}")

# Command-line entry
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python long_to_wide.py <input_csv_file> <output_folder_tables>")
        sys.exit(1)

    input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print(f"File not found: {input_file}")
        sys.exit(1)

    output_folder = sys.argv[2]
    if not os.path.exists(output_folder):
        print(f"File not found: {output_folder}")
        sys.exit(1)

    split_long_to_tables(input_file, output_folder)
