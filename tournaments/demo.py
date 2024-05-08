from components import plotter
from components.team import Position
from components.tournament import Tournament

if __name__ == "__main__":
    tournament: Tournament = Tournament()
    tournament.title = "Demo Kicker Tournament"

    tournament.set_players(
        ["Player 1", "Player 2", "Player 3", "Player 4", "Player 5", "Player 6", "Player 7", "Player 8", "Player 9",
         "Player 10", "Player 11", "Player 12", "Player 13", "Player 14", "JOKER 1", "JOKER 2"])

    # Hard coded matches from https://golfsoftware.com/tools/schedule/playall.html
    tournament.add_hard_coded_round("6-13	9-10	7-12	8-11	1-3	5-14	2-16	4-15")
    tournament.add_hard_coded_round("9-11	8-12	2-3	6-14	1-4	10-16	5-15	7-13")
    tournament.add_hard_coded_round("2-4	1-5	10-11	9-12	7-14	6-15	8-13	3-16")
    tournament.add_hard_coded_round("7-15	3-4	1-6	2-5	9-13	11-16	10-12	8-14")

    tournament.add_score(uid=1, orange=6, blue=5, orange_one=Position.OFF, blue_one=Position.OFF)
    tournament.add_score(uid=2, orange=3, blue=6, orange_one=Position.DEF, blue_one=Position.DEF)
    tournament.add_score(uid=3, orange=6, blue=4, orange_one=Position.OFF, blue_one=Position.OFF)
    tournament.add_score(uid=4, orange=6, blue=0, orange_one=Position.OFF, blue_one=Position.OFF,joker_blue=1, joker_orange=3)
    tournament.add_score(uid=5, orange=6, blue=5, orange_one=Position.DEF, blue_one=Position.OFF)
    tournament.add_score(uid=6, orange=4, blue=6, orange_one=Position.OFF, blue_one=Position.OFF, joker_blue=9)
    tournament.add_score(uid=7, orange=1, blue=6, orange_one=Position.DEF, blue_one=Position.DEF,joker_blue=5)
    tournament.add_score(uid=8, orange=1, blue=6, orange_one=Position.DEF, blue_one=Position.DEF,joker_orange=11)
    tournament.add_score(uid=9, orange=6, blue=3, orange_one=Position.OFF, blue_one=Position.OFF)
    # tournament.add(uid=10, orange=6, blue=4, orange_one=Position.OFF, blue_one=Position.OFF)
    # tournament.add(uid=11, orange=3, blue=6, orange_one=Position.OFF, blue_one=Position.DEF)
    # tournament.add(uid=12, orange=5, blue=6, orange_one=Position.OFF, blue_one=Position.DEF)
    # tournament.add(uid=13, orange=1, blue=6, orange_one=Position.DEF, blue_one=Position.OFF)
    # tournament.add(uid=14, orange=5, blue=6, orange_one=Position.OFF, blue_one=Position.OFF)
    # tournament.add(uid=15, orange=6, blue=5, orange_one=Position.DEF, blue_one=Position.DEF)
    # tournament.add(uid=16, orange=1, blue=6, orange_one=Position.OFF, blue_one=Position.DEF)

    tournament.evaluate_results()
    trivia: [str] = ["Winner", "One goal to victory", "", "One goal to victory", "One goal to victory", "",
                     "Best avg. received", "", "", "", "", "", "", "", "", "", ""]
    plotter.run(tournament, trivia)
