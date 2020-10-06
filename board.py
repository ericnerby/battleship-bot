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

from segments import Segment


class Board(OrderedDict):
    """
    An OrderedDict representing a grid with the letters A-J and numbers 1-10

    Attributes
    ----------
    owner : Player object
        the object which owns the Board
    """
    def __init__(self, owner):
        """
        Construct attributes for Board object

        Parameters
        ----------
            owner : Player object
                the object which owns the Board
        """
        self.owner = owner
        self._set_up_spaces()

    def _set_up_spaces(self):
        """Set up grid of A-J and numbers 1-10 with Space instances."""
        for letter in alphabet[:10]:
            self[letter] = OrderedDict()
            for number in range(1, 11):
                location = letter.upper() + str(number)
                self[letter][number] = Space(location, self)


class Space:
    """
    A class for a space on the board which can hold a ship segment.

    Attributes
    ----------
    location : str
        a string representation of the grid location, eg. 'F7'
    board : Board object
        the board to which the space belongs
    guessed : boolean
        whether a guess has been made on the space
    segment : None or Segment object
        the Segment object assigned to the space (or None if not assigned)
    """
    def __init__(self, location, board):
        """
        Construct attributes for Space object

        Parameters
        ----------
            location : str
                a string representation of the grid location, eg. 'F7'
            board : Board object
                the board to which the space belongs
        """
        self.location = location
        self.board = board
        self.guessed = False
        self._segment = None

    @property
    def segment(self):
        """Return 'segment' property of the Space."""
        return self._segment

    @segment.setter
    def segment(self, segment):
        """Assign a Segment to the 'segment' property."""
        if self._segment:
            raise TypeError(
                "Can't assign a segment to "
                + self.location
                + " since the space is already assigned a segment.")
        else:
            self._segment = segment
