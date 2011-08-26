from YoukaiTools import RollingDictionary
import sys

'''
Created on Jun 15, 2011

@author: nathan
'''

if __name__ == '__main__':
    rd = RollingDictionary.RollingDictionary()
    rd.addEntry("man", 1)
    rd.addEntry("mantis", 2)
    rd.addEntry("mantle", 3)
    print(rd.dic)
    
    nd = {}
    nd["man"] = 1
    nd["mantis"] = 2
    nd["mantle"] = 3
    pass