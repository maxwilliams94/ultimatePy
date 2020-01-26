from archive.groups import Group
from archive.teams import Team
from logging import Logging
from itertools import cycle
import datetime
from copy import deepcopy
from sys import exit
import collections
from os import path, getcwd


class Tournament:
    """
    Store (and initialise) dictionary and storage structures
    Contains dictionaries for teams, groups, pitches which in turn
    contain values which are Team, Group and Pitch object respectively.
    """

    def __init__(self, team_list, name="tournament"):
        self.name = name
        self.log_file = path.join(getcwd(), self.name + ".log")
        self.groups = {}
        self.teams = {}
        self.pitches = {}
        self.schedule = []

        self.group_size = 0
        self.total_groups = 0
        self.total_teams = 0
        self.total_pitches = 0

        self.max_placement_game_slots = 0
        self.max_concurrent_games = 0
        self.req_group_games = 0

        # Timings
        self.timings = Timings
        self.current_time_slot = datetime.datetime

        # Populate teams with Team objects
        for pos, team in enumerate(team_list):
            self.teams[pos + 1] = Team(team, pos + 1)
        self.total_teams = len(team_list)

        Logging.write_log_event(self.log_file,
                                'Tournament object initialisation',
                                'Populated dict teams',
                                'Total teams: {}'.format(self.total_teams))

    def create_groups(self, group_size=4):
        self.group_size = group_size
        self.total_groups = self.total_teams // self.group_size

        print("{} groups of {} teams".format(self.total_groups, group_size))

        self.req_group_games = self.total_groups * (self.group_size * (self.group_size - 1)) // 2
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

    def create_pitches(self, total_pitches=2):
        self.total_pitches = total_pitches

        for id in range(total_pitches):
            self.pitches[id] = Pitch(id)

    def set_timings(self, timings):
        self.timings = timings

        length_day1 = self.timings.day1_end - self.timings.day1_start
        length_day2 = self.timings.day2_end - self.timings.day2_start
        available_time = length_day1 + length_day2
        adj_group_game_length = self.timings.group_game_length + self.timings.game_break
        adj_game_length = self.timings.game_length + self.timings.game_break
        self.max_placement_game_slots = self.total_pitches * (available_time -
                                                              adj_group_game_length * (
                                                                      self.req_group_games // self.total_pitches)
                                                              ) // adj_game_length
        total_group_game_time = (self.req_group_games * adj_group_game_length) / self.total_pitches
        print("Total Tournament Time: {}".format(available_time))
        if total_group_game_time / available_time > 0.6:
            print("{} group games lasting {} ({}% of available time!)".format(self.req_group_games,
                                                                              total_group_game_time,
                                                                              100 * total_group_game_time / available_time))
        if self.max_placement_game_slots < self.total_teams:
            print("Only {} game slots available for placement games!".format(self.max_placement_game_slots))
            print("Consider lengthening tournament hours, adding more pitches or removing teams")

        self.current_time_slot = self.timings.day1_start

    def create_group_stage(self):
        """
        create match_ups dictionary of Fixture objects
        assign_fixtures_to_schedule()
            get_match_priority()
        """
        self.max_concurrent_games = min([self.total_pitches, self.group_size // 2])

        Logging.write_log_event(self.log_file,
                                "create_group_stage",
                                "",
                                'max concurrent games: {}'.format(self.max_concurrent_games))

        # Create dictionary of group game match ups (as fixtures)
        match_ups = {}
        for group in self.groups.values():
            match_ups[group.index] = self.create_group_fixtures(group)

        self.assign_fixtures_to_schedule(self.groups.keys(), match_ups, group_game=True, log_stage="create_group_stage")

    @staticmethod
    def get_group_match_up_indices(group_size):
        """
        Create a list of tuples for possible team1 and team2 index
        combinations. When a team is chosen as t1, it is removed from t2
        to stop double counting
        :rtype: tuple array
        :param group_size: number of teams in a group
        """
        match_ups = []
        team_ones = list(range(0, group_size))
        team_twos = list(range(0, group_size))
        for t1 in team_ones:
            for t2 in team_twos:
                if t1 != t2:
                    match_ups.append((t1, t2))

            team_twos.pop(team_twos.index(t1))

        return match_ups

    def assign_fixtures_to_schedule(self, group_keys, fixtures, group_game, log_stage="-"):
        """
        :param group_keys: list of groups, made into a cycled iterable
        :param fixtures: dictionary of fixtures with pitch, time emitted, containing only the teams involved
        :param group_game: True/False
        :param log_stage: information for logging
        :return: None
        """
        groups_it = cycle(iter(group_keys))
        pitches = cycle(range(self.total_pitches))
        pitch = next(pitches)
        group = next(groups_it)
        i_concurrent = 0
        assigned_fixtures = 0
        match_to_append = Fixture(None, None, None, None, None)

        Logging.write_log_event(self.log_file,
                                log_stage,
                                'assign_fixtures_to_schedule',
                                'Begin assigning {} games to schedule'.format(
                                    sum(len(matches) for matches in fixtures.values())))

        while True:
            # Get match priorities
            match_priority = self.return_match_priorities(fixtures)
            try:
                prio_i_match = match_priority[group].index(max(match_priority[group]))
            except ValueError:
                print("Assigned {} fixtures to the schedule".format(assigned_fixtures))
                break

            match_to_append = fixtures[group].pop(prio_i_match)

            # Assign Time and Pitch to match before adding to schedule
            match_to_append.game_start = self.current_time_slot
            match_to_append.pitch = pitch
            # Log chosen fixture to append
            Logging.write_log_event(path.join(getcwd(), 'create_group_stage.log'),
                                    log_stage,
                                    'highest priority match chosen',
                                    'T:{} P:{} T1:{} T2:{} Priority:{:5.0f}'
                                    .format(match_to_append.game_start.strftime('%H:%M'),
                                            match_to_append.pitch,
                                            match_to_append.team1.name,
                                            match_to_append.team2.name,
                                            match_priority[group][prio_i_match]))
            self.schedule.append(match_to_append)
            assigned_fixtures += 1
            i_concurrent += 1

            # Increment pitch for next game
            pitch = next(pitches)
            if pitch == 0:
                # Pitch choice has has just cycled around: must move to next time slot
                self.current_time_slot = self.increment_current_time(self.current_time_slot, group_game=group_game)

            # Increment group if max concurrent games has been reached
            if i_concurrent == self.max_concurrent_games:
                i_concurrent = 0
                group = next(groups_it)

        return None

    def create_bracket(self):
        """
        top x, the rest decided by group stage
        Match ups:
        Top8/bottom 8
        1-8,2-7,3-6,4-5
        """
        top_half = self.total_teams // 2
        if top_half % 2 != 0:
            if top_half <= 7:
                top_half += 1
            else:
                top_half -= 1

        grouped_seeds = {'top': list(range(1, top_half + 1)), 'bottom': list(range(top_half + 1, self.total_teams + 1))}

        if len(grouped_seeds['bottom']) % 2 != 0:
            print("Must have even number of teams in bottom half of bracket")
            print(len(grouped_seeds['bottom']))
            exit(1)

        # Create dictionary of lists of level 1 bracket match ups
        # todo dictionary creation should be in a method to avoid repetition for both group and bracket stages
        seed_combos = {}
        match_ups = {}
        for g in ['top', 'bottom']:
            seed_combos[g] = []
            while len(grouped_seeds[g]) > 0:
                t1 = grouped_seeds[g].pop(0)
                t2 = grouped_seeds[g].pop(-1)
                seed_combos[g].append((t1, t2))

            # Turn match up seed combinations to a dict of fixtures
            match_ups[g] = []
            for t1, t2 in seed_combos[g]:
                match_ups[g].append(deepcopy(Fixture(self.teams[t1],
                                                     self.teams[t2],
                                                     -1,
                                                     None,
                                                     None,
                                                     None)))

        # Assign match ups to schedule
        self.assign_fixtures_to_schedule(['top', 'bottom'], match_ups, group_game=False, log_stage="create_bracket")

    def create_group_fixtures(self, group):
        # Generate list of (t1, t2) tuples for a generic group
        matchup_indices = self.get_group_match_up_indices(self.group_size)
        group_fixtures = []
        for t1, t2 in matchup_indices:
            group_fixtures.append(deepcopy(Fixture(group.get_team_by_index(t1),
                                                   group.get_team_by_index(t2),
                                                   -1,
                                                   None,
                                                   None,
                                                   group.index)))

        return group_fixtures

    def assign_timings_to_schedule(self):
        """
        Iterate through schedule, assigning timings to the fixture list
        """
        # Iterate over schedule items and iterate timings
        current_time = {}
        for pitch in self.pitches.keys():
            current_time[pitch] = self.timings.day1_start
        for fixture in self.schedule:
            if fixture.group is not None:
                game_length = self.timings.group_game_length
            else:
                game_length = self.timings.game_length
            # Move to 'next day' if required
            if self.timings.day2_start > current_time[fixture.pitch] > self.timings.day1_end:
                current_time[fixture.pitch] = self.timings.day2_start

            if fixture.game_start is None:
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
            fixtures_by_pitch[fixture.pitch].append(fixture)

        # Find longest dimension list
        longest_length = len(max(fixtures_by_pitch, key=lambda col: len(col)))
        # Time for printing to screen
        header = "{:<16}".format("Game Time")
        for pitch in range(self.total_pitches):
            header += "Pitch {:<20}".format(pitch)
        print("longest_length", longest_length)
        print(header)
        for i in range(longest_length):
            fixture_info = [
                " {} ".format(datetime.datetime.strftime(fixtures_by_pitch[0][i].game_start, '%d/%m %H:%M'))]
            for pitch in range(self.total_pitches):
                try:
                    fixture = fixtures_by_pitch[pitch][i]
                    fixture_info.append("{:<10s} vs {:<10s}".format(fixture.team1.name,
                                                                    fixture.team2.name))
                except IndexError:
                    fixture_info.append("{:^10s} vs {:^10s}".format("-", "-", "-", "-"))

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
        for g_key, group in remaining_matches.items():
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
                    if fixture.team1.id == match_up.team1.id or fixture.team2.id == match_up.team2.id:
                        t1_games_played += 1
                        t1_last_game_time = fixture.game_start
                    if fixture.team1.id == match_up.team1.id or fixture.team2.id == match_up.team2.id:
                        t2_last_game_time = fixture.game_start
                        t2_games_played += 1

                # lowest_games_played = min([t1_games_played, t2_games_played])
                total_games_played = t1_games_played + t2_games_played
                time_since_last_game = min([self.current_time_slot - t1_last_game_time,
                                            self.current_time_slot - t2_last_game_time])

                priority = (24.0 - time_since_last_game.seconds / 3600.0) + (10 - total_games_played) * 10
                if time_since_last_game < (
                        min([self.timings.game_length, self.timings.group_game_length]) + self.timings.game_break):
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


class Pitch:
    def __init__(self, identifier):
        self.id = identifier
        self.fixtures = []


class Fixture:
    def __init__(self, team1, team2, pitch, game_start, game_length, group=None):
        self.team1 = team1  # Team Object
        self.team2 = team2  # Team Object
        self.pitch = pitch  #
        self.group = group  # Group ID
        self.game_start = game_start
        if self.game_start is None:
            self.game_start = datetime.datetime.now()
        self.game_length = game_length

    def __str__(self):
        if self.group is None:
            group = "-"
        else:
            group = self.group
        return "{} | pitch {:3} | group {:3} |{:<10} v {:>10}".format(
            datetime.datetime.strftime(self.game_start, '%H:%M'), self.pitch, group, self.team1.name, self.team2.name)


Timings = collections.namedtuple('Timings', ['group_game_length',
                                             'game_length',
                                             'game_break',
                                             'day1_start',
                                             'day2_start',
                                             'day1_end',
                                             'day2_end'])
