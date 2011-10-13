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

from ..BaseChip import BaseChip
import itertools

#A neuron that takes all of its input, and inverts them.
class InvertNeuron(BaseChip):
    def __init__(self, numinputs):
        self.inp = ["in"+str(x) for x in range(numinputs)]
        self.out = ["out"+str(x) for x in range(numinputs)]
        self.setup(self.inp, self.out)
        return
    
    def doCalculation(self):
        for i, o in itertools.izip(self.inp, self.out):
            self.outputs[o] = -self.inputs[i]
        return

class Add(BaseChip):
    def __init__(self):
        self.setup(["a", "b"], ["out"])
    
    def doCalculation(self):
        self.outputs["out"] = self.inputs["a"] + self.inputs["b"]
        return

class Multiply(BaseChip):
    def __init__(self):
        self.setup(["a", "b"], ["out"])
    
    def doCalculation(self):
        self.outputs["out"] = self.inputs["a"] * self.inputs["b"]
        return
