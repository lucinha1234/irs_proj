import os
import shutil
import pandas as pd
import pytest
from xmlcsvconvert.split_long_to_tables import split_long_to_tables

def load_csv(path):
    return pd.read_csv(path).sort_index(axis=1).fillna("")

@pytest.fixture
def test_output_folder(tmp_path):
    """Create a temporary output folder for testing."""
    return tmp_path

def test_long_to_wide_with_sample_data(test_output_folder):
    input_csv = "sample/long.csv"
    expected_dir = "sample/tables"
    
    split_long_to_tables(input_csv, str(test_output_folder))

    # Collect expected files
    expected_files = [f for f in os.listdir(expected_dir) if f.endswith(".csv")]
    generated_files = os.listdir(test_output_folder)
    
    assert set(generated_files) == set(expected_files), "Mismatch in output files"

    # Compare contents
    for file in expected_files:
        expected_df = load_csv(os.path.join(expected_dir, file))
        
        result_df = load_csv(os.path.join(test_output_folder, file))
        
        pd.testing.assert_frame_equal(result_df, expected_df, check_dtype=False)
