#Copyright (c) <2011> <Nathaniel Caldwell>

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

#the gene class        
class Gene:
    #should return the fitness of obj.
    #do not modify obj
    def getFitness(self, obj):
        return 1
    
    #should return a mate of obj1 and obj2
    #do not modify obj1 and obj2
    def mate(self, obj1, obj2):
        return 1
    
    #should return a mutation of obj, keeping the intensity in mind
    def mutate(self, intensity, obj):
        return 1
    
    def getRandom(self):
        return 1
    
    def getBasic(self):
        return 1
    
    def report(self, obj, fitness, generation, topgeneration):
        return 1

#the options class
class Options:
    selection = 0
    deletion = 0
    fill = 0
    mutationchance = 0
    mutationintensitymin = 0
    mutationintensitymax = 0
    def __init__(self, selection, deletion, fill, mc, mimin, mimax):
        self.selection = selection
        self.deletion = deletion
        self.fill = fill
        self.mutationchance = mc
        self.mutationintensitymin = mimin
        self.mutationintensitymax = mimax