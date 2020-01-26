"""
Data structure/class for holding references to fixtures, win/loss record, name, group affiliation of a Team
"""

class Team(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name
