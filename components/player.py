from components.color_stats import ColorStats
from components.position_stats import PositionStats


class Player:

    @property
    def dif(self):
        return self.goals_shot - self.goals_received

    @property
    def points(self):
        return self.blue.points + self.orange.points

    @property
    def played(self):
        return self.blue.played + self.orange.played

    @property
    def draws(self):
        return self.blue.draws + self.orange.draws

    @property
    def wins(self):
        return self.blue.wins + self.orange.wins

    @property
    def goals_shot(self):
        return self.blue.goals_scored + self.orange.goals_scored

    @property
    def goals_received(self):
        return self.blue.goals_received + self.orange.goals_received

    @property
    def max_goals_received(self):
        return max(self.blue.most_goals_per_match_received, self.orange.most_goals_per_match_received)

    @property
    def min_goals_received(self):
        return min(self.blue.least_goals_per_match_received, self.orange.least_goals_per_match_received)

    @property
    def min_goals_scored(self):
        return min(self.blue.min_goals_scored_per_match, self.orange.min_goals_scored_per_match)

    def __init__(self, uid: int, name: str):
        self.uid: int = uid
        self.is_joker: bool = "joker" in name.lower()

        self.name: str = name
        self.joker_players: {int: Player} = {}

        self.blue: ColorStats = ColorStats()
        self.orange: ColorStats = ColorStats()

        self.offence: PositionStats = PositionStats()
        self.defence: PositionStats = PositionStats()

    def __str__(self):
        return f"{self.name}"

    def with_joker(self, match_uid: int):
        if match_uid in self.joker_players.keys():
            return f"({self.joker_players[match_uid]})"
        else:
            return str(self)
