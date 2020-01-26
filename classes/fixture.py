"""
Classes for a fixture (teams, time, location) and Schedule (collated fixtures)
"""
from classes.team import Team

class Fixture(object):
    def __init__(self, team1: Team, team2: Team, time_slot: int, location: int):
        self.t1 = team1
        self.t2 = team2
        self.time_slot = time_slot
        self.location = location


class Schedule(object):
    def __init__(self, tournament_name, tournament_information):
        self.t_name = tournament_name
        self.t_info = tournament_information
        # Initialise data structures
        self.time_slots = []
        self.num_pitches: int
