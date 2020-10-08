import random
from string import ascii_lowercase as alphabet

from board import Board
from fleet import Fleet


class Opponent:
    row_letters = alphabet[:10]

    def __init__(self):
        self.radar_board = Board('radar')
        self.radar_fleet = Fleet()

        self.field_board = Board('field')
        self.field_fleet = Fleet()

    def place_ships(self):
        for ship in self.field_fleet:
            letter = random.choice(Opponent.row_letters)
            number = random.randint(1, 11)
            rotate = random.randint(0, 1)
            if rotate:
                ship.rotate()
            if self._check_spaces(letter, number, ship):
                # assign segments to spaces
                pass

    def _check_spaces(self, letter, number, ship):
        """Check if spaces are available at given starting space for ship."""
        if ship.orientation == 'h':  # if ship is horizontal
            for index, _ in enumerate(ship.segments, 0):
                # If any proposed space for a ship does not exist
                #   or is already occupied, stop the for loop and
                #   return False from the method.
                if (number + index >= len(self.field_board[letter])
                    or self.field_board[letter][number + index].segment):
                    return False
        else:  # if ship is vertical
            letter_index = Opponent.row_letters.index(letter)
            for index, _ in enumerate(ship.segments, 0):
                # If any proposed space for a ship does not exist
                #   or is already occupied, stop the for loop and
                #   return False from the method.
                try:
                    loop_letter = Opponent.row_letters[letter_index + index]
                except:
                    return False
                if self.field_board[loop_letter][number].segment:
                    return False
        return True
