"""
A module that makes conversions from human friendly coordinates to
machine friendly zero-indexed values.

Classes
-------
CoordinateConverter
    Take letter or number values and return a tuple of zero-index values.
"""

import re
from string import ascii_lowercase as alphabet


class CoordinateConverter(tuple):
    """
    Take letter or number values and return a tuple of zero-index values.

    Parameters
    ----------
    *args : str or int
        str must be in range [a-zA-Z] or convertible to an int.
        int will be returned unchanged or converted from one-index
            to zero-index based on zero_index argument.
    zero_index : boolean, named-only, optional | Default: False
        indicates whether int or int convertible str values are already
            zero-indexed.  

    Returns
    -------
    tuple of int
        a tuple of the given args converted to zero-indexed values
    """
    def __new__(cls, *args, zero_index=False):
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
                    + "You provided the value {} of the type {}.".format(arg, type(arg)))
        return super().__new__(cls, output)
