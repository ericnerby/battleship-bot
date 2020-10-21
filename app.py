import os
import random
import re
import sys
import time

from gameconversions import convert_from_index, convert_to_index
from opponent import Opponent


WELCOME_SCREEN = r"""
       . |_
 __=n_[]_[_]_n=_  Welcome to Battleship!
 \_____________/  ----------------------

Please set up your board by placing all your ships and get ready to
play a great game of battleship.  If you don't have a physical game of
battleship available, you can grab a paper/digital sheet here:

https://docs.google.com/spreadsheets/d/1FnvfjBafRl1t-cBGJan1N3Vp_3ucJnNYCR-9fpPn0rg/edit?usp=sharing

To quit at anytime, type '-q' and hit Enter.  To bring up the help
menu, type '-h'.  Otherwise, please follow the prompts throughout
and have fun!

"""

# --------- Helper Functions --------- #
class Player:
    """Create a Player for the game."""
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


def clear():
    """Clear screen in terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')


def sleeper():
    """Pause code execution for three seconds."""
    time.sleep(3)


def check_help_and_quit(user_input):
    """Check user input for help or quit command and execute if present."""
    if re.match(r'-q', user_input):
        sys.exit()
    elif re.match(r'-h', user_input):
        # bring up help screen
        pass


def display_field():
    # display the opponent's field
    pass


# --------- Game Play Functions --------- #
def check_for_win():
    """Return the winner of the game or None if no winner."""
    winner = None
    if opponent.field_fleet.defeated:
        winner = player
    if opponent.radar_fleet.defeated:
        winner = opponent
    return winner


def player_turn():
    """Take player's guess, mark it, and provide feedback."""
    clear()
    player_input = input("Please enter your guess in the format 'A1': ")
    check_help_and_quit(player_input)
    player_guess = re.match(r'([a-zA-Z])(\d+)', player_input)
    if player_guess:
        row_guess, column_guess = player_guess.group(1, 2)
        row_guess, column_guess = convert_to_index(row_guess, column_guess)
        if (row_guess >= len(opponent.field_board)
                or column_guess >= len(opponent.field_board[0])
                or row_guess < 0 or column_guess < 0):
            print("Your guess was outside of the range of the board.")
            sleeper()
            player_turn()
        segment = opponent.field_board[row_guess][column_guess].take_guess()
        if segment:
            print("'{}' is a hit!".format(player_guess))
            ship = segment.ship
            if ship.sunk:
                print("You sunk my {}!".format(ship))
        else:
            print("'{}' is a miss!".format(player_guess))
    else:
        print(
           "Please make sure you're entering your guess in the format 'A1'.")
        sleeper()
        player_turn()


def opponent_turn():
    """What happens when it's the computer's turn."""
    player_input = input("Computer's turn")
    check_help_and_quit(player_input)


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


# --------- Game Setup --------- #
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
