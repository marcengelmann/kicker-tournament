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
        return f"{match_dict[max_key]} x {'lost' if int(max_key.split(':')[0]) < 6 else 'won'} {max_key}"
    return ""


def get_match_percentage(tournament: Tournament):
    data: [str] = []

    for i in range(5, -1, -1):
        number_of_hits = len(
            [m for m in tournament.matches if abs(m.team_blue_score - m.team_orange_score) == (6 - i)])
        data.append(
            f"{number_of_hits} x 6:{i} ({100 * number_of_hits / tournament.total_matches:.0f}%)")

    return data


def run(tournament: Tournament, trivia: [str] = None):
    if trivia is None:
        trivia: [str] = ["" for _ in tournament.players]

    mtc: Match
    match_plan: [] = []
    for mtc in sorted(tournament.matches, key=lambda x: x.round_uid):
        match_plan.append(
            [mtc.round_uid, mtc.uid, mtc.team_orange.name(mtc.uid), mtc.score, mtc.team_blue.name(mtc.uid)])

    match_headers: [str] = ['Round', 'Match', 'Team Orange', 'Score', 'Team Blue']

    log: [] = []
    rank: int = 1

    sorted_players: [Player] = sorted(tournament.players,
                                      key=lambda x: (x.wins, x.dif, x.goals_shot, -x.goals_received, -ord(x.name[0])),
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

        log.append([rank, str(player), f"{player.wins} / {player.played}", f"{player.dif :+d}",
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
                    trivia[i]
                    ])

        rank += 1

    table_headers: [str] = ['#', 'Name', 'Wins', 'Dif', f'Scored (Ratio)',
                            f'Received (Ratio)', 'Worst scored',
                            'Best received', "Avg. scored", "Avg. received", 'Avg. Dif', 'Blue Wins', 'Orange Wins',
                            'Off. Wins', 'Def. Wins', 'Same scores', 'Fun facts']

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
        {'x': [0.0, 0.39], 'y': [0.45, 1.0]},
        {'x': [0.41, 1.0], 'y': [0.51, 1.0]},
        {'x': [0.0, 1.0], 'y': [0.0, 0.49]},
    ]

    traces = [go.Table(header=dict(values=match_headers),
                       cells=dict(values=[[i[j] for i in match_plan] for j in range(len(match_plan[0]))], height=23),
                       domain=domains[0],
                       columnwidth=[15, 20, 80, 20, 80],
                       ),
              go.Table(header=dict(values=stats_headers),
                       cells=dict(values=stats, height=23),
                       domain=domains[1]
                       ),
              go.Table(header=dict(values=table_headers),
                       cells=dict(values=[[i[j] for i in log] for j in range(len(log[0]))], height=23),
                       domain=domains[2],
                       columnwidth=[10, 30, 15, 10, 30, 30, 30, 30, 25, 30, 20, 25, 25, 25, 25, 30, 40],
                       )]

    fig = go.Figure(data=traces)

    progress = f"({tournament.matches_played}/{tournament.total_matches} matches played)" if tournament.matches_played != tournament.total_matches else ""

    title_label = f"{tournament.title} {progress}"

    fig.update_layout(
        title=title_label,
        margin=dict(l=50, r=50, t=50, b=20),
    )

    with open(f"../results/{tournament.title.lower().replace(' ', '_')}.html", 'w', encoding='utf-8') as file:
        file.write(f'<head><title>Kicker Tournament</title></head>')
        file.write(fig.to_html(full_html=True))
