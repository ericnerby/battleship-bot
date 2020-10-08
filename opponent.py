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

    def _check_spaces(self, starting_space, length, orientation):
        pass