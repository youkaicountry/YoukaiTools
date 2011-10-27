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

def xbit_pins(numinputs):
    inpa = ["a"+str(x) for x in range(numinputs)]
    inpb = ["b"+str(x) for x in range(numinputs)]
    outp = ["out"+str(x) for x in range(numinputs)]
    return (inpa, inpb, outp)

class Nand(BaseChip):
    def __init__(self):
        self.setup(["a", "b"], ["out"])
    
    def doCalculation(self):
        self.outputs["out"] = not(self.inputs["a"] and self.inputs["b"])

class And(BaseChip):
    def __init__(self):
        self.setup(["a", "b"], ["out"])
    
    def doCalculation(self):
        self.outputs["out"] = self.inputs["a"] and self.inputs["b"]

class Or(BaseChip):
    def __init__(self):
        self.setup(["a", "b"], ["out"])
    
    def doCalculation(self):
        self.outputs["out"] = self.inputs["a"] or self.inputs["b"]

class Xor(BaseChip):
    def __init__(self):
        self.setup(["a", "b"], ["out"])
    
    def doCalculation(self):
        a = self.inputs["a"]
        b = self.inputs["b"]
        self.outputs["out"] = (a or b) and not (a and b)

class Not(BaseChip):
    def __init__(self):
        self.setup(["a"], ["out"])
        return
    
    def doCalculation(self):
        self.outputs["out"] = not self.inputs["a"]

#take 2 buses of size 'numinputs'.
#they will be named: 'a0, a1, a2,...a(n-1)' & 'b0, b1, b2, ...b(n-1)'.
class AndXBit(BaseChip):
    def __init__(self, numinputs):
        pins = xbit_pins(numinputs)
        self.setup(pins[0]+pins[1], pins[2])
        self.numpins = numinputs
        self.ina = pins[0]
        self.inb = pins[1]
        self.out = pins[2]
        return
    
    def doCalculation(self):
        for i in range(self.numpins):
            self.outputs[self.out[i]] = self.inputs[self.ina] and self.inputs[self.inb]
        return
    
class OrXBit(BaseChip):
    def __init__(self, numinputs):
        pins = xbit_pins(numinputs)
        self.setup(pins[0]+pins[1], pins[2])
        self.numpins = numinputs
        self.ina = pins[0]
        self.inb = pins[1]
        self.out = pins[2]
        return
    
    def doCalculation(self):
        for i in range(self.numpins):
            self.outputs[self.out[i]] = self.inputs[self.ina] or self.inputs[self.inb]
        return

class NandXBit(BaseChip):
    def __init__(self, numinputs):
        pins = xbit_pins(numinputs)
        self.setup(pins[0]+pins[1], pins[2])
        self.numpins = numinputs
        self.ina = pins[0]
        self.inb = pins[1]
        self.out = pins[2]
        return
    
    def doCalculation(self):
        for i in range(self.numpins):
            self.outputs[self.out[i]] = not(self.inputs[self.ina] and self.inputs[self.inb])
        return

class Register(BaseChip):
    def __init__(self, default_val = False):
        self.value = default_val
        self.setup(["in", "set"], ["out"])
        return
    
    def doCalculation(self):
        if self.inputs["load"]:
            self.value = self.inputs["in"]
        self.outputs["out"] = self.value
        return
