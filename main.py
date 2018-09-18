from ultimatepy import Team

# import team list
teamList = ["Uni A","Uni B", "Uni C", "Uni D", "Uni E", "Uni F", "Uni G", "Uni H"]
# count number of teams
numTeams = len(teamList)
# get number of groups
numGroups = len(teamList)/4
print("{} Groups of 4 Teams".format(numGroups))

# Populate TeamDict with Team objects
teamDict = {}
for teamNumber,team in enumerate(teamList):
    teamDict[str(team)] = Team(str(team),teamNumber+1)





