from ultimatepy import Team, Group
from itertools import cycle
import datetime
from math import floor

# Expect team list to be input from file in seed order
team_input = ["Uni A 1", "Uni B", "Uni C", "Uni D", "Uni E", "Uni A 2", "Uni G", "Uni H"]

# Dictionary of Team objects
teams = {}
for pos, team in enumerate(team_input):
    teams[pos + 1] = Team(team, pos)

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
