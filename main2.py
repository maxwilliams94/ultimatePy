import collections

from ultimatepy import Team, Group, Pitch
from itertools import cycle
from datetime import datetime, timedelta


# Expect team list to be input from file in seed order
team_input = ["Uni A 1", "Uni B", "Uni C", "Uni D", "Uni E", "Uni A 2", "Uni G", "Uni H"]

# Dictionary of Team objects
teams = {}
for pos, team in enumerate(team_input):
    teams[pos + 1] = Team(team, pos + 1)

tot_teams = len(team_input)
grp_size = 4
tot_grps = tot_teams // grp_size

print("{} groups of 4 teams".format(tot_grps))

# Create group objects within dictionary
groups = {}
for i in range(tot_grps):
    groups[i] = Group(chr(ord('A') + i), grp_size)

# Assign teams in initial groups by seed
temp_seed_list = list(range(1, tot_teams + 1))
for i in cycle(range(tot_grps)):
    try:
        team = teams[temp_seed_list.pop(0)]
        groups[i].addTeam(team)
        team = teams[temp_seed_list.pop(-1)]
        groups[i].addTeam(team)
    except IndexError:
        # Run out of teams to place into groups
        break

for i in range(tot_grps):
    print(groups[i])

# Game/Day Variables
Timings = collections.namedtuple('Timings', ['game_length', 'game_break', 'day_start', 'day_length'])
timings = Timings(timedelta(hours=1), timedelta(minutes=5), datetime(day=1, hour=9), day_length=timedelta(hours=8))
total_pitches = 1



# Create Pitch objects and store in dictionary
pitches = {}
for id in range(total_pitches):
    pitches[id] = Pitch(id)

#
