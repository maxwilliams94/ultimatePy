from ultimatepy import Team, Group, Pitch, Fixture
import datetime
from math import floor

# import team list
all_teams = ["Uni A 1", "Uni B", "Uni C", "Uni D", "Uni E", "Uni A 2", "Uni G", "Uni H"]
# create dictionary of seeds
seed_dict = {}
# create dictionary to link seeds to teams in opposite direction
rev_seed_dict = {}
# populate seed and reverse seed dicts
for seed,team in enumerate(all_teams):
    seed_dict[team] = seed + 1
    rev_seed_dict[seed + 1] = team

# count number of teams
total_teams = len(all_teams)
# get number of groups
total_groups = len(all_teams) // 4
print("{} Groups of 4 Teams".format(total_groups))

# Populate TeamDict with Team objects
team_dict = {}
for team_num, team in enumerate(all_teams):
    team_dict[str(team)] = Team(str(team), team_num + 1)


# Create dictionary of group objects
group_dict = {}
group_list = []
for number in range(0, total_groups):
    group_name = chr(ord('A') + number)
    group_dict[group_name] = Group(group_name)
    group_list.append(group_name)

# Create team_list dummy
team_list_cp = all_teams
# Iterate through the team list and assign each team to a group according to seed
for num in range(len(all_teams)//2):
    dest_group = group_list[num % len(group_list)]
    group_dict[dest_group].addTeam(team_list_cp.pop(0))
    group_dict[dest_group].addTeam(team_list_cp.pop(-1))


# Sort and set the group size attribute once all team lists are populated
for group in group_dict.values():
    group.refreshGroup(seed_dict,rev_seed_dict)

for group in group_list:
    print(group)
    for team in group_dict[group].team_list:
        print(team_dict[team])

# Game/Day variables
game_length = datetime.timedelta(0, 0, 0, 0, 60, 0, 0)
game_break = datetime.timedelta(0, 0, 0, 0, 5, 0, 0)
days = 2
total_pitches = 3
day1_start = datetime.datetime(datetime.datetime.now().year, 1, 1, 9, 0, 0, 0)
day1_end = datetime.datetime(datetime.datetime.now().year, 1, 1, 17, 0, 0, 0)
day2_start = datetime.datetime(datetime.datetime.now().year, 1, 1, 9, 0, 0, 0)
day2_end = datetime.datetime(datetime.datetime.now().year, 1, 1, 15, 0, 0, 0)
length_of_day1 = day1_end - day1_start
length_of_day2 = day2_end - day2_start

# Create pitch objects
pitch_dict = {}
for pitch in range(1, total_pitches + 1):
    pitch_dict[str(pitch)] = Pitch(str(pitch))

# Check number of time slots versus number of required games
total_group_matches = 0
for group in group_dict.values():
    total_group_matches += group.size * (group.size - 1)
print("\nTotal Group Matches: {}".format(total_group_matches))

total_game_slots = floor((length_of_day1 + length_of_day2) / (game_length + game_break)) * total_pitches
print("\n{} Pitches for {} days with {} games and {} breaks gives {} game slots".format(
    total_pitches, days, game_length, game_break, total_game_slots))

print("\n{} games required for full group stage, leaving {} left for bracket games".format(
    total_group_matches, total_game_slots - total_group_matches))
