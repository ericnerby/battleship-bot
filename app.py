import os
import random
import re
import sys

from gameconversions import ConvertFromIndex, ConvertToIndex
from opponent import Opponent


WELCOME_SCREEN = """
Welcome to Battleship!
----------------------
Please set up your board by placing all your ships and get ready to
play a great game of battleship.  To quit at anytime, type '-q' and hit
Enter. To bring up the help menu, type '-h'.  Otherwise, please
follow the prompts throughout and have fun!

"""


class Player:
    def __init__(self, name):
        self.name = name
    
    def __str__(self):
        return self.name


def clear():
    """Clear screen in terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')


def check_help_and_quit(user_input):
    if re.match(r'-q', user_input):
        sys.exit([0])
    elif re.match(r'-h', user_input):
        # bring up help screen
        pass


def player_turn():
    """What happens when it's the player's turn."""
    pass


def opponent_turn():
    """What happens when it's the computer's turn."""
    pass


def check_for_win():
    """Check to see if there's a winner."""
    winner = None
    if opponent.field_fleet.defeated:
        winner = player
    if opponent.radar_fleet.defeated:
        winner = opponent
    return winner


def display_field():
    # display the opponent's field
    pass


def game_loop(starting_player):
    next_player = starting_player
    while True:
        clear()
        if next_player == player:
            player_turn()
            next_player = opponent
        else:
            opponent_turn()
            next_player = player
        winner = check_for_win()
        if winner:
            print("The winner is... {}!".format(winner))
            display_field()
            break


def main():
    clear()
    if random.randint(0, 1):
        starting_player = opponent
        print(
            "Thank you, {}!\n".format(player)
            + "The computer has been randomly selected to go first.")
    else:
        starting_player = player
        print(
            "Thank you, {}!\n".format(player)
            + "You have been randomly selected to go first.")
    user_input = input("Hit Enter to begin.")
    check_help_and_quit(user_input)
    game_loop(starting_player)


if __name__ == '__main__':
    opponent = Opponent()
    name = None
    clear()
    print(WELCOME_SCREEN)
    while not name:
        name = input(
            "Before we get started, could you please tell me your name? ")
        check_help_and_quit(name)
        if not len(name):
            name = None
    player = Player(name)
    main()