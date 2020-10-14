import random

from board import Board
from fleet import Fleet


class Opponent:
    def __init__(self):
        self.radar_board = Board('radar')
        self.radar_fleet = Fleet()
        self._last_guessed = None

        self.field_board = Board('field')
        self.field_fleet = Fleet()
        self._place_ships()

    # ------------Setup Methods------------ #
    def _place_ships(self):
        for ship in self.field_fleet:
            self._place_ship(ship)

    def _place_ship(self, ship):
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

    # ------------Seeking Methods------------ #
    def make_guess(self):
        row = random.randint(0, len(self.field_board) - 1)
        column = random.randint(0, len(self.field_board[0]) - 1)
        if self.radar_board[row][column].guessed:
            return self.make_guess()
        return row, column
    
    def take_guess_answer(self, row, column, hit):
        try:
            self.radar_board[row][column].note_guess(hit)
        except TypeError as typeerror:
            print(typeerror)
        else:
            self._last_guessed = self.radar_board[row][column]