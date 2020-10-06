"""
Contains the Board and Space classes to place or guess ship locations.

This module is used to set up two 10x10 grids where the computer
opponent can track guesses on its turn and also place its own ships to
receive guesses from the player.

The Board is an ordered dictionary such that a space can be indentified
by letter and number.  For example, board_object['c'][7] would
represent 'C7' on the grid.

Classes
-------
Board
    An OrderedDict representing a grid with the letters A-J and numbers 1-10
Space
    A class for a space on the board which can hold a ship segment.
"""

from collections import OrderedDict
from string import ascii_lowercase as alphabet

from spaces import FieldSpace, RadarSpace


class Board(OrderedDict):
    """
    An OrderedDict representing a grid with the letters A-J and numbers 1-10

    Attributes
    ----------
    role : str
        'radar' or 'field' determines which purpose the board is serving
    """
    def __init__(self, role, *args, **kwargs):
        """
        Construct attributes for Board object

        Parameters
        ----------
            role : Player object
                the object which owns the Board
        """
        if role not in {'radar', 'field'}:
            raise ValueError(
                "'role' argument must equal 'radar' or 'field'.")
        super().__init__(*args, **kwargs)
        self.role = role
        self._set_up_spaces()

    def _set_up_spaces(self):
        """Set up grid of A-J and numbers 1-10 with Space instances."""
        for letter in alphabet[:10]:
            self[letter] = OrderedDict()
            for number in range(1, 11):
                location = letter.upper() + str(number)
                if self.role == 'radar':
                    self[letter][number] = RadarSpace(location, self)
                else:
                    self[letter][number] = FieldSpace(location, self)
