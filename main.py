import math

from tabulate import tabulate


# import random

# class PositionStats:
#     played: int = 0
#     wins: int = 0
#     goals_scored: int = 0
#     goals_received: int = 0
#     most_goals_per_match_received: int = 0
#     least_goals_per_match_received: int = 6

class ColorStats:
    played: int = 0
    wins: int = 0
    goals_scored: int = 0
    goals_received: int = 0
    most_goals_per_match_received: int = 0
    least_goals_per_match_received: int = 6


class Player:

    @property
    def games_played(self):
        return self.blue.played + self.orange.played

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

    def __init__(self, uid: int, name: str):
        self.uid: int = uid
        self.name: str = name
        self.blue: ColorStats = ColorStats()
        self.orange: ColorStats = ColorStats()


class Team:

    def __init__(self, one: int, two: int):
        self.player_defence: int = one
        self.player_offence: int = two


class Match:
    team_orange_score: int = 0
    team_blue_score: int = 0

    def __init__(self, orange: Team, blue: Team, uid: int, round_uid: int):
        self.team_orange: Team = orange
        self.team_blue: Team = blue
        self.uid: int = uid
        self.round_uid: int = round_uid


class Tournament:
    matches: [Match] = []
    players: [Player] = []

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

    def add_players(self, players: [str]):
        uid_counter = 1
        for player_str in players:
            self.players.append(Player(uid_counter, player_str))
            uid_counter += 1

    # def add_round(self):
    #
    #     if len(self.players) % 4 != 0:
    #         raise ValueError("Number of tournament players has to be dividable by 4")
    #
    #     uids: [int] = random.sample(range(1, len(self.players) + 1), len(self.players))
    #
    #     matches_per_round = int(len(self.players) / 4)
    #
    #     for match_count in range(matches_per_round):
    #         self.matches.append(Match(
    #             Team(uids[0 + (match_count * 4)], uids[1 + (match_count * 4)]),
    #             Team(uids[2 + (match_count * 4)], uids[3 + (match_count * 4)]),
    #             len(self.matches) + 1, math.ceil((len(self.matches) + 1) / matches_per_round)))

    def add_score(self, match_uid: int, score_orange: int, score_blue: int):
        self.get_match(match_uid).team_blue_score = score_blue
        self.get_match(match_uid).team_orange_score = score_orange

    def add_hard_coded_round(self, set_plan: str):
        set_plan: [str] = set_plan.replace("\t", ";").split(";")

        number_of_matches: int = int(len(set_plan) / 2)

        for i in range(number_of_matches):
            i *= 2

            team_blue = set_plan[i]
            team_orange = set_plan[i + 1]

            self.matches.append(Match(orange=
                                      Team(one=int(team_blue.split("-")[0]), two=int(team_blue.split("-")[1])),
                                      blue=Team(one=int(team_orange.split("-")[0]),
                                                two=int(team_orange.split("-")[1])),
                                      uid=len(self.matches) + 1,
                                      round_uid=math.ceil((len(self.matches) + 1) / len(set_plan) * 2)))

    def evaluate_results(self):
        match: Match
        for match in self.matches:

            if match.team_orange_score == 0 and match.team_blue_score == 0:
                continue

            orange_offence: ColorStats = self.get_player(match.team_orange.player_defence).orange
            orange_defence: ColorStats = self.get_player(match.team_orange.player_offence).orange
            blue_offence: ColorStats = self.get_player(match.team_blue.player_defence).blue
            blue_defence: ColorStats = self.get_player(match.team_blue.player_offence).blue

            if match.team_orange_score == 6:
                orange_offence.wins += 1
                orange_defence.wins += 1

            elif match.team_blue_score == 6:
                blue_offence.wins += 1
                blue_defence.wins += 1

            else:
                raise ValueError("Illegal Score detected")

            orange_defence.most_goals_per_match_received = max(orange_defence.most_goals_per_match_received,
                                                               match.team_blue_score)
            orange_offence.most_goals_per_match_received = max(orange_offence.most_goals_per_match_received,
                                                               match.team_blue_score)

            blue_defence.most_goals_per_match_received = max(blue_defence.most_goals_per_match_received,
                                                             match.team_orange_score)
            blue_offence.most_goals_per_match_received = max(blue_offence.most_goals_per_match_received,
                                                             match.team_orange_score)

            orange_defence.least_goals_per_match_received = min(orange_defence.least_goals_per_match_received,
                                                                match.team_blue_score)
            orange_offence.least_goals_per_match_received = min(orange_offence.least_goals_per_match_received,
                                                                match.team_blue_score)

            blue_defence.least_goals_per_match_received = min(blue_defence.least_goals_per_match_received,
                                                              match.team_orange_score)
            blue_offence.least_goals_per_match_received = min(blue_offence.least_goals_per_match_received,
                                                              match.team_orange_score)

            orange_defence.goals_scored += match.team_orange_score
            orange_offence.goals_scored += match.team_orange_score
            orange_defence.goals_received += match.team_blue_score
            orange_offence.goals_received += match.team_blue_score

            orange_defence.played += 1
            orange_offence.played += 1

            blue_defence.goals_scored += match.team_blue_score
            blue_offence.goals_scored += match.team_blue_score
            blue_defence.goals_received += match.team_orange_score
            blue_offence.goals_received += match.team_orange_score

            blue_defence.played += 1
            blue_offence.played += 1


