from itertools import cycle
import collections
import datetime
from copy import deepcopy


def create_group_match_ups(group_size):
    """
    Create a list of tuples for possible team1 and team2 index
    combinations. When a team is chosen as t1, it is removed from t2
    to stop double counting
    :param group_size: number of teams in a group
    :return: a list of match up tuples
    """
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
            self.groups[i] = Group(i, self.group_size)

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

        self.current_time_slot = self.timings.day1_start


    def create_group_stage(self):
        """
        """
        self.max_concurrent_games = min([self.total_pitches, self.group_size//2])

        # Create dictionary of group game match ups (as fixtures)
        match_ups = {}
        match_priority = {}
        for group in self.groups.values():
            match_ups[group.index] = []
            match_priority[group.index] = []
            match_up_indices = create_group_match_ups(self.group_size)
            for t1,t2 in match_up_indices:
                match_ups[group.index].append(deepcopy(Fixture(group.team_list[t1],
                                                               group.team_list[t2],
                                                               -1,
                                                               None,
                                                               None,
                                                               group.index)))


        group_cycle = cycle(iter(list(self.groups.keys())))
        pitch_cycle = cycle(range(self.total_pitches))
        fixtures_remaining = self.req_group_games

        pitch = next(pitch_cycle)
        group = next(group_cycle)
        iconcurrent = 0
        while fixtures_remaining > 0:

            # Get match priorities
            match_priority = self.return_match_priorities(match_ups)
            prioritised_match_index = match_priority[group].index(max(match_priority[group]))
            match_to_append = match_ups[group].pop(prioritised_match_index)

            # Assign Time and Pitch to match before adding to schedule
            match_to_append.game_start = self.current_time_slot
            match_to_append.pitch = pitch
            self.schedule.append(match_to_append)
            iconcurrent += 1

            # Increment pitch for next game
            pitch = next(pitch_cycle)
            if pitch == 0:
                # Pitch choice has has just cycled around: must move to next time slot
                self.current_time_slot = self.increment_current_time(self.current_time_slot, group_game=True)
                # print("Incremented Time P={} T={}".format(pitch, datetime.datetime.strftime(self.current_time_slot,'%H:%M')))

            # Increment group if max concurrent games has been reached
            if iconcurrent == self.max_concurrent_games:
                iconcurrent = 0
                group = next(group_cycle)

            # Count number of fixtures remaining within match_ups
            fixtures_remaining = 0
            for l in match_ups.values():
                fixtures_remaining += len(l)


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

    def return_match_priorities(self, remaining_matches):
        """
        :return index linked match priority dictionary of lists
        Prioritise a match according to:
            Slots since last match
            Already playing in current slot?
            Games already played(?)
        :parameter remaining_matches - dictionary of lists
        """
        # Iterate through list, assessing current priority of match
        # relative to current fixture list

        priorities = {}
        for g_key,group in remaining_matches.items():
            priorities[g_key] = []
            for match_up in group:
                # Assess match priority
                # Slots since last match
                # Games already played
                # Work backwards through schedule
                t1_games_played = 0
                t1_last_game_time = self.timings.day1_start
                t2_games_played = 0
                t2_last_game_time = self.timings.day1_start
                for fixture in self.schedule:
                    if (fixture.team1 == match_up.team1 or fixture.team1 == match_up):
                        t1_games_played += 1
                        t1_last_game_time = fixture.game_start
                    if (fixture.team2 == match_up.team1 or fixture.team2 == match_up.team2):
                        t2_last_game_time = fixture.game_start
                        t2_games_played += 1

                # lowest_games_played = min([t1_games_played, t2_games_played])
                total_games_played = t1_games_played + t2_games_played
                time_since_last_game = min([self.current_time_slot - t1_last_game_time,
                                             self.current_time_slot - t2_last_game_time])

                priority = (24.0 - time_since_last_game.seconds/3600.0) + (10 - total_games_played)*10
                if time_since_last_game < (min([self.timings.game_length, self.timings.group_game_length]) + self.timings.game_break):
                    if t1_games_played == 0 and t2_games_played == 0:
                        pass
                    else:
                        priority = -1000

                priorities[g_key].append(priority)

        return priorities

    def increment_current_time(self, current_time, group_game):
        """
        :param current_time: datetime object
        :param group_game: bool
        :return: incremented time
        """
        if group_game:
            g_length = self.timings.group_game_length
        else:
            g_length = self.timings.game_length

        current_time += (g_length + self.timings.game_break)
        if current_time >= self.timings.day1_end:
            current_time = self.timings.day2_end

        return current_time


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
        return "{} {}".format(self.seed, self.name)

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


class Pitch:
    def __init__(self, identifier):
        self.id = identifier
        self.fixtures = []


class Fixture:
    def __init__(self, team1, team2, pitch, game_start, game_length, group = None):
        self.team1 = team1  # Team Object
        self.team2 = team2  # Team Object
        self.pitch = pitch  #
        self.group = group  # Group ID
        self.game_start = game_start
        if self.game_start == None:
            self.game_start = datetime.datetime.now()
        self.game_length = game_length

    def __str__(self):
        return "{} | pitch {:3} | group {:3} |{:<10} v {:>10}".format(
            datetime.datetime.strftime(self.game_start,'%H:%M'), self.pitch, self.group,self.team1.name, self.team2.name)


Timings = collections.namedtuple('Timings', ['group_game_length',
                                             'game_length',
                                             'game_break',
                                             'day1_start',
                                             'day2_start',
                                             'day1_end',
                                             'day2_end'])


# if __name__ == '__main__':