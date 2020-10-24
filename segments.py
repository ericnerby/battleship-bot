"""
Contains the Segment class to use with the ships module.

Segments are where locations are tracked and hits are registered.

Classes
-------
Segment
    A class to represent a segment of a Ship instance.
"""


class Segment():
    """
    A class to represent a segment of a Ship instance.

    Attributes
    ----------
    string_rep_tup : tuple of str
        tuple with two strings that visually represent the section
        before and after a hit.
    ship : Ship object
        the Ship object that owns the segment
    hit : boolean
        indicates whether the Segment instance has been hit
    """
    def __init__(self, string_rep_tup, ship):
        """
        Constructs attributes for Segment object

        Parameters
        ----------
            string_rep_tup : tuple of str
                tuple with two strings that visually represent the
                section before and after a hit.
            ship : Ship object
                the Ship object that owns the segment
        """
        self.string_rep_tup = string_rep_tup
        self.ship = ship
        self._hit = False

    # ------------Properties------------ #
    @property
    def hit(self):
        """Return 'hit' property of segment."""
        return self._hit

    @hit.setter
    def hit(self, value):
        """Set hit value. Produces an error if already hit."""
        if value:
            if not self._hit:
                self._hit = True
            else:
                raise TypeError(
                    "Cannot set 'hit' attribute to True on this "
                    + "segment since it is already marked as hit.")
        elif not value:
            self._hit = False
        else:
            raise ValueError("Value for 'hit' can only be a boolean.")

    # ------------Additional Dunder Methods------------ #
    def __str__(self):
        """Return visual string representation for segment."""
        if self.hit:
            return self.string_rep_tup[1]
        else:
            return self.string_rep_tup[0]

    def __repr__(self):
        """Return a string identifying key attributes of segment"""
        return "Ship segment of {}".format(self.ship)
