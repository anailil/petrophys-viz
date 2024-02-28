import numpy as np


def convert_value_to_nan(arr: np.ndarray, value: float = -999.25):
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
    arr[arr==value] = np.nan
    return arr

def get_values(measure_data, data_key, mini=False, maxi=False):
    """Return values of a single column of a dataset 


    Parameters
    ----------
    measure_data : array
        Input data.
    data_key : str
       Key of the column to return
    mini: Boolean
        If true remove outliners
        Default is False
    maxi: Boolean
        If true remove outliners
        Default is False

    Returns
    -------
    np.array

    """
    value = np.array(measure_data[data_key], dtype=float)
    if mini:
        np.nanmin(value)
    if maxi:
        np.nanmax(value)

    return value
