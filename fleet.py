"""
Contains the Fleet class for a Battleship game.

The Fleet class instantiates one of each Ship subclass and tracks the
status of a player's ships.

Classes
-------
Fleet
    A list of one player's ships with some properties for tracking
"""

from ships import Battleship, Carrier, Destroyer, PTBoat, Submarine


class Fleet(list):
    """
    A list of one player's ships with some properties for tracking

    Properties
    ----------
    defeated : boolean
        indicates whether all ships in fleet have been sunk
    ships_remaining : list
        a list of all ships which have not been sunk
    """
    def __init__(self, *args, **kwargs):
        """Construct attributes for Fleet object."""
        super().__init__(*args, **kwargs)
        self.append(Battleship())
        self.append(Carrier())
        self.append(Destroyer())
        self.append(PTBoat())
        self.append(Submarine())

    @property
    def defeated(self):
        """Indicates whether all ships in fleet have been sunk."""
        return all([ship.sunk for ship in self])

    @property
    def ships_remaining(self):
        """A list of all ships which have not been sunk"""
        return [ship for ship in self if not ship.sunk]
