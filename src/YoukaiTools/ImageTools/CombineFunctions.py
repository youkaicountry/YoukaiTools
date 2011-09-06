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

def paint(p1, p2):
    return p2[:]

def multiply(p1, p2):
    out = []
    for i,c in enumerate(p1):
        #print(i, c, p2[i])
        out.append(c*p2[i])
    return out

def average(p1, p2, weight1, weight2):
    div = weight1+weight2
    out = []
    for i, c in enumerate(p1):
        out.append(((c*weight1) + (p2[i]*weight2))/div)
    return out

def add(p1, p2, top=1.0):
    out = []
    for i,c in enumerate(p1):
        #print(i, c, p2[i])
        a = c+p2[i]
        if a > top: a = top
        out.append(a)
    return out
