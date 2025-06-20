import os
import pandas as pd
import sys
import xml.etree.ElementTree as ET

def wide_to_long_xml(folder_path, output_xml):
    root = ET.Element("Document")

    for filename in sorted(os.listdir(folder_path)):
        if not filename.startswith("table_") or not filename.endswith(".csv"):
            continue


        parts = filename.replace("table_", "").replace(".csv", "").split("_")
        if len(parts) < 3:
            continue

        anexo, quadro, subquadro = parts[:3]
        df = pd.read_csv(os.path.join(folder_path, filename))

        # Create XML elements
        subquadro_elem = ET.SubElement(root, "SubQuadro", {
            "Anexo": anexo,
            "Quadro": quadro,
            "Nome": subquadro
        })

        for _, row in df.iterrows():
            if 'NLinha' in df.columns and not pd.isna(row['NLinha']):
                numero = int(float(row['NLinha']))
                linha_elem = ET.SubElement(subquadro_elem, "Linha", {"numero": str(numero)})
            else:
                linha_elem = ET.SubElement(subquadro_elem, "Linha")

            for field in df.columns:
                if pd.isna(row[field]):
                    continue
                if field == 'NLinha':
                    continue  # Already handled as attribute
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

    wide_to_long_xml(input_folder, output_file)
