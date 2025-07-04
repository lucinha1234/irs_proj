import os
import csv
import pytest
from irshelper.split_long_to_tables import split_long_to_tables

def load_csv(path):
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = [dict(sorted(row.items())) for row in reader]
    # Sort rows for comparison
    return sorted(rows, key=lambda x: tuple(x.values()))

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

        assert result_df == expected_df, "Mismatch in output file contents"
