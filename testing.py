"""Integrating Testing for ultimatepy"""

from ultimatepy import Tournament, Timings
from datetime import datetime, timedelta

team_input = ["Uni 1", "Uni 2", "Uni 3", "Uni 4", "Uni 5", "Uni 6", "Uni 7", "Uni 8"]
# Tournament timings stored within namedTuple
# Game/Day Variables
timings = Timings(game_length=timedelta(hours=1),
                  game_break=timedelta(minutes=5),
                  day_start=datetime(year=1, month=1, day=1, hour=9),
                  day_length=timedelta(hours=8))

t = Tournament(team_list=team_input, timings=timings, total_pitches=1, group_size=4)

assert t.tot_teams == len(team_input), "total teams matches length of input team list"
assert len(t.groups) == len(team_input)//t.group_size, "correct number of groups created"

for group in t.groups.values():
    assert len(group.team_list) == t.group_size, \
        """len(group.team_list) should equal 
        group size {}v.{}""".format(len(group.team_list),t.group_size)


t.create_group_stage()

assert len(t.schedule) != 0, \
    "tournament.schedule should have been populated with group stage games"
expected_group_games = (t.total_groups * (t.group_size * (t.group_size - 1))//2)
assert len(t.schedule) == expected_group_games , \
    """total number of games in the schedule
     should be equal to expected number of
     group games: {} v {}""".format(len(t.schedule), expected_group_games)



