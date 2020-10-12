"""
Contains the Board and Space classes to place or guess ship locations.

This module is used to set up two 10x10 grids where the computer
opponent can track guesses on its turn and also place its own ships to
receive guesses from the player.

The Board is a zero-indexed list of zero-indexed lists.  The first
index represents the letter-row, and the second represents the
number-column.
For example, space A10 would be identified as board[0][9].

Classes
-------
Board
    A 2-D list representing a 10 x 10 grid
Space
    A class for a space on the board which can hold a ship segment.
"""

from string import ascii_lowercase as alphabet

from spaces import FieldSpace, RadarSpace


class Board(list):
    """
    A 2-D list representing a 10 x 10 grid

    Attributes
    ----------
    role : str
        'radar' or 'field' determines board purpose
    """
    def __init__(self, role, *args, **kwargs):
        """
        Construct attributes for Board object

        Parameters
        ----------
            role : str
                'radar' or 'field' determines board purpose
        """
        if role not in {'radar', 'field'}:
            raise ValueError(
                "'role' argument must equal 'radar' or 'field'.")
        super().__init__(*args, **kwargs)
        self.role = role
        self._set_up_spaces()

    def _set_up_spaces(self):
        """Set up 10 x 10 zero-indexed grid with Space instances."""
        for index, letter in enumerate(alphabet[:10]):
            self.append([])
            for number in range(10):
                # Generate str representation of location for space.
                # Example: 'J7'
                location = letter.upper() + str(number + 1)
                if self.role == 'radar':
                    self[index].append(RadarSpace(location, self))
                else:
                    self[index].append(FieldSpace(location, self))

    def __str__(self):
        """Return string of board with role listed."""
        return "{} board".format(self.role)
