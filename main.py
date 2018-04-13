import ultimatepy as up

# import list of teams
list_of_teams = ['Bristol 1','Bath 2','Bristol 2','Bath 1']

swsc = up.Tournament('South West Super Cup')


swsc.import_teams(list_of_teams)

teamDict = {}

for teamNumber,team in enumerate(swsc.team_list):
    teamDict[str(team)] = up.Team(str(team))



# print(teamDict)
# swsc.get_team_list()






