from ultimatepy import Team,Group

# import team list
all_teams = ["Uni A","Uni B", "Uni C", "Uni D", "Uni E", "Uni F", "Uni G", "Uni H"]
# count number of teams
numTeams = len(all_teams)
# get number of groups
numGroups = int(len(all_teams)/4)
print("{} Groups of 4 Teams".format(numGroups))

# Populate TeamDict with Team objects
teamDict = {}
for teamNumber,team in enumerate(all_teams):
    teamDict[str(team)] = Team(str(team),teamNumber+1)


# Create dictionary of group objects
groupDict = {}
groupList = []
for number in range(0,numGroups):
    group_name = chr(65 + number)
    groupDict[group_name] = Group(group_name)
    groupList.append(group_name)

# Create team_list dummy
teamListDummy = all_teams
# Iterate through the team list and assign each team to a group according to seed
for num in range(int(len(all_teams)/2)):
    dest_group = groupList[num%len(groupList)]
    groupDict[dest_group].addTeam(teamListDummy.pop(0))
    groupDict[dest_group].addTeam(teamListDummy.pop(-1))
    groupDict[dest_group].team_list.sort()

for group in groupList:
    print(group)
    for team in groupDict[group].team_list:
        print(teamDict[team])