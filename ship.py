class Ship():
    def __init__(self, owner):
        self.orientation = ''
        self.segments = []
        self.owner = owner
        self.sunk = False


class Carrier(Ship):
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


class Battleship(Ship):
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


class Destroyer(Ship):
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


class Submarine(Ship):
    HORIZONTAL_STRING_REPS = [
        ("<=", "<x"),
        ("==", "=x"),
        ("=>", "x>"),
    ]
    VERTICAL_STRING_REPS = [
        ("/\\", "/X"),
        ("||", "|X"),
        ("\\/", "\\X"),
    ]


class PTBoat(Ship):
    HORIZONTAL_STRING_REPS = [
        ("<=", "<x"),
        ("=]", "x]"),
    ]
    VERTICAL_STRING_REPS = [
        ("/\\", "/X"),
        ("[]", "[X"),
    ]


class Segment():
    def __init__(self, string_rep_tup, ship, location=None):
        self.string_rep_tup = string_rep_tup
        self.ship = ship
        self.location = location
        self.hit = False