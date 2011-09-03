import BaseOptions
import random

#settings = 
class TourneySelect(BaseOptions.BaseSelect):
    def __init__(self, settings):
        BaseOptions.BaseSelect.__init__(self, settings)
    
    def getSelection(self, objectlist):
        numtomake = self.settings
        templist = []
        highesti = 0
        highestval = None
        for x in range(numtomake):
            a = random.randint(0, len(objectlist)-1)
            templist.append((objectlist[a][0], objectlist[a][1], a))
            if objectlist[a][0] > highestval:
                highestval = objectlist[a][0]
                highesti = len(templist)-1
        #templist.sort()
        #print templist
        return templist[highesti][2]
    
    def getSettingsInfo(self):
        return ["tourney size - the size of the tournament",]
    
class TourneyLowSelect(BaseOptions.BaseSelect):
    def __init__(self, settings):
        BaseOptions.BaseSelect.__init__(self, settings)
        
    def getSelection(self, objectlist):
        numtomake = self.settings
        templist = []
        lowesti = 0
        lowestval = ()
        for x in range(numtomake):
            a = random.randint(0, len(objectlist)-1)
            templist.append((objectlist[a][0], objectlist[a][1], a))
            if objectlist[a][0] < lowestval:
                lowestval = objectlist[a][0]
                lowesti = len(templist)-1
        #templist.sort()
        return templist[lowesti][2]
    
    def getSettingsInfo(self):
        return ["tourney size - the size of the tournament",]
    
#a = [(1.1, "yukkuri"), (4, "shitte"), (3.3, "itte"), (2.3, "ne"), (7, "touhou"), (2.7, "patchy"), (1.5, "aya"), (4.4, "suwako")] 