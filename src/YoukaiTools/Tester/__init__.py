#make a tester. Call an addTest for each test function you wish to add.
#the functions should return a result object.

import collections
from . import TesterGUI as __testerGUI

makeGUI = __testerGUI.makeGUI

class Result:
   def __init__(self, passed=True, message="--"):
      self.passed = passed
      self.message = message
      return
      
   def __str__(self):
      m = ""
      if self.passed:
         m = "PASSED"
      else:
         m = "FAILED"
      return m + ", " + self.message
      
class Test:
   def __init__(self, name="", description="--", function=None):
      self.name = name
      self.description = description
      self.function = function
      self.result = None
      return
      
   def doTest(self):
      self.result = self.function()
      return
      
   def __str__(self):
      return self.name + ":\n" + self.description + "\n" + str(self.result)
      
class Tester:
   def __init__(self):
      self.tests = collections.OrderedDict()
      return
      
   def addTest(self, name="", description = "--", function=None):
      self.tests[name] = Test(name, description, function)
      return
   
   #do the tests   
   def doAllTests(self):
      for x in self.tests:
         self.tests[x].doTest()
      return
      
   def doTest(self, name):
      self.tests[name].doTest()
      return
   
   #return result objects
   def getAllResults(self):
      ret = [self.tests[x].result for x in self.tests]
      return ret
   
   def getResult(self, name):
      return self.tests[name].result
   
   def getAllPassedResults(self):
      ret = [self.tests[x].result for x in self.tests if self.tests[x].result.passed]
      return ret
   
   def getAllFailedResults(self):
      ret = [self.tests[x].result for x in self.tests if not self.tests[x].result.passed]
      return ret
      
   def getAllTests(self):
      ret = [self.tests[x] for x in self.tests]
      return ret
   
   def getTest(self, name):
      return self.tests[name]
   
   def getAllPassedTests(self):
      ret = [self.tests[x] for x in self.tests if self.tests[x].result.passed]
      return ret
   
   def getAllFailedTests(self):
      ret = [self.tests[x] for x in self.tests if not self.tests[x].result.passed]
      return ret
      
   
         
      
