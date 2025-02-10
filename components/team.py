from enum import Enum

from components.player import Player


class Position(Enum):
    OFF = "offence"
    DEF = "defence"


class Team:

    def __init__(self, one: Player, two: Player):
        self.player_one: Player = one
        self.player_two: Player = two

    def __str__(self):
        return f"{self.player_one} & {self.player_two}"

    def name(self, match_uid):
        #if self.player_one is None or self.player_two is None:
        #    return f"{self.player_one} {self.player_two}"
        return f"{self.player_one.with_joker(match_uid)} + {self.player_two.with_joker(match_uid)}"
