# Battleship Bot

## About the Project

When you play Battleship against another person, part of the thrill and disappointment is waiting for their response or looking at your board and having to give your response (like telling them they just got a hit or they just sunk your battleship). This is part of what makes Battleship a fun game to play. It's satisfying waiting for and then getting that response, and it's gut-wrenching having to give your response.

That experience is often lacking when you play Battleship against a computer. You don't get to tell your opponent whether they got a hit or a miss, the game just magically makes a red mark on one of your ships or a white mark in your open water.

I wanted to do something different. This is a command line app that plays a game of Battleship with you. You set up half of your board just like you were playing against another human, and the game doesn't know where anything is until you respond to its guesses (and given the possibility of a ship being sunk, the game will prompt you whether a ship was sunk when the computer gets a hit).

This project is still a work in progress. The game runs, and it will make guesses around a hit until confirmation of a sunken ship. Its main weakness right now is dealing with clustered ships. It doesn't currently follow up on stray hits or know how to determine to which player's ship the hits belong.

## Getting the App to Run

1. Make sure you have at least Python 3.8.4 installed on your computer or in a virtual environment. The app has not been tested with older versions, but should work fine with newer versions. You can find downloads and installation instructions on [the Python webpage](https://www.python.org/downloads/).
1. Clone this repo to your computer.
1. Navigate to the root of the project folder and run `pip install -r requirements.txt`.
1. Navigate to the root of the project folder and run `python app.py` from a shell (command prompt, powershell, bash, etc.).\*
    * Note: depending on which version(s) of Python you have installed, you may need to substitute `python` with `py` or `python3` to run the required version. If in doubt, run `python --version` with all three variations to see which one, if any, meet the requirement of 3.8.4 or later.
    * On Windows it's possible that you've installed Python but still get an error "python is not recognized as an internal or external command". If this happens, you need to add python to the environment variables:
        1. Browse your computer for the python installation (typically something like `C:\Program Files\Python39` or whatever version you installed).
        1. Open that folder and copy its path to your clipboard.
        1. Right click "This PC" and go to Properties -> Advanced system settings -> Environment Variables.
        1. Either select or add a "Path" Variable (if it doesn't already exist), then "Edit".
        1. In the "Edit Environment Variable" window, click add and paste the path you copied earlier.
        1. Click OK or Apply on that window, the Environment Variables window, and the System settings window.
1. Follow the on-screen instructions to play the game. You can type '-q' at any time to quit the application or '-h' at any time to bring up the help screen.

\* **One additional compatibility note:** The app is set up to clear the screen at regular intervals to provide a tidier and easier to follow experience. If you use *Git Bash* as your shell to run the application, this functionality may not work, but the app should function otherwise.

## Playing a Game

If you have a game of battleship in the house, set up half of it like you were sitting across from someone and then play against the computer in the app.

If you don't have a game of battleship handy, you can use the Google Sheets template I built instead, either printing out a copy or filling it out right in the browser:

https://docs.google.com/spreadsheets/d/1FnvfjBafRl1t-cBGJan1N3Vp_3ucJnNYCR-9fpPn0rg/edit?usp=sharing.

## Project Requirements

This project meets the following requirements for the Code Louisville Python Course:
* Utilizes a master loop allowing for repeated interactions and the option to quit the application at any time.
* Many classes are created and instantiated throughout, including Ship, Board, Space, and Opponent objects.
* Numerous functions/methods are included and called. Many of these functions have return values used by other parts of the application.
* Regular expressions are used to validate user guesses and get them ready for conversion
* Comments appear where clarification may be needed or to break up sections of code, and docstrings are applied throughout.

## Project Structure and Development

I spent most of my time up front developing modules for `ships` (and their `segments`), the `fleet`, which is a collection of ships, and the `board`, which is a collection of `spaces`. All of these modules come together in the `opponent` module, which is the heart of the game. This is where the computer's ships are randomly placed on one board and where the computer keeps track of its guesses on another board.

Initially, I thought the board would be an *Ordered Dictionary* of *Ordered Dictionaries* so the spaces could be found in `whatever_board_instance['letter'][number]`, but as I started writing the `Opponent` class, this made everything way too complicated. Now instead, it's a simple *List* of *Lists*, and the `gameconversions` module takes care of converting between zero-indexed positions for the computer and the more familiar A1-J10 coordinates for the player.

Once all those classes were constructed, I started building the main landing page, `app.py`. This is all more functional programming than the more object-oriented programming found in the modules, and this is where the help menu, player and computer turns, and main loop of the app are found.

### Continued Development

#### Some recent improvements I've made:
* The Opponent class now has additional methods that seek out the rest of a ship when a hit is made.
* Random guesses are now made in an every other space pattern (A1, A3, B2, B4, etc.) for greater efficiency.
* Random guesses are eliminated based on whether there would be room for the smallest remaining ship around the space.
* The possible sunken ship list presented to the user is further narrowed down by how many unaccounted hits are present (calculated by subtracting the total length of sunken ships from the total number of hits).

#### Some improvements I still want to make:
1. Right now, the hit list generator (which aids in finding the rest of a ship after a hit and eliminates possible guesses) adds up both vertical and horizontal possibilities. This means that a space could be listed as a possible guess when there is in fact not room for a ship in that area.
1. Clustered ships can confuse the opponent. It doens't currently know which hits go with which ship and it doesn't go back and seek around unaccounted for hits. For example, if it scores a hit on the Carrier because it's adjacent to the Battleship, and then sinks the Battleship, it doesn't know to go back and seek around that extra hit.
1. Right now, there is a 3 second delay to allow for reading messages after guesses on the player's turn, and no confirmation after player responses on the computer opponent's turn. There isn't currently a way to confirm or review the previous action, which could cause some issues if there's a mistyped command.
1. Add machine learning to make random guesses dependent on probability of a ship segment in that space.