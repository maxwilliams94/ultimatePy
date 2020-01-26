"""
Tournament class: storage of teams, schedules and output methods
"""
from collections import namedtuple

TournamentDay = namedtuple('TournamentDayTimings', 'date t_start t_end num_pitches')  # Day-specific information
DayTiming = TournamentDay


class Tournament(object):
    def __init__(self):
        self.teams = []  # List of team objects
        self.schedule = None


class TournamentInfo(object):
    """
    timings, details of a tournament
    """
    def __init__(self, num_days: int, init_timings: DayTiming):
        """
        Pass in simplest values on initialisation, set individual timings via method if required
        """
        self.num_days = num_days
        self.timings = [init_timings] * num_days

    def set_day_timing(self, day: int, timings: DayTiming):
        self.timings[day-1] = timings
