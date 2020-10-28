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
    """
    def __init__(self):
        """Builds a new Opponent object. Takes no arguments."""
        self.radar_board = Board('radar')
        self.radar_fleet = Fleet()

        self._destroy_mode = False
        self._guess_list = []
        self._hit_list = []

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
        return [ship for ship in self.radar_fleet.ships_remaining
                 if len(ship) <= longest_possible]
    
    def _build_hit_list(self):
        """Build a hit list to assist the _destroy_ship method."""
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
            self.make_guess()
            return
        starting_row = starting_point.row
        starting_column = starting_point.column
        ships_remaining = self.radar_fleet.ships_remaining
        longest_unsunk = max([len(ship) for ship in ships_remaining])
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
    
    @property
    def last_guess(self):
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
        if self.last_guess.sunk:
            self._hit_list.clear()
            self._destroy_mode = False
            return self.make_guess()
        if len(self._hit_list):
            return self._hit_list.pop(0)
        else:
            # If there are no items in _hit_list, call method to build list
            self._build_hit_list()
            if len(self._hit_list):
                return self._destroy_ship()
            else:
                self._destroy_mode = False
                return self.make_guess()

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
            row = random.randint(0, len(self.field_board) - 1)
            column = random.randint(0, len(self.field_board[0]) - 1)
        if self.radar_board[row][column].guessed:
            return self.make_guess()
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
        if isinstance(ship, Ship) or ship is None:
            self.last_guess.sunk = ship
        else:
            raise TypeError("'ship' argument must be None or Ship object.")


    # ------------Additional Dunder Methods------------ #
    def __str__(self):
        """Return string representation for announcements."""
        return "The Computer"


class Turn:
    def __init__(self, space, row, column):
        self.space = space
        self.row = row
        self.column = column
        self._sunk = None
    
    @property
    def sunk(self):
        return self._sunk
    
    @sunk.setter
    def sunk(self, ship=None):
        if isinstance(ship, Ship) or ship is None:
            self._sunk = ship
        else:
            raise TypeError("'ship' argument must be None or Ship object.")

    @property
    def hit(self):
        if self.space.hit == 2:
            return True
        else:
            return False