import numpy as np


def convert_value_to_nan(arr: np.ndarray, value: float = -999.25) -> np.ndarray:
    """Convert all entries of value to NaN.

    E.g. null = -999.25
    Type <print(lasfile.well)> to find out this value

    Parameters
    ----------
    array : np.ndarray
        Input data.
    value : float, optional
        Value to be converted to NaN's, by default -999.25.

    Returns
    -------
    np.ndarray

    """
    arr_with_nan = np.where(arr == value, np.nan, arr)
    return arr_with_nan
