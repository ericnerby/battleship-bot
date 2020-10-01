class Ship():
    """A Ship object represents one ship on the board, along with its
    segments and string representation for display when necessary."""
    def __init__(self, owner, ship_type, horizontal_string_reps=[],
                 vertical_string_reps=[], orientation='h'):
        self.owner = owner
        self.ship_type = ship_type
        self.horizontal_string_reps = horizontal_string_reps
        self.vertical_string_reps = vertical_string_reps
        self.orientation = orientation
        self.segments = []
        self.sunk = False
        self._assign_segments()
    
    def rotate(self):
        if self.orientation == 'h':
            self.orientation = 'v'
            for segment, segment_rep in zip(self.segments,
                                            self.vertical_string_reps):
                segment.string_rep_tup = segment_rep
        elif self.orientation == 'v':
            self.orientation = 'h'
            for segment, segment_rep in zip(self.segments,
                                            self.horizontal_string_reps):
                segment.string_rep_tup = segment_rep
    
    def _assign_segments(self):
        if self.orientation == 'h':
            for segment in self.horizontal_string_reps:
                self.segments.append(Segment(segment, self))
        elif self.orientation == 'v':
            for segment in self.vertical_string_reps:
                self.segments.append(Segment(segment, self))
    
    def __len__(self):
        return len(self.segments)


class Carrier(Ship):
    def __init__(self, owner, orientation='h'):
        HORIZONTAL_STRING_REPS = [
            ("[=", "[x"),
            ("==", "=x"),
            ("#=", "#x"),
            ("==", "=x"),
            ("=]", "x]"),
        ]
        VERTICAL_STRING_REPS = [
            ("[]", "[X"),
            ("||", "|X"),
            ("#|", "#X"),
            ("||", "|X"),
            ("[]", "[X"),
        ]
        super().__init__(owner, 'Carrier', HORIZONTAL_STRING_REPS,
                         VERTICAL_STRING_REPS, orientation)


class Battleship(Ship):
    def __init__(self, owner, orientation='h'):
        HORIZONTAL_STRING_REPS = [
            ("<=", "<x"),
            ("==", "=x"),
            ("==", "=x"),
            ("=]", "x]"),
        ]
        VERTICAL_STRING_REPS = [
            ("/\\", "/X"),
            ("||", "|X"),
            ("||", "|X"),
            ("[]", "[X"),
        ]
        super().__init__(owner, 'Battleship', HORIZONTAL_STRING_REPS,
                         VERTICAL_STRING_REPS, orientation)



class Destroyer(Ship):
    def __init__(self, owner, orientation='h'):
        HORIZONTAL_STRING_REPS = [
            ("<=", "<x"),
            ("==", "=x"),
            ("=]", "x]"),
        ]
        VERTICAL_STRING_REPS = [
            ("/\\", "/X"),
            ("||", "|X"),
            ("[]", "[X"),
        ]
        super().__init__(owner, 'Destroyer', HORIZONTAL_STRING_REPS,
                         VERTICAL_STRING_REPS, orientation)


class Submarine(Ship):
    def __init__(self, owner, orientation='h'):
        HORIZONTAL_STRING_REPS = [
            ("<=", "<x"),
            ("^=", "^x"),
            ("=>", "x>"),
        ]
        VERTICAL_STRING_REPS = [
            ("/\\", "/X"),
            ("|>", "|X"),
            ("\\/", "\\X"),
        ]
        super().__init__(owner, 'Submarine', HORIZONTAL_STRING_REPS,
                         VERTICAL_STRING_REPS, orientation)


class PTBoat(Ship):
    def __init__(self, owner, orientation='h'):
        HORIZONTAL_STRING_REPS = [
            ("<=", "<x"),
            ("=]", "x]"),
        ]
        VERTICAL_STRING_REPS = [
            ("/\\", "/X"),
            ("[]", "[X"),
        ]
        super().__init__(owner, 'PT Boat', HORIZONTAL_STRING_REPS,
                         VERTICAL_STRING_REPS, orientation)


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