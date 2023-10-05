import numpy as np
from petrophys.data.utils import convert_value_to_nan


def test_convert_value_to_nan():
    # Test case 1: Convert all -999.25 values to NaN
    input_array = np.array([1, 2, -999.25, 4, -999.25])
    expected_output = np.array([1, 2, np.nan, 4, np.nan])
    np.testing.assert_allclose(convert_value_to_nan(input_array), expected_output)


def test_convert_value_to_nan_with_value():
    # Test case 2: Convert all 0 values to NaN
    input_array = np.array([1, 2, 0, 4, 0])
    expected_output = np.array([1, 2, np.nan, 4, np.nan])
    np.testing.assert_allclose(
        convert_value_to_nan(input_array, value=0), expected_output
    )


def test_convert_value_to_nan_2d():
    # Test case 3: Convert all -999.25 values to NaN in a 2D array
    input_array = np.array([[1, 2, -999.25], [4, -999.25, 6]])
    expected_output = np.array([[1, 2, np.nan], [4, np.nan, 6]])
    np.testing.assert_allclose(convert_value_to_nan(input_array), expected_output)


def test_convert_value_to_nan_empty():
    # Test case 4: Convert all -999.25 values to NaN in an empty array
    input_array = np.array([])
    expected_output = np.array([])
    np.testing.assert_allclose(convert_value_to_nan(input_array), expected_output)
