

class Team:
    def __init__(self, name, seed):
        self.name = name
        self.seed = seed
        self.group = ""
        self.groupSeed = -1

    def __repr__(self):
        return '{}: {}'.format(self.seed,self.name)

class Group:
    def __init__(self, identifier):
        self.id = identifier
        self.team_list = []
        self.size = 0
    def addTeam(self,team_name):
        self.team_list.append(str(team_name))

    def refreshGroup(self):
        self.size = len(self.team_list)
        self.team_list.sort()




# if __name__ == '__main__':