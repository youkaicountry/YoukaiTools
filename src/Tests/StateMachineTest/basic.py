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

def s1_data(sm):
    print("s1 data")
    return {1:1}

def s1_tin(sm, from_s, from_d):
    print("s1 tin")
    sm["current_data"][1] += 1
    return

def s1_tout(sm, to_s):
    print("s1 tout")
    print(sm["current_data"])
    return

def s2_data(sm):
    print("s2 data")
    return {2:2}

def s2_tin(sm, from_s, from_d):
    print("s2 tin")
    sm["current_data"][2] += 1
    return

def s2_tout(sm, to_s):
    print("s2 tout")
    print(sm["current_data"])
    return

s1 = StateMachine.newState(s1_data, s1_tin, s1_tout)
s2 = StateMachine.newState(s2_data, s2_tin, s2_tout)

sm = StateMachine.newStateMachine([("state1", s1), ("state2", s2)], start_state_name="state1")
StateMachine.transition(sm, "state2")
StateMachine.transition(sm, "state1")
