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

#Base state
#Upon transition to a new state, 
class State:
    def __init__(self, state_machine):
        return
    
    def generateData(self, state):
        return None
    
    def transitionIn(self, state, data):
        return
    
    def transitionOut(self, state, data):
        return
    
    def setStateMachine(self, state_machine):
        self.state_machine = state_machine
    
class StateMachine:
    #states should be a list of tuples [(state_name, state), ...], or None.
    def __init__(self, states=None, state_generator=None):
        self.states = {}
        if states is not None:
            for s in states:
                self.addState(*s)
        self.state_generator = state_generator
        return
    
    def addState(self, state_name, state_obj):
        self.states[state_name] = state_obj
        return
    
    def spawnInstance(self, start_state_name=None):
        instance = {}
        instance["state"] = None
        instance["data"] = None
        if start_state_name is not None:
            self.transition(instance, start_state_name)
        return instance
    
    def transition(self, instance, to_state_name):
        if instance["state"] is not None:
            instance["state"][1].transtionOut(to_state_name, instance["data"])
        
        s = self.getState(to_state_name)
        d = s[1].generate_data(s)
        self.__modify_instance(instance, s, d)
        instance["state"][1].transitionIn(s, instance["data"])
        return 
    
    def __modify_instance(self, instance, state, data):
        instance["state"] = state
        instance["data"] = data
        return
    
    def getState(self, state_name):
        if state_name in self.states:
            return (state_name, self.state[state_name])
        else:
            if self.state_generator is not None:
                return (state_name, self.state_generator)
            else:
                raise Exception, "No state generator."
        return