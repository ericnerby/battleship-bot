from segments import Segment


class Ship():
    """
    A class to represent a ship on the board.

    Attributes
    ----------
    owner : Player object
        the object representing who owns the ship
    ship_type : str
        indicates the type of ship for reference in messages
    horizontal_string_reps : list of tuples
        a list of tuples that contain string representations for
        hit and not hit segments of the Ship when horizontal
    vertical_string_reps : list of tuples
        a list of tuples that contain string representations for
        hit and not hit segments of the Ship when vertical
    orientation : str
        orientation of the Ship on the board
            'h' for horizontal
            'v' for vertical
    segments : list of Segment objects
        a list containing each Segment of the Ship
    sunk: Boolean
        indicates whether the Ship is sunk

    Methods
    -------
    rotate():
        Change orientation of the Ship from 'v' to 'h' or 'h' to 'v'
    check_sunk():
        Checks to see if ship is sunk based on all segments being hit
    """

    def __init__(self, owner, ship_type, horizontal_string_reps=[],
                 vertical_string_reps=[], *, orientation='h'):
        """
        Constructs attributes for Ship object

        Parameters
        ----------
            owner : Player object
                object which owns the ship
            ship_type : str
                a string representing the type of ship
                example: 'PT Boat'
            horizontal_string_reps : list of tuples, optional
                should generally be passed by __init__ in subclass
                (default is [])
            vertical_string_reps : list of tuples, optional
                should generally be passed by __init__ in subclass
                (default is [])
            orientation : str, optional
                'h' for horizontal, 'v' for vertical (default is 'h')
        """
        self.owner = owner
        self.ship_type = ship_type
        self.horizontal_string_reps = horizontal_string_reps
        self.vertical_string_reps = vertical_string_reps
        self.orientation = orientation
        self.segments = []
        self.sunk = False
        self._assign_segments()

    def _assign_segments(self):
        """
        Based on the string_reps and orientation, creates and assigns
        Segment objects to the segments list.
        """
        if self.orientation == 'h':
            for segment in self.horizontal_string_reps:
                self.segments.append(Segment(segment, self))
        elif self.orientation == 'v':
            for segment in self.vertical_string_reps:
                self.segments.append(Segment(segment, self))

    def rotate(self):
        """
        Change orientation of the Ship from 'v' to 'h' or 'h' to 'v'

        Flips the orientation of the Ship based on its current
        orientation.  This method also changes the string
        representations of the segments to match the newly assigned
        orientation.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
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

    def check_sunk(self):
        """
        Checks to see if ship is sunk based on all segments being hit.

        Checks 'hit' attribute of each Segment in segments list and
        if all are True, sets 'sunk' attribute of ship to True.

        Parameters
        ----------
        None

        Returns
        -------
        Boolean - indicates whether the ship was sunk
        """
        if all([segment.hit for segment in self.segments]):
            self.sunk = True
        return self.sunk

    def __len__(self):
        """Returns length of 'segments' attribute for ship length"""
        return len(self.segments)


class Carrier(Ship):
    def __init__(self, owner, orientation='h'):
        horizontal_string_reps = [
            ("[=", "[x"),
            ("==", "=x"),
            ("#=", "#x"),
            ("==", "=x"),
            ("=]", "x]"),
        ]
        vertical_string_reps = [
            ("[]", "[X"),
            ("||", "|X"),
            ("#|", "#X"),
            ("||", "|X"),
            ("[]", "[X"),
        ]
        super().__init__(owner, 'Carrier', horizontal_string_reps,
                         vertical_string_reps, orientation=orientation)


class Battleship(Ship):
    def __init__(self, owner, orientation='h'):
        horizontal_string_reps = [
            ("<=", "<x"),
            ("==", "=x"),
            ("==", "=x"),
            ("=]", "x]"),
        ]
        vertical_string_reps = [
            ("/\\", "/X"),
            ("||", "|X"),
            ("||", "|X"),
            ("[]", "[X"),
        ]
        super().__init__(owner, 'Battleship', horizontal_string_reps,
                         vertical_string_reps, orientation=orientation)


class Destroyer(Ship):
    def __init__(self, owner, orientation='h'):
        horizontal_string_reps = [
            ("<=", "<x"),
            ("==", "=x"),
            ("=]", "x]"),
        ]
        vertical_string_reps = [
            ("/\\", "/X"),
            ("||", "|X"),
            ("[]", "[X"),
        ]
        super().__init__(owner, 'Destroyer', horizontal_string_reps,
                         vertical_string_reps, orientation=orientation)


class Submarine(Ship):
    def __init__(self, owner, orientation='h'):
        horizontal_string_reps = [
            ("<=", "<x"),
            ("^=", "^x"),
            ("=>", "x>"),
        ]
        vertical_string_reps = [
            ("/\\", "/X"),
            ("|>", "|X"),
            ("\\/", "\\X"),
        ]
        super().__init__(owner, 'Submarine', horizontal_string_reps,
                         vertical_string_reps, orientation=orientation)


class PTBoat(Ship):
    def __init__(self, owner, orientation='h'):
        horizontal_string_reps = [
            ("<=", "<x"),
            ("=]", "x]"),
        ]
        vertical_string_reps = [
            ("/\\", "/X"),
            ("[]", "[X"),
        ]
        super().__init__(owner, 'PT Boat', horizontal_string_reps,
                         vertical_string_reps, orientation=orientation)
