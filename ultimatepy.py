

class Team:
    def __init__(self, name, seed):
        self.name = name
        self.seed = seed
        self.group = ""
        self.groupSeed = -1

    def setSeed(self, seed):
        self.seed = seed

    def getName(self):
        print(self.name)

    def getSeed(self):
        print(self.seed)
    def __repr__(self):
        return '{}: {}'.format(self.seed,self.name)


if __name__ == '__main__':
    #tournamentName = input("Tournament Name: ")

    # import team list
    teamList = ["Uni A","Uni B", "Uni C", "Uni D", "Uni E", "Uni F", "Uni G", "Uni H"]
    # count number of teams
    numTeams = len(teamList)
    # get number of groups
    numGroups = len(teamList)/4
    print("{} Groups of 4 Teams".format(numGroups))

    # Create team objects in teamDict
    teamDict = {}
    for teamNumber,team in enumerate(teamList):
        teamDict[str(team)] = Team(str(team),teamNumber+1)


    print(teamDict)
    # assign teams to groups according to seed
