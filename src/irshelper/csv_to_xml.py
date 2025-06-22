import csv
import json
import xml.etree.ElementTree as ET
import argparse
import re

def strip_ns(tag):
    return tag.split('}', 1)[-1] if '}' in tag else tag

def parse_tag_with_attr(tag):
    match = re.match(r"(.*?)\[(.*?)=(.*?)\]$", tag)
    if match:
        tag_name = match.group(1)
        attr_name = match.group(2)
        attr_value = match.group(3)
        return tag_name, {attr_name: attr_value}
    else:
        return tag, {}

def get_or_create_child(parent, tag, attrs):
    for child in parent.findall(tag):
        if all(child.attrib.get(k) == v for k, v in attrs.items()):
            return child
    return ET.SubElement(parent, tag, attrs)

def set_nested_value(root, path_parts, value):
    current = root
    for part in path_parts:
        if not part.strip():  # ✅ Skip empty strings
            continue
        tag, attrs = parse_tag_with_attr(part)
        current = get_or_create_child(current, tag, attrs)
    current.text = value

def create_empty_nodes(root, empty_paths, filled_paths):
    for path in empty_paths:
        if path in filled_paths:
            continue
        parts = path.split(',')
        current = root
        for part in parts:
            if not part.strip():  # ✅ Skip empty strings
                continue
            tag, attrs = parse_tag_with_attr(part)
            current = get_or_create_child(current, tag, attrs)


def csv_to_xml(output_path, meta_path, csv_path):
    with open(meta_path, encoding="utf-8") as f:
        meta = json.load(f)

    root_info = meta["root"]
    attributes = meta["attributes"]
    empty_paths = meta["empty_paths"]

    ns_uri = root_info["namespace"]
    tag = root_info["tag"]
    attrib = root_info["attrib"]
    qualified_tag = f"{{{ns_uri}}}{tag}" if ns_uri else tag

    root = ET.Element(qualified_tag, attrib=attrib)
    if ns_uri:
        ET.register_namespace('', ns_uri)

    filled_paths = set()

    # Populate values from CSV
    with open(csv_path, newline='', encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or all(cell.strip() == '' for cell in row):
                continue  # skip empty rows
            value = row[-1]
            path_parts = row[:-1]
            set_nested_value(root, path_parts, value)
            filled_paths.add(','.join(path_parts))

    # Apply saved attributes
    for path, attr_dict in attributes.items():
        parts = path.split(',')
        current = root
        for part in parts:
            tag, attrs = parse_tag_with_attr(part)
            current = get_or_create_child(current, tag, attrs)
        current.attrib.update(attr_dict)

    # Re-add empty nodes if not already present
    create_empty_nodes(root, empty_paths, filled_paths)

    tree = ET.ElementTree(root)
    tree.write(output_path, encoding="utf-8", xml_declaration=True)

def main():
    parser = argparse.ArgumentParser(description="Convert CSV to XML")
    parser.add_argument("output", help="Output XML file path")
    parser.add_argument("meta", help="Metadata JSON file path")
    parser.add_argument("csv", help="Input CSV file path")
    args = parser.parse_args()

    csv_to_xml(args.output, args.meta, args.csv)
    print(f"XML saved to: {args.output}")

if __name__ == "__main__":
    main()
