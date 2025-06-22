import os
import sys
import xml.etree.ElementTree as ET
import csv

def join_tables_to_xml(folder_path, output_xml):
    root = ET.Element("Modelo")

    for filename in sorted(os.listdir(folder_path)):
        if not filename.startswith("table_") or not filename.endswith(".csv"):
            continue


        parts = filename.replace("table_", "").replace(".csv", "").split("_")
        if len(parts) < 3:
            continue

        anexo, quadro, subquadro = parts[:3]
        csv_path = os.path.join(folder_path, filename)
        if not os.path.isfile(csv_path):
            print(f"File not found: {csv_path}")
            continue
        
        # Ensure structure: root -> Anexo -> Quadro -> Subquadro
        anexo_elem = root.find(anexo)
        if anexo_elem is None:
            anexo_elem = ET.SubElement(root, anexo)

        quadro_elem = anexo_elem.find(quadro)
        if quadro_elem is None:
            quadro_elem = ET.SubElement(anexo_elem, quadro)

        subquadro_elem = ET.SubElement(quadro_elem, subquadro)

        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for idx, row in enumerate(reader, start=1):
                linha_elem = ET.SubElement(subquadro_elem, f"{subquadro}-Linha", {"numero": str(idx)})

            for field in row.keys():
                if not row[field]:
                    continue
                field_elem = ET.SubElement(linha_elem, field)
                field_elem.text = str(row[field])

    # Write XML tree to file
    tree = ET.ElementTree(root)
    tree.write(output_xml, encoding="utf-8", xml_declaration=True)
    print(f"Saved XML: {output_xml}")

# CLI entry
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python wide_to_long.py <folder_with_tables> <output_xml_file>")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.isdir(input_folder):
        print(f"Folder not found: {input_folder}")
        sys.exit(1)

    join_tables_to_xml(input_folder, output_file)
