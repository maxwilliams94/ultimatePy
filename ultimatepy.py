import numpy as np
from numpy import genfromtxt

class Tournament:
    def __init__(self,name):
        self.name = name
        self.size = -1
        self.structure = "null"
        self.numberOfGroups = 0
        self.teamList = []
        self.possGroupings = []
        self.teamDict = {}
        self.groupDict = {}

    def importTeams(self, list):
        self.teamList = list
        print("Team list imported:")
        print(str(len(self.teamList)) + " Teams\n")
        self.size = len(self.teamList)
        # create team objects
        for teamNumber, team in enumerate(self.teamList):
            self.teamDict[str(team)] = Team(str(team))
            self.teamDict[team].setSeed(teamNumber + 1)
        for groupSize in range(1,10):
            if (self.size/groupSize) % 2 == 0:
                self.possGroupings.append(groupSize)


        if len(self.possGroupings) == 0:
            print("No possible groupings")

    def setGroupSizes(self):
        print("Possible Even Group Sizes:")
        for item in self.possGroupings:
            print(str(int(self.size/item))+" groups of "+str(item))

        while (self.numberOfGroups == 0):
            chosenGroupSize = input('Enter Number of groups required: ')
            if (self.size/int(chosenGroupSize) % 2 == 0):
                self.numberOfGroups = chosenGroupSize

        if self.numberOfGroups != 0:
            for code in range(65,65+int(self.numberOfGroups)):
                self.groupDict[str(chr(code))] = Group(chr(code))
                self.groupDict[str(chr(code))].size = int(self.size)/int(self.numberOfGroups)

    def getTeamList(self):
        for item in range(len(self.teamList)):
            print(str(item+1) + " " + str(self.teamList[item]))



class Group:
    def __init__(self,size):
        self.identifier = "0"
        self.size = size
        self.type = "-1"

class Team:
    def __init__(self,name):
        self.name = name
        self.seed = -1
        self.group = ""
        self.groupSeed = -1

    def setSeed(self, seed):
        self.seed = seed

    def getName(self):
        print(self.name)

    def getSeed(self):
        print(self.seed)



