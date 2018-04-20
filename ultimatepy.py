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
        self.groupList = []
        self.seedDict = {}
        self.seedList = []

    def importTeams(self, list):
        self.teamList = list
        print("Team list imported:")
        print(str(len(self.teamList)) + " Teams\n")
        self.size = len(self.teamList)
        # create team objects
        for teamNumber, team in enumerate(self.teamList):
            self.teamDict[str(team)] = Team(str(team))
            self.teamDict[team].setSeed(teamNumber + 1)
            self.seedDict[str(teamNumber+1)] = Team(str(Team))
            self.seedList.append(teamNumber)
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
                self.groupList.append(str(chr(code)))

    def assignGroupSeeds(self):
        # assign team seeds into group seedLists
        # these will then be used to assign objects to the seedDict

    def getTeamList(self):
        for item in range(len(self.teamList)):
            print(str(item+1) + " " + str(self.teamList[item]))



class Group:
    def __init__(self,size):
        self.identifier = "0"
        self.size = size
        self.type = "-1"
        self.teamList = []

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
    def __repr__(self):
        return '{}: {}'.format(self.seed,self.name)



if __name__ == '__main__':
    swsc = Tournament('South West Super Cup')

    swsc.importTeams(['Bristol 1','Bath 2','Bristol 2','Bath 1', 'Cardiff 1', 'Swansea 1', 'Bears 1', 'UWE 2'])

    swsc.setGroupSizes()

    swsc.assignGroupSeeds()



