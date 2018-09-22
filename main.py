from ultimatepy import Team,Group

# import team list
all_teams = ["Uni A","Uni B", "Uni C", "Uni D", "Uni E", "Uni F", "Uni G", "Uni H"]
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
    group_name = chr(65 + number)
    group_dict[group_name] = Group(group_name)
    group_list.append(group_name)

# Create team_list dummy
team_list_cp = all_teams
# Iterate through the team list and assign each team to a group according to seed
for num in range(int(len(all_teams)/2)):
    dest_group = group_list[num % len(group_list)]
    group_dict[dest_group].addTeam(team_list_cp.pop(0))
    group_dict[dest_group].addTeam(team_list_cp.pop(-1))
    group_dict[dest_group].team_list.sort()

for group in group_list:
    print(group)
    for team in group_dict[group].team_list:
        print(team_dict[team])