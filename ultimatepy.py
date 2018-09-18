

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

class Group:
    def __init__(self, identifier):
        self.id = identifier
        self.team_list = []
        self.size = 0
    def addTeam(self,team_name):
        self.team_list.append(str(team_name))

    def setSize(self):
        self.size = len(self.team_list)


# if __name__ == '__main__':