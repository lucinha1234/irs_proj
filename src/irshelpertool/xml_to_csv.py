import xml.etree.ElementTree as ET
import csv
import json
import argparse
import os

def strip_ns(tag):
    """Strip namespace from the tag"""
    return tag.split('}', 1)[-1] if '}' in tag else tag

def serialize_path(path_parts):
    """Serialize path parts for CSV"""
    return path_parts

def walk(elem, path=None, rows=None, attributes=None, empty_paths=None):
    """Recursively traverse XML elements to capture data"""
    if path is None:
        path = []
    if rows is None:
        rows = []
    if attributes is None:
        attributes = {}
    if empty_paths is None:
        empty_paths = set()

    tag = strip_ns(elem.tag)
    
    # Add "numero" attribute to tag if it exists
    if "numero" in elem.attrib:
        tag += f"[numero={elem.attrib['numero']}]"
    
    path.append(tag)

    # Store attributes in attributes dictionary
    if elem.attrib:
        attributes[",".join(path)] = dict(elem.attrib)

    children = list(elem)
    if children:
        for child in children:
            walk(child, path[:], rows, attributes, empty_paths)
    else:
        # If there's text, store the value
        text = (elem.text or "").strip()
        if text:
            rows.append((path[:], text))
        else:
            empty_paths.add(",".join(path))  # Mark as empty path if no text

    return rows, attributes, empty_paths

def xml_to_csv(input_path):
    output_dir = "output_csv"
    os.makedirs(output_dir, exist_ok=True)  # Ensure output directory exists

    tree = ET.parse(input_path)
    root = tree.getroot()

    # Skip the root node by processing only its children
    rows, attributes, empty_paths = [], {}, set()
    
    for child in root:
        # Process all children of the root
        child_rows, child_attributes, child_empty_paths = walk(child, path=[], rows=[], attributes={}, empty_paths=set())
        rows.extend(child_rows)
        attributes.update(child_attributes)
        empty_paths.update(child_empty_paths)

    # Find the maximum depth of the path for padding in the CSV
    max_depth = max(len(p) for p, _ in rows) if rows else 0

    # Extract just the filename without extension
    base_filename = os.path.splitext(os.path.basename(input_path))[0]

    # Build new output paths
    csv_path = os.path.join(output_dir, "file.csv")
    meta_path = os.path.join(output_dir, "meta.json")

    # Write the rows into the CSV file
    with open(csv_path, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        for path, value in rows:
            padded_path = path + [""] * (max_depth - len(path))  # Pad paths to uniform length
            writer.writerow(padded_path + [value])

    # Prepare the metadata
    ns_uri = root.tag.split("}")[0][1:] if "}" in root.tag else ""
    tag = strip_ns(root.tag)
    meta = {
        "root": {
            "tag": tag,
            "attrib": dict(root.attrib),
            "namespace": ns_uri
        },
        "attributes": attributes,
        "empty_paths": list(empty_paths)
    }

    # Save the metadata to a JSON file
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

    print(f"✅ CSV saved to: {csv_path}")
    print(f"✅ Meta saved to: {meta_path}")
    
def main():
    parser = argparse.ArgumentParser(description="Convert XML to CSV")
    parser.add_argument("input", help="Input XML file path")
    args = parser.parse_args()

    xml_to_csv(args.input)

if __name__ == "__main__":
    main()
