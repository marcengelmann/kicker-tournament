from __future__ import annotations

from components.team import Team, Position


class Match:

    def __init__(self, orange: Team, blue: Team, uid: int, round_uid: int):
        self.team_orange: Team = orange
        self.team_blue: Team = blue
        self.uid: int = uid
        self.round_uid: int = round_uid
        self.team_orange_score: int = 0
        self.team_blue_score: int = 0
        self.team_blue_player_one: Position | None = None
        self.team_orange_player_one: Position | None = None

    def __str__(self):
        return f"Match {self.uid} ({self.score})"

    @property
    def score(self):
        if self.team_blue_score == 0 and self.team_orange_score == 0:
            return "-:-"
        else:
            return f"{self.team_orange_score}:{self.team_blue_score}"
