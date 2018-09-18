from ultimatepy import Team,Group

# import team list
teamList = ["Uni A","Uni B", "Uni C", "Uni D", "Uni E", "Uni F", "Uni G", "Uni H"]
# count number of teams
numTeams = len(teamList)
# get number of groups
numGroups = int(len(teamList)/4)
print("{} Groups of 4 Teams".format(numGroups))

# Populate TeamDict with Team objects
teamDict = {}
for teamNumber,team in enumerate(teamList):
    teamDict[str(team)] = Team(str(team),teamNumber+1)


# Create dictionary of group objects
groupDict = {}
groupList = []
for number in range(0,numGroups):
    group_name = chr(65 + number)
    groupDict[group_name] = Group(group_name)
    groupList.append(group_name)

# Create team_list dummy
teamListDummy = teamList
# Iterate through the team list and assign each team to a group according to seed