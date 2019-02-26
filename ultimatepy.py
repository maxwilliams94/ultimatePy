

class Team:
    def __init__(self, name, seed):
        self.name = name
        self.seed = seed
        self.group = ""
        self.groupSeed = -1

    def __repr__(self):
        return '{}: {}'.format(self.seed,self.name)

class Group:
    def __init__(self, identifier, size):
        self.id = identifier
        self.team_list = []  # List of team objects
        self.size = size

    def addTeam(self, team):
        self.team_list.append(team)

    def refreshGroup(self,seed_dictionary,rev_seed_dictionary):
        """Set group size and then sort self.team_list according to seeds"""
        self.size = len(self.team_list)
        group_seeds = []
        for team in self.team_list:
            group_seeds.append(seed_dictionary[team])
        group_seeds.sort()
        temp_team_list = []
        for seed in group_seeds:
            temp_team_list.append(rev_seed_dictionary[seed])
        self.team_list = temp_team_list


class Pitch:
    def __init__(self, identifier):
        self.id = identifier
        self.fixtures = []


class Fixture:
    def __init__(self, team1, team2, pitch, gamestart, gamelength):
        self.team1 = team1
        self.team2 = team2
        self.pitch = pitch
        self.gamestart = gamestart
        self.gamelength = gamelength






# if __name__ == '__main__':