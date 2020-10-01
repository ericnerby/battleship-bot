from segments import Segment


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
    
    """Switch the orientation of the ship
    and its segment string representations"""
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
    
    """Build the segments for a ship based on its string representation list"""
    def _assign_segments(self):
        if self.orientation == 'h':
            for segment in self.horizontal_string_reps:
                self.segments.append(Segment(segment, self))
        elif self.orientation == 'v':
            for segment in self.vertical_string_reps:
                self.segments.append(Segment(segment, self))
    
    """Runs every time a hit is registered on a segment to see if all
    segments are hit.
    If all segments are hit, the Ship instance's sunk value is made true.
    Returns a boolean indicating whether the hit resulted
    in a sunken ship."""
    def check_sunk(self):
        if all([segment.hit for segment in self.segments]):
            self.sunk = True
        return self.sunk
    
    """Return length of segments when checking length of a Ship instance"""
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
