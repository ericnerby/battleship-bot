"""
A module that makes conversions back and forth between human-friendly
coordinates and machine friendly zero-indexed values.

Functions
---------
ConvertToIndex
    Take letter or number values and return a tuple of zero-index values.
ConvertFromIndex
    Take zero-index int and return str in given format.
"""

import re
from string import ascii_lowercase as alphabet


def ConvertToIndex(*args, zero_index=False):
    """
    Take letter or number values and return a tuple of zero-index values.

    Parameters
    ----------
    *args : str or int
        str must be in set [a-zA-Z] or convertible to an int.
        int will be returned unchanged or converted from one-index
            to zero-index based on zero_index argument.
    zero_index : boolean, optional, keyword-only | default: False
        indicates whether int or int convertible str values are already
            zero-indexed.  

    Returns
    -------
    tuple of int
        a tuple of the given args converted to zero-indexed values
    """
    output = []
    if zero_index:
        index_adjust = 0
    else:
        index_adjust = -1
    for arg in args:
        if isinstance(arg, str):
            arg_letter = re.match(r"[a-zA-Z]", arg)
            arg_number = re.match(r"[-\d]+", arg)
            if arg_letter:
                output.append(
                    alphabet.index(arg_letter.group(0).lower()))
            elif arg_number is not None:
                output.append(
                    int(arg_number.group(0)) + index_adjust)
            else:
                raise ValueError(
                    "str arguments must be in the set [a-zA-Z\\d]."
                    + " You provided: '{}'.".format(arg))
        elif isinstance(arg, int):
            output.append(arg + index_adjust)
        else:
            raise TypeError(
                "Parameters for conversion must be int or str type.\n"
                + "You provided the value {} of the type {}.".format(
                                                             arg, type(arg)))
    return tuple(output)


def ConvertFromIndex(number, destination_format='one'):
    """
    Take zero-index int and return str in given format.

    Parameters
    ----------
    number : int
        Zero-index number to be converted.
        If used with 'lower' or 'upper' conversion, must be in range 0-25.
    destination_format : str, optional | default: 'one'
        determine which format to return
        'one' - a one-index number as a string
        'zero' - a zero-index number as a string
        'lower' - a lowercase letter value
        'upper' - an uppercase letter value

    Returns
    -------
    str
        a user-friendly str version of the int in the given format.
    """
    FORMAT_OPTIONS = {
        'lower': lambda num: alphabet[num],
        'upper': lambda num: alphabet[num].upper(),
        'zero': lambda num: str(num),
        'one': lambda num: str(num + 1),
    }
    if not isinstance(number, int):
        raise TypeError("'number' argument must be an integer.")
    if destination_format in FORMAT_OPTIONS:
        if (destination_format in {'upper', 'lower'}
                and number > len(alphabet)):
            raise ValueError(
                "'number' must be 0-25 for 'upper' or 'lower' conversion.")
        return FORMAT_OPTIONS[destination_format](number)
    else:
        raise ValueError(
            f"'destination_format' must be one of: {FORMAT_OPTIONS.keys}.")

