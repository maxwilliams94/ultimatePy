"""
Hold references to fixtures, win/loss record, name, group affiliation of a Team
"""


class Team(object):
    def __init__(self, team_id, name):
        self.id = team_id
        self.name = name
