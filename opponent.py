"""
Contains the Opponent and Turn classes.  The Opponent owns a radar
board and field board and includes all the methods for randomly placing
its ships and hunting for the player's ships.

Classes
-------
Opponent
    A class for the computer opponent in a game of Battleship
Turn
    Used by the Opponent class to keep track of its guesses
"""

import random

from board import Board
from fleet import Fleet
from ships import Ship


class Opponent:
    """
    A class to represent the computer opponent.

    Attributes
    ----------
    radar_board : Board object
        a board for tracking guesses
    radar_fleet : Fleet object
        a fleet to track which player ships have been destroyed
    field_board : Board object
        a board for placing the opponent's ships and taking player guesses
    field_fleet : Fleet object
        a fleet containing the opponent's ships to track player hits

    Properties
    ----------
    total_hits : int
        the number of hits made by the computer throughout the game
    spare_hits : int
        the number of hits made by computer and not tied to a sunken ship
    last_guess : Turn object
        the most recently made guess
    """
    def __init__(self):
        """Builds a new Opponent object. Takes no arguments."""
        self.radar_board = Board('radar')
        self.radar_fleet = Fleet()

        self._destroy_mode = False
        self._guess_list = []
        self._hit_list = []
        # _guess_seed determines evens or odds for _seek_ships method
        #   and order of row and column hits in _hit_list
        self._guess_seed = random.randint(0, 1)

        self.field_board = Board('field')
        self.field_fleet = Fleet()
        self._place_ships()


    # ------------Setup Methods------------ #
    def _place_ships(self):
        """Place every ship in the opponent's fleet on the board."""
        for ship in self.field_fleet:
            self._place_ship(ship)

    def _place_ship(self, ship):
        """Place a single ship on the board randomly."""
        row = random.randint(0, len(self.field_board) - 1)
        column = random.randint(0, len(self.field_board[0]) - 1)
        rotate = random.randint(0, 1)
        if rotate:
            ship.rotate()
        if self._check_spaces(row, column, ship):
            if ship.orientation == 'h':
                for index, segment in enumerate(ship.segments):
                    self.field_board[row][column + index].segment = segment
            if ship.orientation == 'v':
                for index, segment in enumerate(ship.segments):
                    self.field_board[row + index][column].segment = segment
        else:
            self._place_ship(ship)

    def _check_spaces(self, row, column, ship):
        """Check if spaces are available at given starting space for ship."""
        if ship.orientation == 'h':  # if ship is horizontal
            for index in range(len(ship)):
                # If any proposed space for a ship does not exist
                #   or is already occupied, stop the for loop and
                #   return False from the method.
                try:
                    if (column + index) >= len(self.field_board[row]):
                        return False
                    elif self.field_board[row][column + index].segment:
                        return False
                except IndexError:
                    print(
                        "Starting space is outside the range of the board.")
        else:  # if ship is vertical
            for index in range(len(ship)):
                try:
                    if (row + index) >= len(self.field_board):
                        return False
                    elif self.field_board[row + index][column].segment:
                        return False
                except IndexError:
                    print(
                        "Starting space is outside the range of the board.")
        return True


    # ------------Helper Methods------------ #
    @property
    def total_hits(self):
        """Return the total number of hits made by Opponent."""
        total = 0
        for guess in self._guess_list:
            if guess.hit:
                total += 1
        return total

    @property
    def spare_hits(self):
        """Return number of hits not accounted for in sunk ships."""
        total_sunk_hits = 0
        for ship in self.radar_fleet.ships_sunk:
            total_sunk_hits += len(ship)
        return self.total_hits - total_sunk_hits

    def possible_sunk(self):
        """Return list of possibly sunk ships from radar board."""
        longest_possible = 0
        # check horizontally adjacent hits on each row
        for row in range(len(self.radar_board)):
            row_counter = 0
            for column in range(len(self.radar_board[row])):
                if self.radar_board[row][column].hit == 2:
                    row_counter += 1
                    if column + 1 >= len(self.radar_board[row]):
                        if row_counter > longest_possible:
                            longest_possible = row_counter
                        row_counter = 0
                else:
                    if row_counter > longest_possible:
                        longest_possible = row_counter
                    row_counter = 0
        # check vertically adjacent hits on each column
        for column in range(len(self.radar_board[0])):
            column_counter = 0
            for row in range(len(self.radar_board)):
                if self.radar_board[row][column].hit == 2:
                    column_counter += 1
                    if row + 1 >= len(self.radar_board):
                        if column_counter > longest_possible:
                            longest_possible = column_counter
                        column_counter = 0
                else:
                    if column_counter > longest_possible:
                        longest_possible = column_counter
                    column_counter = 0
        # check longest_possible against number of hits not already
        #   tied to a sunken ship
        unaccounted_hits = self.spare_hits
        if unaccounted_hits < longest_possible:
            longest_possible = unaccounted_hits
        return [ship for ship in self.radar_fleet.ships_remaining
                 if len(ship) <= longest_possible]

    def _horizontal_hit_list(self, starting_row, starting_column,
                             longest_unsunk):
        """Add potential hits right and left of starting point."""
        # gather potential hits in row to right of start
        for index in range(longest_unsunk):
            if (starting_column + index >= len(
                    self.radar_board[0])):
                break
            space = self.radar_board[starting_row][
                            starting_column + index]
            if space.hit == 1:
                break
            elif space.hit == 0:
                self._hit_list.append((starting_row,
                                        starting_column + index))
        # gather potential hits in row to left of start
        for index in range(longest_unsunk):
            if starting_column - index < 0:
                break
            space = self.radar_board[starting_row][
                            starting_column - index]
            if space.hit == 1:
                break
            elif space.hit == 0:
                self._hit_list.append((starting_row,
                                        starting_column - index))

    def _vertical_hit_list(self, starting_row, starting_column,
                             longest_unsunk):
        """Add potential hits above and below starting point."""
        # gather potential hits in column below start
        for index in range(longest_unsunk):
            if (starting_row + index >= len(
                    self.radar_board)):
                break
            space = self.radar_board[starting_row + index][
                                     starting_column]
            if space.hit == 1:
                break
            elif space.hit == 0:
                self._hit_list.append((starting_row + index,
                                        starting_column))
        # gather potential hits in column above start
        for index in range(longest_unsunk):
            if starting_row - index < 0:
                break
            space = self.radar_board[starting_row - index][
                                     starting_column]
            if space.hit == 1:
                break
            elif space.hit == 0:
                self._hit_list.append((starting_row - index,
                                       starting_column))

    def _build_hit_list(self, starting_row=None, starting_column=None):
        """
        Build a hit list to assist the _destroy_ship method.

        Parameters
        ----------
        starting_row : int, optional | default: None
            starting row to use _hit_list for evaluating new guesses
        starting_column : int, optional | default: None
            starting column to use _hit_list for evaluating new guesses

        Returns
        -------
        boolean - indicates whether list was successfully created.
        """
        if not starting_row or not starting_column:
            starting_point = None
            # Go through the _guess_list in reverse order to check for the
            #   first hit in the current ship destroying cycle.
            for guess in reversed(self._guess_list):
                if guess.sunk:
                    # when a sunk guess appears, this means the starting
                    #   point has passed.
                    break
                elif guess.hit:
                    starting_point = guess
            if not starting_point:
                self._destroy_mode = False
                self._hit_list.clear()
                return False
            starting_row = starting_point.row
            starting_column = starting_point.column
        ships_remaining = self.radar_fleet.ships_remaining
        longest_unsunk = max([len(ship) for ship in ships_remaining])
        # randomly decide whether to start with horizontal or vertical hits
        if self._guess_seed:
            # gather potential hits in row around start
            self._horizontal_hit_list(starting_row, starting_column,
                                    longest_unsunk)
            # gather potential hits in column around start
            self._vertical_hit_list(starting_row, starting_column,
                                    longest_unsunk)
        else:
            # gather potential hits in column around start
            self._vertical_hit_list(starting_row, starting_column,
                                    longest_unsunk)
            # gather potential hits in row around start
            self._horizontal_hit_list(starting_row, starting_column,
                                    longest_unsunk)
        if len(self._hit_list):
            return True
        else:
            return False

    @property
    def last_guess(self):
        """
        Return the last guess made by the computer.

        Returns
        -------
        Turn object or None - None is returned if no guesses have been made
        """
        if len(self._guess_list):
            return self._guess_list[-1]
        else:
            return None


    # ------------Seeking Methods------------ #
    def _destroy_ship(self):
        """Return tuple of row and column coordinates from the _hit_list."""
        if not self.last_guess.hit:
            self._hit_list.clear()
            self._build_hit_list()
        elif self.last_guess.sunk:
            self._hit_list.clear()
            self._destroy_mode = False
            return self.make_guess()
        if len(self._hit_list):
            return self._hit_list.pop(0)
        else:
            # If there are no items in _hit_list, call method to build list
            if self._build_hit_list():
                return self._destroy_ship()
            else:
                self._destroy_mode = False
                return self.make_guess()

    def _seek_ships(self):
        """
        Return tuple of row and column coordinates for guesses.

        Currently uses a lattice grid for efficient searching.  This
        works by guessing only even columns with even rows and only odd
        columns with odd rows.  It also eliminates possibilities where
        there aren't enough potential hits around a space.  This is
        incomplete since it adds row and column possibilities together,
        but it does narrow down the possibilities.

        Note: Currently will only work with even row lengths on the
        radar board.

        Returns
        -------
        two-tuple of int - row and column guess coordinates
        """
        row = random.randint(0, len(self.field_board) - 1)
        # make column even
        column = random.randint(0, int((len(self.field_board[0]) / 2)) - 1)
        column = column * 2
        # if row is odd, make column odd (reverses with _guess_seed value)
        if (row + self._guess_seed) % 2 != 0:
            column += 1
        if self.radar_board[row][column].guessed:
            # make a new guess if the space has already been guessed
            return self._seek_ships()
        # build hit list around proposed guess
        self._build_hit_list(row, column)
        # determine length of shortest remaining ship
        ships_remaining = self.radar_fleet.ships_remaining
        shortest_unsunk = min([len(ship) for ship in ships_remaining])
        # check if there's room for the shortest remaining ship around
        #   the proposed guess
        if len(self._hit_list) + self.spare_hits >= shortest_unsunk:
            self._hit_list.clear()
            return row, column
        else:
            # if there isn't room, generate another guess
            self._hit_list.clear()
            return self._seek_ships()

    def make_guess(self):
        """
        Make a guess based on existing guesses.

        Returns
        -------
        tuple of two int
            zero-indexed row and column for guess
        """
        if self.last_guess:
            if self.last_guess.sunk:
                self._destroy_mode = False
                self._hit_list.clear()
            elif self.last_guess.hit:
                self._destroy_mode = True
        if self._destroy_mode:
            row, column = self._destroy_ship()
        else:
            row, column = self._seek_ships()
        return row, column

    def take_guess_answer(self, row, column, hit):
        """
        Take the result of a guess to mark it down on radar.

        Parameters
        ----------
            row : int
                a zero-indexed row for the guess
            column : int
                a zero-indexed column for the guess
            hit : boolean
                indicates whether the guess was a hit

        Returns
        -------
        None
        """
        try:
            self.radar_board[row][column].note_guess(hit)
        except TypeError as typeerror:
            print(typeerror)
        else:
            self._guess_list.append(Turn(self.radar_board[row][column],
                                    row, column))

    def take_sunk_answer(self, ship):
        """Mark a ship sunk on the previous guess.

        Parameters
        ----------
        ship : Ship object or None
            Indicates the ship sunk on that guess or None for no ship sunk.
        """
        if isinstance(ship, Ship) or ship is None:
            self.last_guess.sunk = ship
        else:
            raise TypeError("'ship' argument must be None or Ship object.")


    # ------------Additional Dunder Methods------------ #
    def __str__(self):
        """Return string representation for announcements."""
        return "The Computer"


class Turn:
    """
    Class for keeping track of the result of the computer's turn.

    Attributes
    ----------
    space : Space object
        space associated with turn
    row : int
        row number associated with turn
    column : int
        column number associated with turn

    Properties
    ----------
    sunk : Ship object or None
        indicates if a ship was sunk on that guess
    hit : boolean
        indicates whether the guess was a hit on the turn
    """
    def __init__(self, space, row, column):
        """
        Build a Turn object.

        Parameters
        ----------
        space : Space object
            the space associated with the guess
        row : int
            the row associated with the guess
        column : int
            the column associated with the guess
        """
        self.space = space
        self.row = row
        self.column = column
        self._sunk = None

    @property
    def sunk(self):
        """Return sunk property"""
        return self._sunk

    @sunk.setter
    def sunk(self, ship=None):
        """
        Set sunk property
    
        Parameters
        ----------
        ship : Ship object or None, optional | default: None
            indicates the ship that was sunk, if any, on the guess
        """
        if isinstance(ship, Ship) or ship is None:
            self._sunk = ship
        else:
            raise TypeError("'ship' argument must be None or Ship object.")

    @property
    def hit(self):
        """Return boolean indicating whether guess was a hit."""
        if self.space.hit == 2:
            return True
        else:
            return False
