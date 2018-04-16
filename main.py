import ultimatepy as up

# import list of teams
list_of_teams = ['Bristol 1','Bath 2','Bristol 2','Bath 1', 'Cardiff 1', 'Swansea 1', 'Bears 1', 'UWE 2']

swsc = up.Tournament('South West Super Cup')


swsc.importTeams(list_of_teams)

swsc.setGroupSizes()

swsc.getTeamList()






