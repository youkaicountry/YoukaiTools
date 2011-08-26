from YoukaiTools import Tester

def test1():                            
   return Tester.Result(True, "it's okay")
   
def test2():
   return Tester.Result(True, "also okay")
   
def test3():
   return Tester.Result(False, "uh oh")
   
def test4():
   return Tester.Result(True, "yay")
   
t = Tester.Tester()
t.addTest("Test 1", "Not much of a test", test1)
t.addTest("Test 2", "Also not much", test2)
t.addTest("Test 3", "Not much again", test3)
t.addTest("Test 4", "Nope.", test4)

Tester.makeGUI(t)

t.doAllTests()

r = t.getAllFailedTests()
for x in r:
   print(str(x))
   print("")
