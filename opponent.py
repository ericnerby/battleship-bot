import random

from board import Board
from fleet import Fleet


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
        self.radar_board = Board('radar')
        self.radar_fleet = Fleet()
        self._last_guessed = None

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
    def possible_sunk(row, column):
        possible_sunk_list = []
        for ship in self.radar_fleet.ships_remaining:
            ship_length = len(ship)
            # check horizontal right
            if column + ship_length <= len(self.radar_board[0]):
                if all([self.radar_board[row][column + index].hit == 2
                            for index in range(ship_length)]):
                    possible_sunk_list.append(ship)
                    continue
            # check horizontal left
            if column - ship_length >= -1:
                if all([self.radar_board[row][column - index].hit == 2
                            for index in range(ship_length)]):
                    possible_sunk_list.append(ship)
                    continue
            # check vertical down
            if row + ship_length <= len(self.radar_board):
                if all([self.radar_board[row + index][column].hit == 2
                            for index in range(ship_length)]):
                    possible_sunk_list.append(ship)
                    continue
            # check vertical up
            if column - ship_length >= -1:
                if all([self.radar_board[row + index][column].hit == 2
                            for index in range(ship_length)]):
                    possible_sunk_list.append(ship)
                    continue
        return possible_sunk_list

    # ------------Seeking Methods------------ #
    def make_guess(self):
        """
        Make a guess based on existing guesses.

        Returns
        -------
        tuple of two int
            zero-indexed row and column for guess
        """
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
            self._last_guessed = self.radar_board[row][column]

    # ------------Additional Dunder Methods------------ #
    def __str__(self):
        """Return string representation for announcements."""
        return "The Computer"