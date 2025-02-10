from typing import Callable

from components.match import Match
from components.player import Player

from plotly import graph_objs as go

from components.tournament import Tournament


def get_by_attribute(items: [any], func: Callable, reverse: bool = True):
    selected_item: any = sorted(items, key=func, reverse=reverse)[0]
    selected_item_value: int = func(selected_item)
    selected_items: [any] = [p for p in items if func(p) == selected_item_value]

    return selected_items


def get_match_percentage_player(tournament: Tournament, player: Player):
    match_dict: {} = {}

    for match in tournament.matches:
        score: str = ""
        if match.team_blue.player_one is player or match.team_blue.player_two is player:
            score = f"{match.team_blue_score}:{match.team_orange_score}"

        elif match.team_orange.player_one is player or match.team_orange.player_two is player:
            score = f"{match.team_orange_score}:{match.team_blue_score}"

        if score != "":
            if score in match_dict.keys():
                match_dict[score] += 1
            else:
                match_dict[score] = 1

    max_key = max(match_dict, key=match_dict.get)
    if match_dict[max_key] > 1:
        return f"{match_dict[max_key]} x {('lost' if int(max_key.split(':')[0]) < 6 else 'won') if int(max_key.split(':')[0]) != int(max_key.split(':')[1]) else "draw"} {max_key}"
    return ""


def get_match_percentage(tournament: Tournament):
    pre_data: dict = {}

    for match in tournament.matches:
        match: Match
        if match.score in pre_data:
            pre_data[match.score] += 1
        else:
            pre_data[match.score] = 1

    data = [f"{v} x {k} ({100 *v / tournament.total_matches:.0f}%)" for k, v in sorted(pre_data.items(), key=lambda item: item[1],reverse=True)]

    # data = []
    #
    # for i in range(5, -1, -1):
    #     number_of_hits = len(
    #         [m for m in tournament.matches if abs(m.team_blue_score - m.team_orange_score) == (6 - i)])
    #     data.append(
    #         f"{number_of_hits} x 6:{i} ({100 * number_of_hits / tournament.total_matches:.0f}%)")
    # for i in range(5, -1, -1):
    #     number_of_hits = len(
    #         [m for m in tournament.matches if (m.team_blue_score == m.team_orange_score and m.team_blue_score == i)])
    #     data.append(
    #         f"{number_of_hits} x {i}:{i} ({100 * number_of_hits / tournament.total_matches:.0f}%)")

    return data


