import xml.etree.ElementTree as ET
import pytest
from xmlcsvconvert.join_tables_to_xml import join_tables_to_xml

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

    # Fill missing columns with ""
    all_columns = set()
    for row in rows:
        all_columns.update(row.keys())
    for row in rows:
        for col in all_columns:
            if col not in row:
                row[col] = ""

    # Sort rows for comparison
    sorted_columns = sorted(all_columns)
    rows = [dict(sorted(row.items())) for row in rows]
    rows = sorted(rows, key=lambda x: tuple(x[col] for col in sorted_columns))
    return rows

def test_wide_to_xml_conversion(output_long_file):
    input_folder = "sample/tables"
    expected_xml = "sample/long.xml"

    join_tables_to_xml(input_folder, str(output_long_file))

    assert output_long_file.exists(), "Output long-format file not created"
    
    result_df = load_xml(output_long_file)
    print("result_df:",result_df)
    expected_df = load_xml(expected_xml)
    print("expected_df:",expected_df)
    assert result_df == expected_df, "XML conversion output does not match expected result"
