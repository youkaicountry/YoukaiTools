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

from YoukaiTools import GameTools

class A(GameTools.GameState):
    def __init__(self):
        self.i = 0
        return
        
    def initialize(self, name, manager, data):
        print("A(" + self.name+ ") INIT")
        return
    
    def update(self):
        print("A(" + self.name + ") UPDATE " + str(self.i))
        self.i += 1
        if self.i == 5: self.manager.killInstance("game")
        if self.i == 10:
            a = self.manager.getInstancesOfType("B")
            self.manager.setInstancePriority(a[0], 0)
        if self.i == 15: self.manager.endProgram() 
        return
        
    def destroy(self, data):
        print("A(" + self.name+ ") DESTROY")
        return

class B(GameTools.GameState):
    def __init__(self):
        self.i = 0
        return
        
    def initialize(self, name, manager, data):
        print("B(" + self.name+ ") INIT")
        return
        
    def update(self):
        print("B(" + self.name+ ") UPDATE " + str(self.i))
        self.i += 1
        return
        
    def destroy(self, data):
        print("B(" + self.name+ ") DESTROY")
        return
        
gsm = GameTools.GameStateManager()
gsm.addType("A", A)
gsm.addType("B", B)
gsm.startInstance("A", "main_driver")
gsm.startInstance("B", "game")
gsm.startInstance("B", "game")
gsm.run()
