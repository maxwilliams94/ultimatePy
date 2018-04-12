import ultimatepy as up

list_of_teams = ['Bristol 1','Bath 2','Bristol 2','Bath 1']

swsc = up.Tournament('South West Super Cup')

swsc.import_teams(list_of_teams)

print(swsc.team_list[0])

for team_number in range(1,len(list_of_teams)+1):
    team_number_str = str(team_number)
    ob_name = "team"+team_number_str


#swsc.get_team_list()

director = up.ProcessDirector()

#for index,name_of_team in enumerate(swsc.team_list):





