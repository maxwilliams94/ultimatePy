

class Team:
    def __init__(self, name, seed):
        self.name = name
        self.seed = seed
        self.group = ""
        self.groupSeed = -1
        self.grp_pos = 0
        self.id = seed
        self.goal_diff = 0
        self.group_points = 0

    def __repr__(self):
        return '{}: {}'.format(self.seed,self.name)

class Group:
    def __init__(self, identifier, size):
        self.id = identifier
        self.team_list = []  # List of team objects
        self.size = size
        self.seed_list = []

    def addTeam(self, team):
        self.team_list.append(team)
        self.seed_list.append(team.seed)
        self.seed_list.sort()

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

    def __str__(self):
        self.team_list.sort(key=lambda e: e.seed)
        team_str = ""
        team_str += "Group {}\n{}\n".format(self.id, 7 * "-")
        for team in self.team_list:
            team_str += "{}\n".format(team)
        return team_str


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