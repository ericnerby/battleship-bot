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
    location : TBD
    hit : boolean
        indicates whether the Segment instance has been hit
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
                the Ship object that owns the segment
            location : TBD
        """
        self.string_rep_tup = string_rep_tup
        self.ship = ship
        self.location = location
        self.hit = False

    def register_segment_hit(self):
        """
        Change 'hit' attribute to True.

        IMPORTANT: Running this method on a Segment instance that has
        already been hit raises a TypeError.

        Parameters
        ----------
        None

        Returns
        -------
        boolean - indicates whether the Ship instance was sunk
        """
        if not self.hit:
            self.hit = True
        else:
            raise TypeError("Cannot register a hit on the ship segment"
                            + " located at "
                            + self.location
                            + " since it is already marked as hit.")

    def __str__(self):
        """Return the appropriate visual string representation of the
        segment based on whether or not it's been hit."""
        if self.hit:
            return self.string_rep_tup[1]
        else:
            return self.string_rep_tup[0]

    def __repr__(self):
        """Return a string identifying key attributes of segment"""
        return "Segment located at " + self.location
