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

#def data_func(state_machine)
#def transition_in_func(state_machine, from_state, from_data)
#def transition_out_func(state_machine, to_state)

#data_func is a pointer to a function takes the state machine and returns arbitrary data
#transition_in_func is a pointer to a function that takes the state machine and the from_state and does whatever it wants 
def newState(data_func, transition_in_func, transition_out_func):
    return (data_func, transition_in_func, transition_out_func)
    
#{"current_state":(name, state), "current_data":data, "states":states, "state_generator":state_generator}
#states should be a list of tuples [(state_name, state), ...], or None.
def newStateMachine(states=None, state_generator=None, start_state_name=None):
    state_generator = state_generator
    sm = {"current_state":(None, None), "current_data":None, "states":{}, "state_generator":state_generator}
    if states is not None:
        for s in states:
            addState(sm, *s)
    transition(sm, start_state_name)
    return sm
    
def addState(sm, state_name, state_obj):
    sm["states"][state_name] = state_obj
    return
    
def transition(state_machine, to_state_name):
    s = getState(state_machine, to_state_name)
    if s == (None, None): return
    os = state_machine["current_state"]
    od = state_machine["current_data"]
    if state_machine["current_state"] != (None, None):
        #transition out
        state_machine["current_state"][1][2](state_machine, s)
    state_machine["current_state"] = s
    #generate data
    state_machine["current_data"] = s[1][0](state_machine)
    
    #transition in
    state_machine["current_state"][1][1](state_machine, os, od)
    
    return 
    
def getState(state_machine, state_name):
    if state_name is None: return (None, None)
    if state_name in state_machine["states"]:
        return (state_name, state_machine["states"][state_name])
    else:
        if state_machine["state_generator"] is not None:
            return (state_name, state_machine["state_generator"])
        else:
            raise Exception, "No state generator."
    return
    