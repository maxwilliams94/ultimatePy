import collections

from ultimatepy import Tournament, Timings
from itertools import cycle
from datetime import datetime, timedelta


# Expect team list to be input from file in seed order
team_input = ["Uni A 1", "Uni B", "Uni C", "Uni D", "Uni E", "Uni A 2", "Uni G", "Uni H"]
# Tournament timings stored within namedTuple
# Game/Day Variables
timings = Timings(game_length=timedelta(hours=1),
                  game_break=timedelta(minutes=5),
                  day_start=datetime(year=1, month=1, day=1, hour=9),
                  day_length=timedelta(hours=8))
total_pitches = 1

tournament = Tournament(team_input, timings, total_pitches)

for i in range(tournament.tot_grps):
    print(tournament.groups[i])

# todos
# todo Create schedule (group stage)
# todo Add schedules to pitches
# todo allow data input for match results
# todo create storage for group results
