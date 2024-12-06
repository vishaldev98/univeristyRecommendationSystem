import pytest
from unittest import mock
import pandas as pd
from your_module import write_data, read_data  # Replace 'your_module' with the actual module name


# Mocking DataFrame for testing purposes
@pytest.fixture
def mock_dataframe():
    # Creating a mock dataframe that mimics the expected structure
    data = {
        'UNIVERSITY': ['University_A', 'University_B', 'University_C']
    }
    return pd.DataFrame(data)


# Test case for write_data function
@mock.patch('pandas.read_excel')
@mock.patch('builtins.open', new_callable=mock.mock_open)
@mock.patch('sklearn.preprocessing.LabelEncoder')
def test_write_data(mock_label_encoder, mock_open, mock_read_excel, mock_dataframe):
    """
    Test the write_data function to ensure it writes correctly to a file.
    """
    # Mock the read_excel to return the mock dataframe
    mock_read_excel.return_value = mock_dataframe

    # Mock the LabelEncoder to return a simple transformation
    mock_label_encoder_instance = mock.Mock()
    mock_label_encoder.return_value = mock_label_encoder_instance
    mock_label_encoder_instance.fit_transform.return_value = [0, 1, 2]

    # Call the function
    write_data()

    # Verify that the file was opened in write mode
    mock_open.assert_called_once_with(
        r"C:\projectworkspace\universityrecommendation\base\static\adminResources/canada_classes.txt", "w")

    # Check if the correct data was written to the file
    handle = mock_open()
    handle.write.assert_any_call('University_A 0\n')
    handle.write.assert_any_call('University_B 1\n')
    handle.write.assert_any_call('University_C 2\n')


# Test case for read_data function
@mock.patch('builtins.open', new_callable=mock.mock_open)
def test_read_data(mock_open):
    """
    Test the read_data function to ensure it reads correctly from a file.
    """
    # Mock the file content as if it was written by write_data
    mock_open.return_value.readlines.return_value = [
        'University_A 0\n',
        'University_B 1\n',
        'University_C 2\n'
    ]

    # Call the function with a mock college_id
    result = read_data(1)

    # Check if the correct value is returned for college_id 1
    assert result == 'University_B'

    # Verify that the file was opened in read mode
    mock_open.assert_called_once_with(
        r"C:\projectworkspace\universityrecommendation\base\static\adminResources/canada_classes.txt", "r")


# Test case for read_data function when no match is found
@mock.patch('builtins.open', new_callable=mock.mock_open)
def test_read_data_no_match(mock_open):
    """
    Test the read_data function when no matching college_id is found.
    """
    # Mock the file content as if it was written by write_data
    mock_open.return_value.readlines.return_value = [
        'University_A 0\n',
        'University_B 1\n',
        'University_C 2\n'
    ]

    # Call the function with an invalid college_id
    result = read_data(999)

    # Check if None is returned when no match is found
    assert result is None

    # Verify that the file was opened in read mode
    mock_open.assert_called_once_with(
        r"C:\projectworkspace\universityrecommendation\base\static\adminResources/canada_classes.txt", "r")


if __name__ == "__main__":
    pytest.main()
