"""
Contains Ship and its subclasses for a Battleship game.

The Ship class keeps segments grouped appropriately and uses the
segments to determine whether a ship is sunk. It also creates the
segments with the appropriate string representations that match the
class of the ship.

Classes
-------
Ship
    A class to represent a ship on the board.

Subclasses of Ship
------------------
Carrier
Battleship
Destroyer
Submarine
PTBoat
"""

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

    Properties
    ----------
    sunk: boolean
        indicates whether the Ship instance is sunk
    """

    def __init__(self, ship_type, horizontal_string_reps,
                 vertical_string_reps, *, orientation='h'):
        """
        Construct attributes for Ship object

        Parameters
        ----------
            ship_type : str
                a string representing the type of ship
                example: 'PT Boat'
            horizontal_string_reps : list of tuples, optional
                should generally be passed by __init__ in subclass
            vertical_string_reps : list of tuples, optional
                should generally be passed by __init__ in subclass
            orientation : str, optional, keyword-only | default: 'h'
                'h' for horizontal, 'v' for vertical
        """
        if orientation not in {'v', 'h'}:
            raise ValueError(
                "'orientation' argument must equal 'v' or 'h'."
            )
        self.ship_type = ship_type
        self.horizontal_string_reps = horizontal_string_reps
        self.vertical_string_reps = vertical_string_reps
        self.orientation = orientation
        self.segments = []
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
        Change orientation of the Ship from 'v' to 'h' or 'h' to 'v'.

        Flips the orientation of the Ship based on its current
        orientation.  This method also changes the string
        representations of the segments to match the newly assigned
        orientation.

        Returns
        -------
        str - the new orientation value after rotation
        """
        if self.orientation == 'h':
            self.orientation = 'v'
            for segment, segment_rep in zip(self.segments,
                                            self.vertical_string_reps):
                segment.string_rep_tup = segment_rep
            return self.orientation
        self.orientation = 'h'
        for segment, segment_rep in zip(self.segments,
                                        self.horizontal_string_reps):
            segment.string_rep_tup = segment_rep
        return self.orientation

    # ------------Properties------------ #
    @property
    def sunk(self):
        """
        Indicate if ship is sunk based on all segments being hit.

        Returns
        -------
        boolean - indicates whether the ship was sunk
        """
        return all([segment.hit for segment in self.segments])

    @sunk.setter
    def sunk(self, value):
        """Allow setting of sunk value for computer opponent usage"""
        if value:
            for segment in self.segments:
                if not segment.hit:
                    segment.hit = True
        elif not value:
            raise ValueError(
                "A ship's 'sunk' value can't be set to False directly.\n"
                + "Set 'hit' attribute on segments to False instead.")
        else:
            raise ValueError("Value for 'sunk' can only be a boolean.")

    # ------------Additional Dunder Methods------------ #
    def __len__(self):
        """Return length of 'segments' attribute for ship length."""
        return len(self.segments)

    def __str__(self):
        """Return ship_type when printing ship."""
        return self.ship_type


class Carrier(Ship):
    """
    Subclass of ship with Carrier attributes filled in.
    """

    def __init__(self, *, orientation='h'):
        """
        Construct attributes for Carrier subclass of Ship.

        Parameters
        ----------
            owner : Player object
                object which owns the ship
            orientation : str, optional, keyword-only
                'h' for horizontal, 'v' for vertical (default is 'h')
        """
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
        super().__init__('Carrier', horizontal_string_reps,
                         vertical_string_reps, orientation=orientation)


class Battleship(Ship):
    """
    Subclass of Ship with Battleship attributes filled in.
    """

    def __init__(self, *, orientation='h'):
        """
        Construct attributes for Battleship subclass of Ship.

        Parameters
        ----------
            owner : Player object
                object which owns the ship
            orientation : str, optional, keyword-only
                'h' for horizontal, 'v' for vertical (default is 'h')
        """
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
        super().__init__('Battleship', horizontal_string_reps,
                         vertical_string_reps, orientation=orientation)


class Destroyer(Ship):
    """
    Subclass of Ship with Destroyer attributes filled in.
    """

    def __init__(self, *, orientation='h'):
        """
        Construct attributes for Destroyer subclass of Ship.

        Parameters
        ----------
            owner : Player object
                object which owns the ship
            orientation : str, optional, keyword-only
                'h' for horizontal, 'v' for vertical (default is 'h')
        """
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
        super().__init__('Destroyer', horizontal_string_reps,
                         vertical_string_reps, orientation=orientation)


class Submarine(Ship):
    """
    Subclass of Ship with Submarine attributes filled in.
    """

    def __init__(self, *, orientation='h'):
        """
        Construct attributes for Submarine subclass of Ship.

        Parameters
        ----------
            owner : Player object
                object which owns the ship
            orientation : str, optional, keyword-only
                'h' for horizontal, 'v' for vertical (default is 'h')
        """
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
        super().__init__('Submarine', horizontal_string_reps,
                         vertical_string_reps, orientation=orientation)


class PTBoat(Ship):
    """
    Subclass of Ship with PTBoat attributes filled in.
    """

    def __init__(self, *, orientation='h'):
        """
        Construct attributes for PTBoat subclass of Ship.

        Parameters
        ----------
            owner : Player object
                object which owns the ship
            orientation : str, optional, keyword-only
                'h' for horizontal, 'v' for vertical (default is 'h')
        """
        horizontal_string_reps = [
            ("<=", "<x"),
            ("=]", "x]"),
        ]
        vertical_string_reps = [
            ("/\\", "/X"),
            ("[]", "[X"),
        ]
        super().__init__('PT Boat', horizontal_string_reps,
                         vertical_string_reps, orientation=orientation)