def run(tournament: Tournament, trivia: [str] = None):
    if trivia is None:
        trivia: [str] = ["" for _ in tournament.players]

    mtc: Match
    match_plan: [] = []
    for mtc in sorted(tournament.matches, key=lambda x: x.round_uid):
        # if mtc.team_blue_score > mtc.team_orange_score:
        #     team_blue_name:str = f"<b>{mtc.team_blue.name(mtc.uid)}</b>"
        #     team_orange_name:str = mtc.team_orange.name(mtc.uid)
        # elif mtc.team_blue_score < mtc.team_orange_score:
        #     team_blue_name:str = mtc.team_blue.name(mtc.uid)
        #     team_orange_name:str = f"<b>{mtc.team_orange.name(mtc.uid)}</b>"
        # else:
        team_blue_name: str = mtc.team_blue.name(mtc.uid)
        team_orange_name: str = mtc.team_orange.name(mtc.uid)
        match_plan.append(
            [mtc.round_uid, mtc.uid, team_orange_name, mtc.score, team_blue_name])

    match_headers: [str] = ['Round', 'Match', 'Team Orange', 'Score', 'Team Blue']

    log: [] = []
    rank: int = 1

    sorted_players: [Player] = sorted(tournament.players,
                                      key=lambda x: (
                                          x.points, x.wins, x.dif, x.goals_shot, -x.goals_received, -ord(x.name[0])),
                                      reverse=True)

    previous_equal = False

    for i, player in enumerate(sorted_players):

        if player.is_joker:
            continue

        if i >= 1:
            if player.wins == sorted_players[i - 1].wins and player.dif == sorted_players[
                i - 1].dif and player.goals_shot == sorted_players[i - 1].goals_shot and player.goals_received == \
                    sorted_players[i - 1].goals_received:
                rank -= 1
                previous_equal = True

            else:
                if previous_equal:
                    previous_equal = False
                    rank += 1

        log.append([rank,
                    str(player),
                    player.points,
                    f"{player.wins} / {player.played}",
                    f"{player.draws}",
                    f"{player.dif :+d}",
                    f"{player.goals_shot} ({100 * (player.goals_shot / (player.played * 6)) if player.played != 0 else 0:.0f}%)",
                    f"{player.goals_received} ({100 * (player.goals_received / (player.played * 6)) if player.played != 0 else 0:.0f}%)",
                    player.min_goals_scored, player.min_goals_received,
                    f"{(player.goals_shot / player.played) if player.played != 0 else 0:.1f}",
                    f"{(player.goals_received / player.played) if player.played != 0 else 0:.1f}",
                    f"{(player.goals_shot / player.played - player.goals_received / player.played) if player.played != 0 else 0:+.1f}",
                    f"{player.blue.wins} / {player.blue.played}",
                    f"{player.orange.wins} / {player.orange.played}",
                    f"{player.offence.wins} / {player.offence.played}",
                    f"{player.defence.wins} / {player.defence.played}",
                    get_match_percentage_player(tournament, player),
                    # trivia[i]
                    ])

        rank += 1

    table_headers: [str] = ['#',
                            'Name',
                            "Points",
                            'Wins',
                            'Draws',
                            'Goal Dif.',
                            f'Scored (Ratio)',
                            f'Received (Ratio)', 'Worst scored',
                            'Best received', "Avg. scored", "Avg. received", 'Avg. Dif.', 'Blue Wins', 'Orange Wins',
                            'Off. Wins', 'Def. Wins', 'Same scores',
                            # 'Fun facts'
                            ]

    non_jokers: [Player] = [p for p in tournament.players if not p.is_joker]

    top_scorers: [Player] = get_by_attribute(non_jokers, func=lambda x: x.goals_shot)
    top_receivers: [Player] = get_by_attribute(non_jokers, func=lambda x: x.goals_received)
    top_difs: [Player] = get_by_attribute(non_jokers, func=lambda x: x.dif)

    closest_matches: [Match] = get_by_attribute(tournament.matches,
                                                func=lambda x: abs(x.team_orange_score - x.team_blue_score),
                                                reverse=False)
    highest_matches: [Match] = get_by_attribute(tournament.matches,
                                                func=lambda x: abs(x.team_orange_score - x.team_blue_score))

    blue_wins: int = len([m for m in tournament.matches if m.team_blue_score > m.team_orange_score])
    orange_wins: int = len([m for m in tournament.matches if m.team_blue_score < m.team_orange_score])

    best_defence: [Player] = get_by_attribute(non_jokers, func=lambda x: x.defence.least_goals_per_match_received,
                                              reverse=False)

    stats = [
        [f"{p} ({p.goals_shot})" for p in top_scorers],
        [f"{p} ({p.goals_received})" for p in top_receivers],
        [f"{p} ({p.dif})" for p in top_difs],
        [str(m) for m in closest_matches],
        [str(m) for m in highest_matches],
        [f"{p} ({p.defence.least_goals_per_match_received})" for p in best_defence],
        get_match_percentage(tournament),
        [f"{blue_wins}:{orange_wins}"]]

    stats_headers = ["Most Scored", "Most Received", "Best Difference", "Closest Game", "Highest Win", "Best Defence",
                     "Result Percentage", "Blue vs. Orange"]

    domains = [
        {'x': [0.0, 0.25], 'y': [0.0, 1.0]},
        {'x': [0.26, 1.0], 'y': [0.0, 0.45]},
        {'x': [0.26, 1.0], 'y': [0.46, 1.0]},
    ]
    colors = ['rgb(201, 176, 55)', 'rgb(215, 215, 215)', 'rgb(173, 138, 86)',
              'rgb(235, 240, 248)']

    traces = [go.Table(header=dict(values=match_headers),
                       cells=dict(
                           values=[[i[j] for i in match_plan] for j in range(len(match_plan[0]))],
                           height=26
                       ),
                       domain=domains[0],
                       columnwidth=[20, 20, 80, 20, 80],

                       ),
              go.Table(header=dict(values=stats_headers),
                       cells=dict(values=stats, height=26),
                       domain=domains[1]
                       ),
              go.Table(header=dict(values=table_headers),
                       cells=dict(
                           values=[[i[j] for i in log] for j in range(len(log[0]))],
                           height=26,
                           fill_color=[colors],
                       ),
                       domain=domains[2],
                       columnwidth=[10, 30, 15, 20, 15, 20, 30, 30, 30, 25, 30, 20, 25, 25, 25, 25, 30, 40],
                       )]

    fig = go.Figure(data=traces)

    progress = f"({tournament.matches_played}/{tournament.total_matches} matches played)" if tournament.matches_played != tournament.total_matches else ""

    title_label = f"{tournament.title} {progress}"

    fig.update_layout(
        title=title_label,
        margin=dict(l=10, r=10, t=30, b=10),
    )

    with open(f"../results/{tournament.title.lower().replace(' ', '_')}.html", 'w', encoding='utf-8') as file:
        file.write(f'<head><title>Kicker Tournament</title></head>')
        file.write(fig.to_html(full_html=True))
