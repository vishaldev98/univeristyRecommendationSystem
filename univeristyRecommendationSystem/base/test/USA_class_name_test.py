import pytest
import pandas as pd
from unittest import mock
from base.com.controller.usa_class_name import write_data, read_data

# Test for write_data function
def test_write_data(mocker):
    # Mock the Excel file reading
    mock_data = {
        'UNIVERSITY': ['University of Test1', 'University of Test2', 'University of Test3']
    }
    mock_df = pd.DataFrame(mock_data)
    mocker.patch('pandas.read_excel', return_value=mock_df)

    # Mock LabelEncoder to provide predictable IDs
    mock_label_encoder = mocker.patch('sklearn.preprocessing.LabelEncoder.fit_transform')
    mock_label_encoder.return_value = [0, 1, 2]

    # Mock file opening and writing
    mock_open = mocker.mock_open()
    mocker.patch("builtins.open", mock_open)

    # Run the function
    write_data()

    # Expected calls to write based on the mock data
    expected_calls = [
        mock.call().write("University_of_Test1 0\n"),
        mock.call().write("University_of_Test2 1\n"),
        mock.call().write("University_of_Test3 2\n")
    ]

    mock_open.assert_has_calls(expected_calls, any_order=True)

# Test for read_data function
def test_read_data(mocker):
    # Mock file reading with sample content simulating the written file
    mock_open = mocker.mock_open(read_data="University_of_Test1 0\nUniversity_of_Test2 1\nUniversity_of_Test3 2\n")
    mocker.patch("builtins.open", mock_open)

    # Test retrieval by college ID
    assert read_data(0) == "University_of_Test1"
    assert read_data(1) == "University_of_Test2"
    assert read_data(2) == "University_of_Test3"
