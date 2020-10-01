"""
Contains the Segment class to use with the ships module.

Classes
-------
Segment
    A class to represent an individual segment of a ship.
"""


class Segment():
    """
    A class to represent an individual segment of a ship.

    Attributes
    ----------
    string_rep_tup : tuple of str
        tuple with two strings that visually represent the section
        before and after a hit.
    ship : Ship object
        the Ship object that owns the Segment
    location : TBD
    hit : Boolean
        indicates whether the Segment has been hit

    Methods
    -------
    register_segment_hit():
        Changes 'hit' attribute to True and calls additional checks
    """
    def __init__(self, string_rep_tup, ship, location=None):
        """
        Constructs attributes for Segment object

        Parameters
        ----------
            string_rep_tup : tuple of str
                tuple with two strings that visually represent the
                section before and after a hit.
            ship : Ship object
                thie Ship object that owns the Segment
            location : TBD
        """
        self.string_rep_tup = string_rep_tup
        self.ship = ship
        self.location = location
        self.hit = False

    def register_segment_hit(self):
        """
        Changes 'hit' attribute to True and calls additional checks.

        After the 'hit' attribute is set to True on the current
        Segment, this method calls the check_sunk() method on the
        Ship owning the Segment.  This method then returns the return
        value from the parent Ship's method to indicate whether the
        Ship was sunk.

        IMPORTANT: Running this method on a Segment that has already been hit
        raises a TypeError.

        Parameters
        ----------
        None

        Returns
        -------
        Boolean - indicates whether the ship was sunk
        """
        if not self.hit:
            self.hit = True
            return self.ship.check_sunk()
        else:
            raise TypeError("Cannot register a hit on the ship segment"
                            + " located at "
                            + self.location
                            + " since it is already marked as hit.")

    def __str__(self):
        """Returns the appropriate visual string representation of the
        segment based on whether or not it's been hit."""
        if self.hit:
            return self.string_rep_tup[1]
        else:
            return self.string_rep_tup[0]
