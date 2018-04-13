import numpy as np
from numpy import genfromtxt

class Tournament:
    def __init__(self,name):
        self.name = name
        self.size = -1
        self.structure = "null"
        self.number_of_groups = 0
        self.team_list = []

    def import_teams(self,list):
        self.team_list = list
        print("Team list imported:")
        print(self.team_list)

    def get_team_list(self):
        for item in range(len(self.team_list)):
            print(str(item+1)+ " " + str(self.team_list[item]))

    #def create_teams(self):
        #for index,name_of_team in enumerate(self.team_list):


class Group:
    def __init__(self):
        self.identifier = "0"
        self.size = 0
        self.type = "-1"

class Team:
    def __init__(self,name):
        self.name = name
        self.seed = -1

    def set_seed(self,seed):
        self.seed = seed

    def get_name(self):
        print(self.name)

    def get_seed(self):
        print(self.seed)



