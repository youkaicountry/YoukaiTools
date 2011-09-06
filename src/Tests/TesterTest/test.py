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
