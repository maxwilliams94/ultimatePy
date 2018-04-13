import ultimatepy as up

list_of_teams = ['Bristol 1','Bath 2','Bristol 2','Bath 1']

swsc = up.Tournament('South West Super Cup')

swsc.import_teams(list_of_teams)

print(swsc.team_list[0])

teamDict = {}

for team_number in range(len(list_of_teams)):
    teamDict[list_of_teams[team_number]] = up.Team(list_of_teams[team_number])

for team in teamDict:
    team = teamDict[team]

#swsc.get_team_list()

director = up.ProcessDirector()

#for index,name_of_team in enumerate(swsc.team_list):





