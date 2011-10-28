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

import Algorithms, BaseGA, SelectionTypes
import FillTypes
__all__ = ["Algorithms", "BaseGA"]

def make_gene(fitness, mate, mutate, random_dna, basic_dna, report=lambda obj,fitness,generation,topgeneration:1):
    d = {}
    d["fitness"] = fitness
    d["mate"] = mate
    d["mutate"] = mutate
    d["random_dna"] = random_dna
    d["basic_dna"] = basic_dna
    d["report"] = report
    return d
        
def make_options(selection, selection_settings, deletion, deletion_settings, fill, fill_settings, mc, mimin, mimax):
    d = {}
    d["selection"] = selection
    d["selection_settings"] = selection_settings
    d["deletion"] = deletion
    d["deletion_settings"] = deletion_settings
    d["fill"] = fill
    d["fill_settings"] = fill_settings
    d["mutation_chance"] = mc
    d["mutation_intensity_min"] = mimin
    d["mutation_intensity_max"] = mimax
    return d
