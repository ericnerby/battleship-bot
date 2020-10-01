class Segment():
    """Each Segment has a location and a string
    representation and belongs to a certain ship"""
    def __init__(self, string_rep_tup, ship, location=None):
        self.string_rep_tup = string_rep_tup
        self.ship = ship
        self.location = location
        self.hit = False
    
    """Return the appropriate ASCII representation of
    the segment based on whether or not it's been hit."""
    def __str__(self):
        if self.hit:
            return self.string_rep_tup[1]
        else:
            return self.string_rep_tup[0]
    
    """Register a hit on a Segment and call the function from its
    ship that checks if the ship was sunk.
    Return the boolean value 'sunk' from the ship."""
    def register_segment_hit(self):
        if self.hit == False:
            self.hit = True
            return self.ship.check_sunk()
        else:
            raise TypeError("Cannot register a hit on "
                            + self
                            + " since it is already marked as hit.")
