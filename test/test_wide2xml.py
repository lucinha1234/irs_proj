import os
import xml.etree.ElementTree as ET
import pandas as pd
import pytest
from xmlcsvconvert.wide2xml import wide_to_xml

def normalize_xml_element(elem):
    """Recursively sort children and strip text/attributes for reliable comparison."""
    # Sort children by tag and attributes
    elem[:] = sorted(elem, key=lambda e: (e.tag, sorted(e.attrib.items())))
    for child in elem:
        normalize_xml_element(child)

    # Strip leading/trailing whitespace from text
    if elem.text:
        elem.text = elem.text.strip()
    if elem.tail:
        elem.tail = elem.tail.strip()

    # Sort attributes (not necessary for ElementTree equality, but useful for readability/debug)
    elem.attrib = dict(sorted(elem.attrib.items()))

def load_xml(path):
    """Load and normalize XML file for comparison."""
    tree = ET.parse(path)
    root = tree.getroot()
    normalize_xml_element(root)
    return root

@pytest.fixture
def output_long_file(tmp_path):
    """Temporary output file path."""
    return tmp_path / "output_long.csv"

def load_xml(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    rows = []
    for element in root:
        row_data = {}
        for child in element:
            row_data[child.tag] = child.text or ""
        rows.append(row_data)

    df = pd.DataFrame(rows).fillna("")
    df = df.sort_values(by=sorted(df.columns)).reset_index(drop=True)
    return df

def test_wide_to_xml_conversion(output_long_file):
    input_folder = "sample/tables"
    expected_xml = "sample/long.xml"

    wide_to_xml(input_folder, str(output_long_file))

    assert output_long_file.exists(), "Output long-format file not created"
    print("output_long_file:",output_long_file)
    print("expected_xml:",expected_xml)
    result_df = load_xml(output_long_file)
    print("result_df:",result_df)
    expected_df = load_xml(expected_xml)
    print("expected_df:",expected_df)
    pd.testing.assert_frame_equal(result_df, expected_df, check_dtype=False)
