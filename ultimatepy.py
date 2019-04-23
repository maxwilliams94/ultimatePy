from itertools import cycle
import collections
import datetime


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

        #Timings
        self.timings = Timings

        # Populate teams with Team objects
        for pos, team in enumerate(team_list):
            self.teams[pos + 1] = Team(team, pos + 1)

        self.total_teams = len(team_list)


    def create_groups(self, group_size):
        self.group_size = group_size
        self.total_groups = self.total_teams // self.group_size

        print("{} groups of {} teams".format(self.total_groups, group_size))

        self.req_group_games = self.total_groups * (self.group_size * (self.group_size - 1))//2
        print("Total group games: {}".format(self.req_group_games))
        # Create group objects within dictionary
        for i in range(self.total_groups):
            self.groups[i] = Group(chr(ord('A') + i), self.group_size)

        # Assign teams in initial self.groups by seed
        temp_seed_list = list(range(1, self.total_teams + 1))
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


    def set_timings(self, timings):
        self.timings = timings

        length_day1 = self.timings.day1_end - self.timings.day1_start
        length_day2 = self.timings.day2_end - self.timings.day2_start
        available_time = length_day1+length_day2
        adj_group_game_length = self.timings.group_game_length + self.timings.game_break
        adj_game_length = self.timings.game_length + self.timings.game_break
        self.max_placement_game_slots = self.total_pitches * (available_time -
                                         adj_group_game_length * self.req_group_games
                                         )//adj_game_length
        total_group_game_time = self.req_group_games * adj_group_game_length
        print("Total Tournament Time: {}".format(available_time))
        if total_group_game_time/available_time > 0.6:
            print("{} group games lasting {} ({}% of available time!)".format(self.req_group_games,
                                                     total_group_game_time,
                  100*total_group_game_time/available_time))
        if self.max_placement_game_slots < self.total_teams:
            print("Only {} game slots available for placement games!".format(self.max_placement_game_slots))
            print("Consider lengthening tournament hours, adding more pitches or removing teams")



    def create_group_stage(self):


        # For each group, as many games from the same group should play at the same time
        max_concur_games = self.group_size//2
        if max_concur_games > self.total_pitches:
            max_concur_games = self.total_pitches

        group_game_combinations = {}
        for group in self.groups.keys():
            group_game_combinations[group] = iter(cycle(create_group_match_ups(self.group_size)))
        t1_last = []
        t2_last = []
        group_last = []
        for i in range(max_concur_games):
            t1_last.append("a")
            t2_last.append("a")
            group_last.append("a")


        group_games_created = 0
        group_it = cycle(self.groups.keys())
        pitch_it = cycle(self.pitches.keys())
        group = next(group_it)
        pitch = next(pitch_it)
        i = 0
        while group_games_created < self.req_group_games:
            t1,t2 = next(group_game_combinations[group])
            if self.check_last_teams_scheduled(t1, t2, group, t1_last, t2_last, group_last):
                print(t1,t2,group,"|",t1_last,t2_last, "|", group_last)
                self.schedule.append(
                    Fixture(self.groups[group].team_list[t1],
                            self.groups[group].team_list[t2],
                            pitch,
                            None,
                            None,
                            self.groups[group]))
                t1_last[i],t2_last[i], group_last[i] = t1, t2, group
                group_games_created += 1
                pitch = next(pitch_it)
                i = i+1
                if i == max_concur_games:
                    group = next(group_it)
                    i = 0
        print("Created {} group stage games".format(group_games_created))

    def assign_timings_to_schedule(self):
        """
        Iterate through schedule, assigning timings to the fixture list
        """
        # Iterate over schedule items and iterate timings
        current_time = {}
        for pitch in self.pitches.keys():
            current_time[pitch] = self.timings.day1_start
        for fixture in self.schedule:
            if fixture.group != None:
                game_length = self.timings.group_game_length
            else:
                game_length = self.timings.game_length
            # Move to 'next day' if required
            if self.timings.day2_start > current_time[fixture.pitch] > self.timings.day1_end:
                current_time[fixture.pitch] = self.timings.day2_start

            if fixture.game_start == None:
                fixture.game_start = current_time[fixture.pitch]
                fixture.game_length = game_length
                current_time[fixture.pitch] += game_length + self.timings.game_break
            else:
                # Fixture already has a time assigned, skip
                current_time[fixture.pitch] += (fixture.game_length + self.timings.game_break)


    def print_schedule(self):
        """Output schedule in easy to read format"""
        fixtures_by_pitch = []
        for pitch in range(self.total_pitches):
            fixtures_by_pitch.append([])
        assert len(fixtures_by_pitch) == self.total_pitches, "incorrect fixtures_by_pitch initialisation"

        for fixture in self.schedule:
            fixtures_by_pitch[fixture.pitch-1].append(fixture)

        # Find longest dimension list
        longest_length = len(max(fixtures_by_pitch, key=lambda col: len(col)))
        # Time for printing to screen
        header = "{:<16}".format("Game Time")
        for pitch in range(self.total_pitches):
            header += "Pitch {:<20}".format(pitch)
        print(header)
        for i in range(longest_length):
            fixture_info = []
            fixture_info.append(" {} ".format(datetime.datetime.strftime(fixtures_by_pitch[0][i].game_start,'%d/%m %H:%M')))
            for pitch in range(self.total_pitches):
                fixture = fixtures_by_pitch[pitch][i]
                try:
                    fixture_info.append("{:10s} vs {:10s}".format(
                        fixture.team1.name, fixture.team2.name))
                except IndexError:
                    fixture_info.append("({}) {} vs {} ({})".format(
                        "-", "-", "-", "-"))

            print(" | ".join(fixture_info))
    @staticmethod
    def check_last_teams_scheduled(team1, team2, group, team1_last, team2_last, group_last):

        return ((team1 not in team1_last and
                 team1 not in team2_last and
                 team2 not in team1_last and
                 team2 not in team2_last)
                 or group not in group_last)


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

    # def __str__(self):
    #     return self.name

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
            team_str += "{:<2} {}\n".format(team.seed, team.name)
        return team_str


class Pitch:
    def __init__(self, identifier):
        self.id = identifier
        self.fixtures = []


class Fixture:
    def __init__(self, team1, team2, pitch, game_start, game_length, group = None):
        self.team1 = team1
        self.team2 = team2
        self.pitch = pitch
        self.group = group
        self.game_start = game_start
        self.game_length = game_length

    def __str__(self):
        return "{} | pitch {:3} | group {:3} |{:<10} v {:>10}".format(
            datetime.datetime.strftime(self.game_start,'%H:%M'), self.pitch, self.group.id,self.team1.name, self.team2.name)


Timings = collections.namedtuple('Timings', ['group_game_length',
                                             'game_length',
                                             'game_break',
                                             'day1_start',
                                             'day2_start',
                                             'day1_end',
                                             'day2_end'])


# if __name__ == '__main__':