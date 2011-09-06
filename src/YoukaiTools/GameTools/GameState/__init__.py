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

class GameStateManager:
    def __init__(self):
        self.state_types = {}                                                   #name to object of base state objects
        self.state_instance = {}                                                #the actual instances
        self.state_instance_paused = {}                                         #boolean that tells if each value is paused or not
        self.state_instance_priority_list = []                                  #the list of all the instances, in order (prio, 
        self.state_instance_priority = {}                                       #the priority number of each instance
        self.state_instance_type = {}                                           #the specific types of each instance
        self.kill_list = []
        self.end = False
        self.messages = {}
        return
    
    ############################################################################
    # CONTROL FLOW
    ############################################################################
    def run(self):   #when it returns, it's over 
         while len(self.state_instance) != 0:
             if self.run_limited(1) == True: break
         return
    
    #returns whether the end flag has been tripped
    def run_limited(self, times):
        for x in range(times):
            l = self.state_instance_priority_list[:]
            for x in l:
                if not self.state_instance_paused[x]: self.state_instance[x].update()
                else: self.state_instance[x].pause_update()
            self.__doKills()
            if self.end: break
        return self.end
        
    def pause_instance(self, name):
        self.state_instance_paused[name] = True
        self.state_instance[name].pause_initialize()
        return
        
    def resume_instance(self, name):
        self.state_instance_paused[name] = False
        self.state_instance[name].resume_initialize()
        return
    
    def endProgram(self):
        self.end = True
        
    ############################################################################
    # TYPES
    ############################################################################
    #pointer to the class (not a specific)
    def addType(self, type_name, state):
        self.state_types[type_name] = state
        return
    
    def getTypeOfInstance(self, instance): #returns the type of an instance
        return
    
    def getTypes(self):  #returns all of the types present
        return
    
    ############################################################################
    # INSTANCES
    ############################################################################
    #create a new object of type state_type, with name instance
    def startInstance(self, state_type, name, data=None):
        s = self.state_types[state_type]()                                      #make the actual new instance
        s_name = self.__unique_identifier(name)                                 #get a unique name for the instance
        self.state_instance[s_name] = s                                         #add the instance to the instance list
        self.state_instance_paused[s_name] = False                              #add the instance to the paused list as unpaused
        self.state_instance_priority[s_name] = len(self.state_instance_priority_list)    #set the instance's priority to the lowest (should be done before adding to the list)
        self.state_instance_priority_list.append(s_name)                        #add the instance to the actual priority list
        self.state_instance_type[s_name] = state_type
        self.state_instance[s_name].manager = self
        self.state_instance[s_name].name = s_name
        self.state_instance[s_name].initialize(s_name, self, data)              #run the intialization (needs to be the last thing)
        self.messages[s_name] = []
        return s_name
    
    def killInstance(self, name, data=None):
        self.kill_list.append((name, data))
        return
    
    def getInstancesOfType(self, type_name):
        output = []
        for x in self.state_instance_priority_list:
            if self.state_instance_type[x] == type_name:
                output.append(x)
        return output
        
    def getInstances(self): #returns all of the Instances present, in priority order
        return
        
    ############################################################################
    # PRIORITY
    ############################################################################
    def setInstancePriority(self, name, priority):
        s = self.state_instance_priority_list.pop(self.state_instance_priority[name])
        self.state_instance_priority_list.insert(priority, s)
        self.state_instance_priority = {}
        self.__update_priority()
        return
    
    def getInstancePriority(self, name):
        return
    
    ############################################################################
    # MESSAGES
    ############################################################################
    def getNextMessage(self, name):
        return self.__getMessage(name, 0)
        
    def peekNextMessage(self, name):
        return self.__peekMessage(name, 0)
        
    def getNumberOfMessages(self, name):
        return len(self.messages[name])
        
    def getAllMessages(self, name):
        output = self.messages[name]
        self.messages[name] = []
        return output
        
    def peekAllMessages(self, name):
        return self.messages[name]
        
    def getMessageIndex(self, name, index):
        return self.__getMessage(name, index)
        
    def peekMessageIndex(self, name, index):
        return self.__peekMessage(name, index)
        
    
    def sendMessageToInstance(self, name, message):  #send a message to a specific instance
        self.__sendMessage(name, message)
        return
    
    def sendMessageToType(self, type_name, message): #send a message to all instances of a specific type
        inst = self.getInstancesOfType(type_name)
        for x in inst:
            self.__sendMessage(x, message)
        return
        
    def sendMessageToAll(self, message):
        for x in self.state_instance_priority_list:
            self.__sendMessage(x, message)
        return
        
    def sendMessageToAllTypesBut(self, but_type, message):
        return
        
    def sendMessageToAllInstancesBut(self, but_name, message):
        return
    
    ############################################################################
    # PRIVATE METHODS
    ############################################################################
    def __doKills(self):
        for x in self.kill_list:
            self.__kill(x[0], x[1])
        self.kill_list = []
        return
        
    def __kill(self, name, data):
        self.state_instance[name].destroy(data)
        self.state_instance.pop(name)
        self.state_instance_paused.pop(name)
        self.state_instance_priority_list.pop(self.state_instance_priority[name])
        self.state_instance_priority.pop(name)
        self.state_instance_type.pop(name)
        self.messages.pop(name)
        self.__update_priority()
        return
        
    def __sendMessage(self, instance, message):
        self.messages[instance].append(message)
        return
        
    def __peekMessage(self, name, index):
        return self.messages[name][index]
        
    def __getMessage(self, name, index):
        return self.messages[name].pop(index)
        
    #gets a unique instance name
    def __unique_identifier(self, name):
        n = name[:]
        i = 2
        while n in self.state_instance.keys():
            n += "-" + str(i)
            i += 1
        return n
        
    def __update_priority(self):
        for i in range(len(self.state_instance_priority_list)):
            self.state_instance_priority[self.state_instance_priority_list[i]] = i
        return



################################################################################
# THE GAME STATE OBJECT
################################################################################
class GameState:
    def __init__(self):
        self.manager = None
        self.name = ""
        return
    
    def initialize(self, name, manager, data):
        return
    
    def update(self):
        return
    
    def pause_initialize(self, message):
        return
    
    def pause_update(self):
        return
    
    def resume_initialize(self, message):
        return
    
    def destroy(self, data):
        return