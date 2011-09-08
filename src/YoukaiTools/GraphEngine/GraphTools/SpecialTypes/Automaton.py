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

import YoukaiTools.GraphEngine

#AUTOMATON:
#nodes:
#data[0] = (start?, nodedata)
#data["nodestart"] = startnode?
#data["nodereturn"] = return value
#edges:
#MUST BE DIRECTED
#data["transition"] = (object), 'object is None' means that it is empty (free move)

#dfa - properly formed dfa
#indata - list whose objects are the string to be simulated
#startstate - the state (node id) whose objects are the string to be simulated
#returns: (endstate, enddata)  
def simulateDFA(dfa, indata, startstate):
    return

def move(fa, state, symbol):
    movestate = set()
    for v in state:
        edges = fa.getConnectingEdges(v)
        for e in edges:
            if fa.getEdgeData(e, "transition") == symbol: movestate.add(fa.getEdgeEnd(v, e))
    return movestate

def dfaNotation(dfa):
    return
   
def nfaNotation(nfa):
    return

#return the e closure of the given state (given as a set)
def eclosure(nfa, state):
    tocheck = state.copy()   
    checked = set()
    while len(tocheck) > 0:
        l = [x for x in tocheck]
        for o in l: #objects in tocheck
            edges = nfa.getConnectingEdges(o)
            for e in edges:
                if nfa.getEdgeData(e, "transition") is None:
                    end = nfa.getEdgeEnd(o, e)
                    if end not in checked : tocheck.add(end)
            checked.add(o)
            tocheck.remove(o)
    return checked

#takes a graph that is a properly formed NFA. Returns True if at the end a marker is 
#on a state whose return = accept. Otherwise returns False
#nfa - properly formed NFA graph object
#indata - list whose objects are the string to be simulated
#startstate - a list of states that have initial markers
#returns: (endstate, endstate) 
def simulateNFA(nfa, indata, startstate):
    currentstate = set()
    for x in startstate:
        currentstate.add(x)
    tstate = set()
   
    #make free moves initially
    currentstate = eclosure(nfa, currentstate)
   
    #main loop
    for o in indata:
        currentstate = eclosure(nfa, move(nfa, currentstate, o))
      
    out = [x for x in currentstate]
    return (out, [nfa.getVertexData(x, "nodereturn") for x in out])

#give it an empty graph, it fills it
def makeNFAFromRegEx(graph, regex, endstatedata, otherstatedata):
    return
   
#calls makeNFAFromRegEx, then convertNFA2DFA
def makeDFAFromRegEx(graph, regex, endstatedata, otherstatedata):
    return

#returns the output of the given state
def __getout(fa, state, accept, decline):
    for x in state:
        if fa.getVertexData(x, "nodereturn") == accept : return accept
    return decline
   
def convertNFA2DFA(dfaout, nfa, startstate, accept, decline):
    dfaout.clearGraph()
    #get the alphabet from the edges
    alphabet = set()
    for e in nfa.getEdgeList():
        d = nfa.getEdgeData(e, "transition")
        if d != None:
            alphabet.add(d)
   
    salphabet = [x for x in alphabet] #static alphabet
    #rint(salphabet)
   
    zerostate = eclosure(nfa, startstate)
    currentstate = zerostate
   
    #the dfa table
    set2id = {}
    id2symbol = {}
    id2marked = {}
    id2set = {}
    tabletop = 1
   
    #set up the initial state:
    set2id[frozenset(zerostate)] = 0
    id2set[0] = frozenset(zerostate)
    id2symbol[0] = {}
    id2marked[0] = False
    currentid = 0
   
    #now do the main loop
    while True:
        #notout = True
        #for k in id2marked.keys():
        #   notout = notout and id2marked[k]
        # if not notout : break
      
        for a in salphabet:
            s = frozenset(eclosure(nfa, move(nfa, id2set[currentid], a)))
            if s in set2id.keys(): #already in table
                id2symbol[currentid][a] = set2id[s]
            else: #not in table, make a new entry
                set2id[s] = tabletop
                id2set[tabletop] = s
                id2symbol[tabletop] = {}
                id2marked[tabletop] = False
                id2symbol[currentid][a] = tabletop
                tabletop += 1
            
      
        id2marked[currentid] = True
      
        #print(str(currentid) + " " + str(tabletop))
        currentid += 1
        if currentid >= tabletop : break
   
    #for x in range(currentid):
    #   print(id2symbol[x])
   
    #now construct the table
    v = currentid
    e = []
    vdata = {}
    for i in range(currentid):
        for a in id2symbol[i].keys():
            e.append((i, id2symbol[i][a], 1, [("transition", a)]))
        vdata[i] = [("nodereturn", __getout(nfa, id2set[i], accept, decline))]
   
   
    YoukaiTools.GraphEngine.GraphTools.Builders.buildGraph(dfaout, v, e, vdata)
   
    print("v: " + str(v))
    print("e: " + str(e))
    print("vdata: " + str(vdata)) 
    return

