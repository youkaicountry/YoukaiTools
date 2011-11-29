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

from math import tanh

from ..BaseChip import BaseChip

import Cases

# Threshold functions.
def thresh_spin(u, T):
    return 1.0 if u > T else -1.0

def thresh_meanfield(u, T):
    return tanh(u/T)

def thresh_passthrough(u, T):
    return u

class ArtificalNeuron(BaseChip):
    #if threshold_const is None, there will be an input pin for it, else it will
    #be set to the value given
    #if threshold_func is None, there will be no threshold function, else it
    #calls the function given with (u, T) as parameters
    def __init__(self, numinputs, threshold_const=1.0, threshold_func=thresh_meanfield):
        self.threshold_const = threshold_const
        self.threshold_func = threshold_func
        self.inp = ["in"+str(i) for i in xrange(numinputs)]
        self.weight = ["w"+str(i) for i in xrange(numinputs)]
        t = ["T"] if threshold_const is None else []
        self.setup(self.inp+self.weight+t, ["out"])
        self.numinputs = numinputs
        return
    
    def doCalculation(self):
        u = 0
        self_inp = self.inp
        for i in xrange(self.numinputs):
            u += (self.inputs[self_inp[i]] * self.inputs[self.weight[i]])
        T = self.inputs["T"] if self.threshold_const is None else self.threshold_const
        self.outputs["out"] = u if self.threshold_func is None else self.threshold_func(u, T)
        return

#layers = [num, num, num, ...], where num is the number of chips
#in each layer
#layer_Tconst is a list of thresholds for each layer. each should be None if no consts 
#layer_tfunc is a list of what threshold function to use in each layer
class ForwardFeedNeuralNetwork(BaseChip):
    def __init__(self, layers, layer_tconst, layer_tfunc, default_const=0):
        chips = {}
        constants = {}
        wires = []
        inputs = []
        outputs = []
        order = []
        for layer in xrange(len(layers)):
            for chip in xrange(layers[layer]):
                name = "l"+str(layer)+"c"+str(chip)
                order.append(name)
                inpnum = 1 if layer == 0 else layers[layer-1]
                chips[name] = ArtificalNeuron(inpnum, layer_tconst[layer], layer_tfunc[layer])
                for inum in xrange(inpnum):
                    nw = name+"_w"+str(inum)
                    inputs.append(nw)
                    wires.append((nw, name+".w"+str(inum)))
                if layer_tconst[layer] is None:
                    nt = name+"_T" 
                    inputs.append(name+"_T")
                    wires.append((nt, name+".T"))
                if layer == 0:
                    inp = "in"+str(chip)
                    wires.append((inp, name+".in0"))
                    inputs.append(inp)
                if layer == len(layers)-1:
                    outp = "out"+str(chip)
                    wires.append((name+".out", outp))
                    outputs.append(outp)
                else:
                    l = layer+1
                    ln = "l"+str(l)
                    for c in xrange(layers[l]):
                        wires.append((name+".out", ln+"c"+str(c)+".in"+str(chip)))
        self.bb = Cases.BreadBoard(chips, inputs, outputs, constants, wires, optimized_order=order)
        #inputs = ["in"+str(i) for i in range(layers[0])]
        #outputs = ["out"+str(i) for i in range(layers[-1])]
        self.setup(inputs, outputs)
        return

    def doCalculation(self):
        for x in self.inputs:
            self.bb.inputs[x] = self.inputs[x]
        self.bb.doCalculation()
        for x in self.outputs:
            self.outputs[x] = self.bb.outputs[x]

