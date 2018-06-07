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
    tournamentName = input("Tournament Name: ")

# import team list

# count number of teams

# get number of groups

# calculate group sizes

# choose group size

# assign teams to groups according to seed
