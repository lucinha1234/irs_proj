import pytest
import xml.etree.ElementTree as ET
from xmlcsvconvert.csv2xml import csv_to_xml

import xml.etree.ElementTree as ET

def elements_equal(e1, e2):
    if e1.tag != e2.tag:
        return False
    if (e1.text or '').strip() != (e2.text or '').strip():
        return False
    if (e1.tail or '').strip() != (e2.tail or '').strip():
        return False
    if sorted(e1.attrib.items()) != sorted(e2.attrib.items()):
        return False
    if len(e1) != len(e2):
        return False
    return all(elements_equal(c1, c2) for c1, c2 in zip(e1, e2))

def compare_xml_files(path1, path2):
    tree1 = ET.parse(path1)
    tree2 = ET.parse(path2)
    root1 = tree1.getroot()
    root2 = tree2.getroot()
    return elements_equal(root1, root2)

@pytest.fixture
def output_xml_file(tmp_path):
    return tmp_path / "output.xml"

def test_csv_to_xml_conversion(output_xml_file):
    input_csv = "sample/long.csv"
    meta_path = "sample/long_meta.json"
    expected_xml = "sample/long.xml"

    # Run conversion
    csv_to_xml(str(output_xml_file), meta_path, input_csv)
    
    assert output_xml_file.exists()

    assert compare_xml_files(output_xml_file, expected_xml)
