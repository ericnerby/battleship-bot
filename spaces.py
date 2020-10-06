"""
Contains the Space classes for use by the Board class.

Classes
-------
Space
    An abstract class for a space on the board which can hold a ship segment.

Subclasses of Space
-------------------
FieldSpace
    A grid space where ships can be placed and ship locations guessed.
RadarSpace
    A grid space where hits or misses can be recorded from guesses.
"""


class Space:
    """
    An abstract class for a space on the board which can hold a ship segment.

    Attributes
    ----------
    location : str
        a string representation of the grid location, eg. 'F7'
    board : Board object
        the board to which the space belongs
    guessed : boolean
        whether a guess has been made on the space
    """
    def __init__(self, location, board):
        """
        Construct attributes for Space object

        Parameters
        ----------
            location : str
                a string representation of the grid location, eg. 'F7'
            board : Board object
                the board to which the space belongs
        """
        self.location = location
        self.board = board
        self._guessed = False

    @property
    def guessed(self):
        """Return guessed property"""
        return self._guessed

    def _validate_unguessed(self):
        """Check if '_guessed' is currently False, then mark it True"""
        if self._guessed:
            raise TypeError(
                "Can't make a guess on '"
                + self.location
                + "' since a guess has already been made on the space.")
        self._guessed = True


class FieldSpace(Space):
    """
    A grid space where ships can be placed and ship locations guessed.

    FieldSpace is a subclass of Space and adds the attribute listed
    below along with the method make_guess().

    Additional Attributes
    ---------------------
    segment : None or Segment object
        the Segment object assigned to the space (or None if not assigned)
    """
    def __init__(self, location, board):
        """
        Construct attributes for FieldSpace object

        Parameters
        ----------
            location : str
                a string representation of the grid location, eg. 'F7'
            board : Board object
                the board to which the space belongs
        """
        super().__init__(location, board)
        self._segment = None

    @property
    def segment(self):
        """Return 'segment' property of the Space."""
        return self._segment

    @segment.setter
    def segment(self, segment):
        """Assign a Segment to the 'segment' property."""
        if self._segment:
            raise TypeError(
                "Can't assign a segment to "
                + self.location
                + " since the space is already assigned a segment.")
        self._segment = segment
    

    def make_guess(self):
        """
        Mark space as guessed and return segment from space or None.

        Returns
        -------
        Segment object or None
        """
        # call method to check whether a guess was already placed and
        #   mark space as guessed
        self._validate_unguessed()
        return self.segment


class RadarSpace(Space):
    """
    A grid space where hits or misses can be recorded from guesses.

    RadarSpace is a subclass of Space and adds the property listed
    below along with the method note_guess().

    Additional Properties
    ---------------------
    hit : int
        0: unguessed
        1: miss
        2: hit
    """
    def __init__(self, location, board):
        """
        Construct attributes for RadarSpace object

        Parameters
        ----------
            location : str
                a string representation of the grid location, eg. 'F7'
            board : Board object
                the board to which the space belongs
        """
        super().__init__(location, board)
        self._hit = 0

    @property
    def hit(self):
        """Return hit property"""
        return self._hit

    def note_guess(self, hit):
        """
        Mark space as guessed and mark hit attribute by argument passed.

        Parameters
        ----------
            hit : boolean
                indicates whether the guess was a hit
        Returns
        -------
        int - newly assigned self.hit value
        """
        # call method to check whether a guess was already placed and
        #   mark space as guessed
        self._validate_unguessed()
        if hit:
            self._hit = 2
        else:
            self._hit = 1
        return self.hit
