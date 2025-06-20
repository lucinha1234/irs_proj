import xml.etree.ElementTree as ET
import pytest
from xmlcsvconvert.csv2xml import csv_to_xml

def normalize_xml(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    def recursive_sort(elem):
        elem[:] = sorted(elem, key=lambda e: e.tag)
        for child in elem:
            recursive_sort(child)

    recursive_sort(root)
    return ET.tostring(root, encoding="unicode")

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

    result_xml = normalize_xml(output_xml_file)
    print("result_xml:",result_xml)
    expected_xml_str = normalize_xml(expected_xml)
    print("expected_xml_str:",expected_xml_str)
    assert result_xml == expected_xml_str
