import ultimatepy as up

# import list of teams
list_of_teams = ['Bristol 1','Bath 2','Bristol 2','Bath 1', 'Cardiff 1', 'Swansea 1', 'Bears 1', 'UWE 2']

swsc = up.Tournament('South West Super Cup')


swsc.importTeams(list_of_teams)

teamDict = {}

for teamNumber,team in enumerate(swsc.teamList):
    teamDict[str(team)] = up.Team(str(team))
    teamDict[team].setSeed(teamNumber+1)

swsc.setGroupSizes()




# print(teamDict)
# swsc.get_team_list()






