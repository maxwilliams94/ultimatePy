class Group:
    def __init__(self, i, size):
        self.id = chr(ord('A') + i)
        self.index = i
        self.team_list = []  # List of team objects
        self.size = size
        self.seed_list = []

    def addTeam(self, team):
        self.team_list.append(team)
        self.seed_list.append(team.seed)
        self.seed_list.sort()

    def refreshGroup(self):
        """Set group size and then sort self.team_list according to seeds"""
        self.size = len(self.team_list)
        self.team_list.sort(key=lambda e : e.seed)

    def __str__(self):
        self.team_list.sort(key=lambda e: e.seed)
        team_str = ""
        team_str += "Group {}\n{}\n".format(self.id, 7 * "-")
        for team in self.team_list:
            team_str += "{:<2} {}\n".format(team.seed, team.name)
        return team_str
