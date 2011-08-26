from YoukaiTools import AdvFunctions

#This file contains functions that create new images either from simple
#parameters, or from simple modifications to given input images

#if channels = none, initialcolor is a full array of the base color
#if channels = some int, then channels is the number of channels,
#and initial color is ust some single value
#If indata != None, then it just uses that as the full data. If channels is
#set, it uses that as channel num, else it tried to calculate it
def newImage(width, height, initialcolor=[0, 0, 0], channels=None, indata=None):
    if indata != None:
        c = channels
        if channels == None:
            c = len(indata[0])
        return [width, height, c] + indata
    if channels == None: 
        ic = initialcolor
        number_channels = len(initialcolor)
    else:
        ic = [initialcolor]*channels
        number_channels = channels
    head = [width, height, number_channels]
    body = []
    for i in range(width*height):
        body += [ic[:]]
    return head + body

