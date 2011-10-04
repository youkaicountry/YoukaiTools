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
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

from YoukaiTools import GeneAlg

class Train(GeneAlg.User.Gene):
    #input_dic should be a dictionary with input name as keys, and 
    #(initial value, standard deviation) as value.
    #test_list is a list of tuples: [(input_test, output_test)]
    #input_test & output_test are dictionaries {name:val, name:val, ...}
    def __init__(self, neuron, input_dic, test_set, default_input=0, mutation_range=(0, 1), maxp = 10000000000):
        st = GeneAlg.SelectionTypes.TourneySelect(5)
        dt = GeneAlg.SelectionTypes.TourneyLowSelect(5)
        fill = GeneAlg.FillTypes.BasicFill(self)
        op = GeneAlg.User.Options(st, dt, fill, .9, .00, 1.0)
        self.GA = GeneAlg.Algorithms.Pool(self, op, 200)
        return
    
    