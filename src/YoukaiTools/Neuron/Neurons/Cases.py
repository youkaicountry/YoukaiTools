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
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

from ..BaseNeuron import BaseNeuron

import YoukaiTools.GraphEngine as GraphEngine

class BreadBoard(BaseNeuron):
    #neurons should be a dic {"neuron_name": neuron, ...}
    #inputs should be a dictionary {"inp": "what_to_call_it"}
    #constants should be a dic {"inp":const, ...}
    #wires should be [("output", "input"), ...]
    def __init__(self, neurons, input_names, output_names, constants, wires, default=0):
        self.neurons = neurons
        inputset = set(input_names.keys())
        missinginputpins = []
        internalinputpins = set()
        #enumerate the internal pins, and missing problem pins
        for w in wires:
            internalinputpins.add(w[1])
        for k in neurons.keys():
            for inp in neurons[k].inputs.keys():
                thisi = k+"."+inp
                if (thisi not in inputset) and (thisi not in internalinputpins) and (thisi not in constants):
                    missinginputpins.append(thisi)
        
        #set the constants, including missing pins
        self.constants = []
        for c in constants:
            self.constants.append((self.__getTuple(c), constants[c]))
        for m in missinginputpins:
            self.constants.append((self.__getTuple(m), default))
        
        #construct the input pin and output pin maps
        self.input_map = {}
        for k in input_names:
            self.input_map[input_names[k]] = self.__getTuple(k)
            
        self.output_map = {}
        for k in output_names:
            self.output_map[output_names[k]] = self.__getTuple(k)
        
        #call the base neuron setup
        self.setup([i for i in self.input_map.keys()], [i for i in self.output_map.keys()])
        
        #construct the graph of the wires
        self.graph = GraphEngine.BasicGraph()
        for n in neurons:
            self.graph.addVertex(n)
        for w in wires:
            outp = self.__getTuple(w[0])
            inp = self.__getTuple(w[1])
            e = self.graph.addEdge(outp[0], inp[0], True)
            self.graph.setEdgeData(e, "outpin", outp[1])
            self.graph.setEdgeData(e, "inpin", inp[1])
            self.graph.setEdgeData(e, "end", inp[0])
        return
    
    def doCalculation(self):
        #prep the unresolved set
        unresolved = set()
        for k in self.neurons.keys():
            unresolved.add(k)
        
        #reset all neurons
        for k in unresolved:
            self.neurons[k].reset()
        
        #set all constant inputs
        for c in self.constants:
            self.neurons[c[0][0]].inputs[c[0][1]] = c[1]
        
        #carry through input_map pins to the proper inputs
        for k in self.inputs.keys():
            inf = self.input_map[k]
            self.neurons[inf[0]].setInput(inf[1], self.inputs[k])
        
        #iterate through the list of unresolved neurons
        #when one complete, find outbound edges on graph
        #set the proper inputs
        #remove resolved neuron from the list of unresolved
        #repeat if there are still unresolved
        takeout = set()
        while len(unresolved) > 0:
            for n in unresolved:
                thisneuron = self.neurons[n]
                if thisneuron.calculate():
                    takeout.add(n)
                    outbound = GraphEngine.GraphTools.Paths.getInboundEdges(self.graph, n)
                    for o in outbound:
                        outpin = self.graph.getEdgeData(o, "outpin")
                        inpin = self.graph.getEdgeData(o, "inpin")
                        end = self.graph.getEdgeData(o, "end")
                        self.neurons[end].setInput(inpin, thisneuron.getOutput(outpin))
            unresolved = unresolved - takeout
        
        #carry through output_map pins to the case outputs
        for k in self.outputs.keys():
            outf = self.output_map[k]
            self.outputs[k] = self.neurons[outf[0]].getOutput(outf[1])
            
        return
    
    def __getTuple(self, name):
        sp = name.split(".")
        return (".".join(sp[:-1]), sp[-1])
    