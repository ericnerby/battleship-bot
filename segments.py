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