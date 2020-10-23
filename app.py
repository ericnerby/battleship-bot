import os
import random
import re
import sys
import time

from gameconversions import convert_from_index, convert_to_index
from opponent import Opponent

WAIT_TIME = 3

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

HELP_STRING = """
HELP
----

To quit at anytime, type '-q' and hit Enter.
To bring up this menu, enter '-h'.

When it is your turn, enter your guess as a letter followed by a number
with no spaces or characters in between (eg 'a1'or 'B10') and hit Enter
to submit your guess.  The computer's response to your guess will
display for {} seconds.  A space that you have already guessed will
not be accepted.

When it is the computer's turn, respond to the computer's guess with
'h' for hit or 'm' for miss.  The default will be miss if you don't
enter a recognized command.  If a sunken ship is possible, you'll
receive an additional prompt with a numbered list of possible ships.
If there is no sunken ship at that time, you can simply hit Enter
without a number or type '0'.
""".format(WAIT_TIME)


# --------- Helper Functions --------- #
class Player:
    """Create a Player for the game."""
    def __init__(self, name):
        self.name = name

    def __str__(self):
        """Return name when Player object printed"""
        return self.name


def clear():
    """Clear screen in terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')


def sleeper():
    """Pause code execution for seconds stored in WAIT_TIME."""
    time.sleep(WAIT_TIME)


def check_help_and_quit(user_input):
    """
    Check user input for help or quit command and execute if present.
    
    If the help menu is called, the function returns True.  If the quit
    command is called, the program closes in this function.  Otherwise,
    the function returns False.

    Returns
    -------
    boolean - indicates whether the help menu was called and displayed.
    """
    if re.match(r'-q', user_input):
        sys.exit()
    elif re.match(r'-h', user_input):
        print(HELP_STRING)
        _ = input("Hit Enter to return to game.")
        return True
    return False


def display_field():
    # TODO-display the opponent's field
    pass


# --------- Game Play Functions --------- #
def check_for_win():
    """Return the winner of the game or None if no winner."""
    winner = None
    if opponent.field_fleet.defeated:
        winner = player
    elif opponent.radar_fleet.defeated:
        winner = opponent
    return winner


def player_turn():
    """Take player's guess, mark it, and provide feedback."""
    clear()
    player_input = input("Please enter your guess in the format 'A1': ")
    if check_help_and_quit(player_input):
        # if the help menu is called, the player's turn starts
        #     over after the help menu closes.
        player_turn()
        return
    player_guess = re.match(r'([a-zA-Z])(\d+)', player_input)
    # check input for correct format
    if player_guess:
        row_guess, column_guess = player_guess.group(1, 2)
        row_guess, column_guess = convert_to_index(row_guess, column_guess)
        # check that input is inside range of board
        if (row_guess >= len(opponent.field_board)
                or column_guess >= len(opponent.field_board[0])
                or row_guess < 0 or column_guess < 0):
            print("Your guess was outside of the range of the board.")
            sleeper()
            player_turn()
            return
        # check if space was already guessed by player previously
        if opponent.field_board[row_guess][column_guess].guessed:
            if opponent.field_board[row_guess][column_guess].segment:
                prev_guess_status = 'hit'
            else:
                prev_guess_status = 'miss'
            print("You've already guessed {}. It was a {}".format(
                player_input, prev_guess_status))
            sleeper()
            player_turn()
            return
        # check space for hit or miss
        segment = opponent.field_board[row_guess][column_guess].take_guess()
        if segment:
            print("'{}' is a hit!".format(player_input))
            segment.hit = True
            ship = segment.ship
            if ship.sunk:
                print("You sunk my {}!".format(ship))
        else:
            print("'{}' is a miss!".format(player_input))
        sleeper()
    else:
        print(
           "Please make sure you're entering your guess in the format 'A1'.")
        sleeper()
        player_turn()


def opponent_turn(existing_row=None, existing_column=None):
    """
    Make guess, prompt player, and mark guess.
    
    Parameters
    ----------
        existing_row : int, optional | default: None
        existing_column : int, optional | default: None
            these two parameters allow existing guess to be entered
            instead of a new guess for the purpose of recursion
    """
    clear()
    if existing_row is None and existing_column is None:
        row_guess, column_guess = opponent.make_guess()
    else:
        row_guess = existing_row
        column_guess = existing_column
    print("I'm going to guess... {}{}.".format(
        convert_from_index(row_guess, 'upper'),
        convert_from_index(column_guess, 'one')))
    player_input = input("'h' for hit, 'm' for miss. [M/h] ")
    if check_help_and_quit(player_input):
        # If the help menu is called, the opponent's turn starts over
        #     but with the existing guess loaded.
        opponent_turn(row_guess, column_guess)
    if re.match(r'h', player_input, re.I):
        opponent.take_guess_answer(row_guess, column_guess, True)
        # TODO-On a hit, present additional prompt asking if a ship was sunk.
    else:
        opponent.take_guess_answer(row_guess, column_guess, False)


def game_loop(starting_player):
    """
    Main loop of the game calls player and opponent turns until game over.
    
    Each cycle through the loop switches between player and opponent
    turns and checks for a winner.  When there's a winner, it will be
    announced, the opponent's field displayed, and the loop will break.

    Parameters
    ----------
        starting_player : object
            determines whether the player or the opponent will have the
                first turn of the game
    """
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
    user_name = None
    clear()
    print(WELCOME_SCREEN)
    while not user_name:
        user_name = input(
            "Before we get started, could you please tell me your name? ")
        check_help_and_quit(user_name)
        if not len(user_name):
            user_name = None
    player = Player(user_name)
    main()
