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

import YoukaiTools.StateMachine as StateMachine

class state1(StateMachine.State):
    def __init__(self):
        return
    
    def generateData(self, state):
        return {1:1}
    
    def transitionIn(self, state, data):
        print("1 transition in.")
        data[1] = data[1] + 1
        print(data)
        return
    
    def transitionOut(self, state, data):
        print("1 transition out")
        print(data)
        return
    
class state2(StateMachine.State):
    def __init__(self):
        return
    
    def generateData(self, state):
        return {2:2}
    
    def transitionIn(self, state, data):
        print("2 transition in.")
        data[1] = data[1] + 2
        print(data)
        return
    
    def transitionOut(self, state, data):
        print("2 transition out")
        print(data)
        return

s1 = state1()
s2 = state2()

sm = StateMachine.StateMachine([("state1", s1), ("state2", s2)])
inst = sm.spawnInstance("state1")
print(inst)
