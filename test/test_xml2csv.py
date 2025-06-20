import os
import pandas as pd
import pytest
from xmlcsvconvert.xml2csv import xml_to_csv

def load_csv(path):
    return pd.read_csv(path).fillna("").sort_index(axis=1).reset_index(drop=True)

@pytest.fixture
def output_csv_file(tmp_path):
    return tmp_path / "converted.csv"

def test_xml_to_csv_conversion(output_csv_file):
    input_xml = "sample/long.xml"
    expected_csv = "sample/expected/output.csv"

    # Run conversion
    xml_to_csv(input_xml)

    # Generated CSV will be in same dir as input, so simulate relocation for testing
    generated_csv = input_xml.replace(".xml", ".csv")
    assert os.path.exists(generated_csv)

    # Load & compare
    result_df = load_csv(generated_csv)
    expected_df = load_csv(expected_csv)

    pd.testing.assert_frame_equal(result_df, expected_df, check_dtype=False)
