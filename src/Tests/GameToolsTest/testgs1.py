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
