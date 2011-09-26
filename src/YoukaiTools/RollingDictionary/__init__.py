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

#A memory efficient dictionary for iterable entries with
#many similar roots

class RollingDictionary(object):
    def __init__(self):
        self.dic = {"root": (None, None, None)}
        self.next = 0
        #have a cache of last n words, with number of lookups
        #and remove lowest number of lookups when need a new space
        return
    
    
    #returns last letter
    def addEntry(self, word, data):
        here = self.__addWord(word)
        self.__addDataByLastLetter(here, data)
        return
    
    def getEntry(self, word):
        x = self.__lookupWord(word)
        d = self.dic[x[1]][2]
        if x[0] and (d is not None):
            return self.dic[x[1]][2]
        else:
            raise KeyError, str(word) + " not in dictionary."
    
    #BUILT IN SPECIAL FUNCTIONS:
    def __contains__(self, x):
        return self.__lookupWord(x)[0]
    
    def __getitem__(self, key):
        return self.getEntry(key)
    
    #returns last letter
    def __addWord(self, word):
        lr = self.__lookupWordWithRest(word)
        here = self.__addWordFrom(lr)
        return here
    
    
    #adds the rest of a word from a lookup return with rest
    def __addWordFrom(self, lookup_return):
        here = lookup_return[1]
        for o in lookup_return[2]:
            here = self.__addLetter(here, o)
        return here
    
    def __addLetter(self, last_letter, new_letter):
        n = self.next
        self.dic[n] = (last_letter, None, None)
        if self.dic[last_letter][1] is None: self.dic[last_letter] = (self.dic[last_letter][0], {}, self.dic[last_letter][2])
        self.dic[last_letter][1][new_letter] = n
        self.next += 1
        return n
    
    def __addDataByLastLetter(self, last_letter, data):
        self.dic[last_letter] = (self.dic[last_letter][0], self.dic[last_letter][1], data)
        return
    
    def __addDataByWord(self, word, data):
        l = self.lookupWord(word)
        self.__addDataByLastLetter(l[1], data)
        return 
    
    #returns (isIn, last_letter)
    def __lookupWord(self, word):
        here = "root"
        for i, o in enumerate(word):
            if self.__wordContains(here, o):
                here = self.dic[here][1][o]
            else:
                return (False, here)
        return (True, here, None)
    
    #returns (isIn, last_letter, remaining)
    def __lookupWordWithRest(self, word):
        here = "root"
        for i, o in enumerate(word):
            if self.__wordContains(here, o):
                here = self.dic[here][1][o]
            else:
                return (False, here, word[i:])
        return (True, here, None)
    
    def __wordContains(self, last_letter, next_letter):
        if self.dic[last_letter][1] is None: return False
        return next_letter in self.dic[last_letter][1]

#(parent, childrendic, entriesdic)