if __name__ == "__main__":
    tournament: Tournament = Tournament()
    tournament.add_players(
        ["Player 1","Player 2","Player 3","Player 4","Player 5","Player 6","Player 7","Player 8","Player 9","Player 10","Player 11","Player 12","Player 13","Player 14","Player 15","Player 16",])
    # tournament.add_round()

    # Hard coded matches from https://golfsoftware.com/tools/schedule/playall.html
    tournament.add_hard_coded_round("6-13	9-10	7-12	8-11	1-3	5-14	2-16	4-15")
    tournament.add_hard_coded_round("9-11	8-12	2-3	6-14	10-16	1-4	5-15	7-13")
    tournament.add_hard_coded_round("2-4	1-5	10-11	9-12	7-14	6-15	8-13	3-16")
    tournament.add_hard_coded_round("7-15	3-4	1-6	2-5	9-13	11-16	10-12	8-14")

    tournament.add_score(1, score_orange=3, score_blue=6)
    tournament.add_score(2, score_orange=6, score_blue=5)
    tournament.add_score(3, score_orange=6, score_blue=3)
    tournament.add_score(4, score_orange=6, score_blue=5)
    tournament.add_score(5, score_orange=6, score_blue=3)
    tournament.add_score(6, score_orange=6, score_blue=5)
    tournament.add_score(7, score_orange=6, score_blue=5)
    tournament.add_score(8, score_orange=0, score_blue=6)
    tournament.add_score(9, score_orange=2, score_blue=6)
    tournament.add_score(10, score_orange=6, score_blue=4)
    tournament.add_score(11, score_orange=6, score_blue=1)
    tournament.add_score(12, score_orange=3, score_blue=6)
    tournament.add_score(13, score_orange=4, score_blue=6)
    tournament.add_score(14, score_orange=6, score_blue=2)
    tournament.add_score(15, score_orange=6, score_blue=5)
    tournament.add_score(16, score_orange=3, score_blue=6)

    tournament.evaluate_results()

    print()

    mtc: Match
    match_plan: [] = []
    for mtc in sorted(tournament.matches, key=lambda x: x.round_uid):
        match_plan.append(
            [mtc.round_uid, mtc.uid,
             tournament.get_player(mtc.team_orange.player_defence).name + " & " + tournament.get_player(
                 mtc.team_orange.player_offence).name, str(mtc.team_orange_score) + ":" + str(mtc.team_blue_score),
             tournament.get_player(mtc.team_blue.player_defence).name + " & " + tournament.get_player(
                 mtc.team_blue.player_offence).name])

    print(tabulate(match_plan, headers=['Round', 'Match', 'Team Orange', 'Score', 'Team Blue']))
    print()

    log: [] = []
    rank: int = 1
    for player in sorted(tournament.players,
                         key=lambda x: (x.wins, x.goals_shot - x.goals_received, x.goals_shot, -x.goals_received),
                         reverse=True):
        log.append([rank, player.name, player.wins, player.goals_shot - player.goals_received, player.goals_shot,
                    player.goals_received, player.max_goals_received, player.min_goals_received, player.blue.wins,
                    player.orange.wins])
        rank += 1

    # TODO: Add
    #   - Best match
    #   - Best defence
    #   - Offence / defence dependencies

    print(tabulate(log, headers=['#', 'Name', 'Wins', 'Dif', 'Scored', 'Received', 'Max received', 'Min received',
                                 'Blue Wins', 'Orange Wins']))

    # TODO: Print best players for ...
    #   - Defence
    #   - ...
