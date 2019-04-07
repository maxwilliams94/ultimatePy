from itertools import cycle, product

import collections


def create_group_match_ups(group_size):
    match_ups = []
    team_ones = list(range(0,group_size))
    team_twos = list(range(0,group_size))
    for t1 in team_ones:
        for t2 in team_twos:
            if t1 != t2: match_ups.append((t1,t2))

        team_twos.pop(team_twos.index(t1))

    return match_ups

class Tournament:
    """
    Store (and initialise) dictionary and storage structures
    Contains dictionaries for teams, groups, pitches which in turn
    contain values which are Team, Group and Pitch object respectively.
    """

    def __init__(self, team_list):
        self.groups = {}
        self.teams = {}
        self.pitches = {}
        self.schedule = []

        self.group_size = 0
        self.total_groups = 0
        self.total_teams = 0
        self.total_pitches = 0

        # Populate teams with Team objects
        for pos, team in enumerate(team_list):
            self.teams[pos + 1] = Team(team, pos + 1)

        self.tot_teams = len(team_list)


    def create_groups(self, group_size):
        self.group_size = group_size
        self.total_groups = self.tot_teams // self.group_size

        print("{} groups of {} teams".format(self.total_groups, group_size))

        # Create group objects within dictionary
        for i in range(self.total_groups):
            self.groups[i] = Group(chr(ord('A') + i), self.group_size)

        # Assign teams in initial self.groups by seed
        temp_seed_list = list(range(1, self.tot_teams + 1))
        for i in cycle(range(self.total_groups)):
            try:
                team = self.teams[temp_seed_list.pop(0)]
                self.groups[i].addTeam(team)
                team = self.teams[temp_seed_list.pop(-1)]
                self.groups[i].addTeam(team)
            except IndexError:
                # Run out of teams to place into self.groups
                break

    def create_pitches(self, total_pitches):
        self.total_pitches = total_pitches

        for id in range(total_pitches):
            self.pitches[id] = Pitch(id)


    def create_group_stage(self):
        req_group_games = self.total_groups * (self.group_size * (self.group_size - 1))//2
        print("Total group games: {}".format(req_group_games))

        # For each group, as many games from the same group should play at the same time
        max_concur_games = self.group_size//2
        if max_concur_games > self.total_pitches: max_concur_games = self.total_pitches

        group_game_combinations = {}
        for group in self.groups.keys():
            group_game_combinations[group] = iter(cycle(create_group_match_ups(self.group_size)))

        t1_last = t2_last = group_last = 99
        group_games_created = 0
        group_it = cycle(self.groups.keys())
        pitch_it = cycle(self.pitches.keys())
        group = next(group_it)
        pitch = next(pitch_it)
        i = 0
        while group_games_created < req_group_games:
            t1,t2 = next(group_game_combinations[group])
            if (t1 not in [t1_last, t2_last] and t2 not in [t1_last, t2_last]) or group != group_last:
                self.schedule.append(
                    Fixture(self.groups[group].team_list[t1],
                            self.groups[group].team_list[t2],
                            pitch,
                            None,
                            None,
                            self.groups[group]))
                t1_last,t2_last, group_last = t1, t2, group
                group_games_created += 1
                pitch = next(pitch_it)
                i = i+1
                if i == max_concur_games:
                    group = next(group_it)
                    i = 0
        print("Created {} group stage games".format(group_games_created))


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

    def __str__(self):
        return self.name

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

    def refreshGroup(self):
        """Set group size and then sort self.team_list according to seeds"""
        self.size = len(self.team_list)
        self.team_list.sort(key=lambda e : e.seed)

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
    def __init__(self, team1, team2, pitch, gamestart, gamelength, group = None):
        self.team1 = team1
        self.team2 = team2
        self.pitch = pitch
        self.group = group
        self.gamestart = gamestart
        self.gamelength = gamelength

    def __str__(self):
        return "{} | pitch {:3} | group {:3} |{:<10} v {:>10}".format(
            self.gamestart, self.pitch, self.group.id,self.team1.name, self.team2.name)


Timings = collections.namedtuple('Timings', ['game_length', 'game_break', 'day_start', 'day_length'])


# if __name__ == '__main__':