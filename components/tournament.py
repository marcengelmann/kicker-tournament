from __future__ import annotations

import math

from components.color_stats import ColorStats
from components.match import Match
from components.player import Player
from components.position_stats import PositionStats
from components.team import Team, Position


class Tournament:

    def __init__(self):
        self.matches: [Match] = []
        self.players: [Player] = []
        self.matches_played: int = 0
        self.title = "Kicker Tournament"
        self.number_of_rounds: int = 0

    @property
    def total_matches(self):
        return len(self.matches)

    def get_player(self, uid: int):
        plr: Player
        for plr in self.players:
            if plr.uid == uid:
                return plr

    def get_match(self, uid: int):
        mtch: Match
        for mtch in self.matches:
            if mtch.uid == uid:
                return mtch

    def set_players(self, players: [str]):
        self.players.clear()
        uid_counter = 1
        for player_str in players:
            self.players.append(Player(uid_counter, player_str))
            uid_counter += 1

    def add_score(self,
                  uid: int,
                  orange: int,
                  blue: int,
                  blue_one: Position,
                  orange_one: Position,
                  joker_blue: int | None = None,
                  joker_orange: int | None = None):

        match: Match = self.get_match(uid)
        match.team_blue_score = blue
        match.team_orange_score = orange

        match.team_blue_player_one = blue_one
        match.team_orange_player_one = orange_one

        if joker_blue:
            if match.team_blue.player_one.is_joker:
                match.team_blue.player_one.joker_players[uid] = self.get_player(joker_blue)
            else:
                match.team_blue.player_two.joker_players[uid] = self.get_player(joker_blue)

        if joker_orange:
            if match.team_orange.player_one.is_joker:
                match.team_orange.player_one.joker_players[uid] = self.get_player(joker_orange)
            else:
                match.team_orange.player_two.joker_players[uid] = self.get_player(joker_orange)

        self.matches_played += 1

    def add_hard_coded_round(self, set_plan: str):
        set_plan: [str] = set_plan.replace("\t", ";").split(";")

        number_of_matches: int = int(len(set_plan) / 2)

        for i in range(number_of_matches):
            i *= 2

            team_orange: str = set_plan[i]
            team_blue: str = set_plan[i + 1]

            player_one_blue: Player = self.get_player(int(team_blue.split("-")[0]))
            player_two_blue: Player = self.get_player(int(team_blue.split("-")[1]))
            player_one_orange: Player = self.get_player(int(team_orange.split("-")[0]))
            player_two_orange: Player = self.get_player(int(team_orange.split("-")[1]))

            self.matches.append(Match(orange=Team(one=player_one_orange, two=player_two_orange),
                                      blue=Team(one=player_one_blue, two=player_two_blue),
                                      uid=len(self.matches) + 1,
                                      round_uid=math.ceil((len(self.matches) + 1) / len(set_plan) * 2)))

        self.number_of_rounds += 1

    def evaluate_results(self):
        match: Match
        for match in self.matches:

            if match.team_orange_score == 0 and match.team_blue_score == 0:
                continue

            orange_one: ColorStats = match.team_orange.player_one.orange
            orange_two: ColorStats = match.team_orange.player_two.orange
            blue_one: ColorStats = match.team_blue.player_one.blue
            blue_two: ColorStats = match.team_blue.player_two.blue

            if match.team_orange_player_one == Position.OFF:
                orange_offence: PositionStats = match.team_orange.player_one.offence
                orange_defence: PositionStats = match.team_orange.player_two.defence
            else:
                orange_offence: PositionStats = match.team_orange.player_two.offence
                orange_defence: PositionStats = match.team_orange.player_one.defence

            if match.team_blue_player_one == Position.OFF:
                blue_offence: PositionStats = match.team_blue.player_one.offence
                blue_defence: PositionStats = match.team_blue.player_two.defence
            else:
                blue_offence: PositionStats = match.team_blue.player_two.offence
                blue_defence: PositionStats = match.team_blue.player_one.defence

            if match.team_orange_score == 6:
                orange_one.wins += 1
                orange_two.wins += 1
                orange_offence.wins += 1
                orange_defence.wins += 1

            elif match.team_blue_score == 6:
                blue_one.wins += 1
                blue_two.wins += 1
                blue_offence.wins += 1
                blue_defence.wins += 1

            else:
                raise ValueError("Illegal Score detected")

            orange_two.most_goals_per_match_received = max(orange_two.most_goals_per_match_received,
                                                           match.team_blue_score)
            orange_one.most_goals_per_match_received = max(orange_one.most_goals_per_match_received,
                                                           match.team_blue_score)

            blue_two.most_goals_per_match_received = max(blue_two.most_goals_per_match_received,
                                                         match.team_orange_score)
            blue_one.most_goals_per_match_received = max(blue_one.most_goals_per_match_received,
                                                         match.team_orange_score)

            orange_two.least_goals_per_match_received = min(orange_two.least_goals_per_match_received,
                                                            match.team_blue_score)
            orange_one.least_goals_per_match_received = min(orange_one.least_goals_per_match_received,
                                                            match.team_blue_score)

            blue_two.least_goals_per_match_received = min(blue_two.least_goals_per_match_received,
                                                          match.team_orange_score)
            blue_one.least_goals_per_match_received = min(blue_one.least_goals_per_match_received,
                                                          match.team_orange_score)

            orange_two.min_goals_scored_per_match = min(orange_two.min_goals_scored_per_match,
                                                        match.team_orange_score)
            orange_one.min_goals_scored_per_match = min(orange_one.min_goals_scored_per_match,
                                                        match.team_orange_score)

            blue_two.min_goals_scored_per_match = min(blue_two.min_goals_scored_per_match,
                                                      match.team_blue_score)
            blue_one.min_goals_scored_per_match = min(blue_one.min_goals_scored_per_match,
                                                      match.team_blue_score)

            # ----

            orange_offence.most_goals_per_match_received = max(orange_offence.most_goals_per_match_received,
                                                               match.team_blue_score)
            orange_defence.most_goals_per_match_received = max(orange_defence.most_goals_per_match_received,
                                                               match.team_blue_score)

            blue_offence.most_goals_per_match_received = max(blue_offence.most_goals_per_match_received,
                                                             match.team_orange_score)
            blue_defence.most_goals_per_match_received = max(blue_defence.most_goals_per_match_received,
                                                             match.team_orange_score)

            orange_offence.least_goals_per_match_received = min(orange_offence.least_goals_per_match_received,
                                                                match.team_blue_score)
            orange_defence.least_goals_per_match_received = min(orange_defence.least_goals_per_match_received,
                                                                match.team_blue_score)

            blue_offence.least_goals_per_match_received = min(blue_offence.least_goals_per_match_received,
                                                              match.team_orange_score)
            blue_defence.least_goals_per_match_received = min(blue_defence.least_goals_per_match_received,
                                                              match.team_orange_score)

            orange_two.goals_scored += match.team_orange_score
            orange_one.goals_scored += match.team_orange_score
            orange_two.goals_received += match.team_blue_score
            orange_one.goals_received += match.team_blue_score

            orange_offence.goals_scored += match.team_orange_score
            orange_defence.goals_scored += match.team_orange_score
            orange_offence.goals_received += match.team_blue_score
            orange_defence.goals_received += match.team_blue_score

            orange_two.played += 1
            orange_one.played += 1
            orange_offence.played += 1
            orange_defence.played += 1

            blue_two.goals_scored += match.team_blue_score
            blue_one.goals_scored += match.team_blue_score
            blue_two.goals_received += match.team_orange_score
            blue_one.goals_received += match.team_orange_score

            blue_offence.goals_scored += match.team_blue_score
            blue_defence.goals_scored += match.team_blue_score
            blue_offence.goals_received += match.team_orange_score
            blue_defence.goals_received += match.team_orange_score

            blue_two.played += 1
            blue_one.played += 1
            blue_offence.played += 1
            blue_defence.played += 1
