#Copyright (c) <2011-2012> <Nathaniel Caldwell>

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

#unsimplified range conversion equation:
#(((val - abs(min_s)) / (max_s - min_s)) * (max_t - min_t)) + min_t
def rangeToRange(value, min_source, max_source, min_target, max_target):
    return (normalize(value, min_source, max_source) * (max_target - min_target)) + min_target

def normalize(value, min_source, max_source):
    bottom = max_source - min_source
    return ((value - min_source) / bottom) if bottom != 0 else max_source
    
#finds min and max of a given list, and returns range converted values
def histogramConvert(values, min_target, max_target):
    return

