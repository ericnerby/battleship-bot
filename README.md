# Battleship Bot

## About the Project

When you play Battleship against another person, part of the thrill and disappointment is waiting for their response or looking at your board and having to give your response (like telling them they just got a hit or they just sunk your battleship). This is part of what makes Battleship a fun game to play. It's satisfying waiting for and then getting that response, and it's gut-wrenching having to give your response.

That experience is often lacking when you play Battleship against a computer. You don't get to tell your opponent whether they got a hit or a miss, the game just magically makes a red mark on one of your ships or a white mark in your open water.

I wanted to do something different. This is a command line app that plays a game of Battleship with you. You set up half of your board just like you were playing against another human, and the game doesn't know where anything is until you respond to its guesses (and given the possibility of a ship being sunk, the game will prompt you whether a ship was sunk when the computer gets a hit).

As you can see, I'm slowly building the game right now (as a project for my Code Louisville Python course), so check back later and hopefully there will be a fun game waiting for you in the future!

## Getting the App to Run

1. Make sure you have at least Python 3.8.4 installed on your computer. The app has not been tested with older versions, but should work fine if you've already upgraded to 3.9.0. You can get the installers and find instructions for installation on [the Python webpage](https://www.python.org/downloads/).
1. Clone this repo to your computer.
1. Navigate to the root of the project folder and run `python app.py` from a shell (command prompt, powershell, bash, etc.).\*
    * Note: depending on which version(s) of Python you have installed, you may need to substitute `python` with `py` or `python3` to run the required version. If in doubt, run `python --version` with all three variations to see which one, if any, meet the requirement of 3.8.4 or later.
    * On Windows it's possible that you've installed Python but still get an error "python is not recognized as an internal or external command". If this happens, you need to add python to the environment variables:
        1. Browse your harddrive for the python installation (typically something like `C:\Program Files\Python39` or whatever version you installed)
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