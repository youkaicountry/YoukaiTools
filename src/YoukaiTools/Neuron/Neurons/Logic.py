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

import YoukaiTools.Neuron.BaseNeuron as __bn
BaseNeuron = __bn.BaseNeuron

def __xbit_pins(numinputs):
    inpa = ["a"+str(x) for x in range(numinputs)]
    inpb = ["b"+str(x) for x in range(numinputs)]
    outp = [str(x) for x in range(numinputs)]
    return (inpa+inpb, outp)

#take 2 buses of size 'numinputs'.
#they will be named: 'a0, a1, a2,...a(n-1)' & 'b0, b1, b2, ...b(n-1)'.
class AndXBit(BaseNeuron):
    def __init__(self, numinputs):
        pins = __xbit_pins(numinputs)
        self.setup(*pins)
        self.numpins = numinputs
        return
    
    def doCalculation(self):
        for p in range(self.numpins):
            stp = str(p)
            self.outputs[stp] = self.inputs["a"+stp] and self.inputs["b"+stp]
        return
    
class OrXBit(BaseNeuron):
    def __init__(self, numinputs):
        pins = __xbit_pins(numinputs)
        self.setup(*pins)
        self.numpins = numinputs
        return
    
    def doCalculation(self):
        for p in range(self.numpins):
            stp = str(p)
            self.outputs[stp] = self.inputs["a"+stp] or self.inputs["b"+stp]
        return
    