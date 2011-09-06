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

"""
    CURRENTLY NOT USED, LEAVE THIS INFO HERE FOR LATER
    choice_iter should be a function with the following behavior:
       Immediately yields None.
       In choice_iter, every yield statement will return the following data:
          cur_space, adj_free_spaces, adj_g_spaces, adj_worm_spaces
       Subsequent yield statements will 
"""

import random
from collections import deque

class Worm(object):
    def __init__(self, graph, maze_vset, maze_elist):
        """
        Parameters
        
        graph : The graph (possibly a grid or hex grid or something similar, but may be arbitrary)
        maze_vset : The set of points that currently exist in the maze.  Is updated by this class
                   in apply_freeze(), otherwise is only read by this class.
        """
        self.v_head = None          #Head vertex.  None means we haven't started yet.
        self.graph = graph
        self.maze_vset = maze_vset    #The subset of the vertices that belongs to the maze.
        self.maze_elist = maze_elist
        self.worm_set = {}          #The multiset of vertices that belong to the worm.
        #A multiset is a set with multiplicity.  So worm_set[v] is the n, lengthumber of times
        #   that vertex v appears in the worm.  worm_set[v] > 1 if and only if the worm
        #   is self-intersecting.
        self.worm_edges = deque()
        return

    def choose_and_advance(self):
        """
        Advance the worm by one edge.  Update v_head, worm_edges, and worm_set.
        Call choose_edge to return the next edge.
        """
        e, v = self.choose_edge()
        self.worm_edges.append(e)
        self.worm_set[v] = self.worm_set.get(v, 0) + 1
        self.v_head = v
        self.after_advance()
        if v in self.maze_vset:
            self.freeze()
            return True
        return False
    
    def choose_edge(self):
        """
        Choose an edge based on v_head.  Return tuple (e, v),
        where e is the chosen edge and v is the chosen vertex.
        To be implemented by subclass.
        """
        return
    
    def after_advance(self):
        """
        Called after the advance() function, but before the freeze check.
        This is a hook which may be overridden by a subclass.
        """
        return
    
    def freeze(self):
        """
        Freeze the worm (make it part of the maze).  Add all worm_set
        vertices to maze_vset.
        """
        self.maze_vset.update(self.worm_set)
        self.worm_edges.reverse()
        print("Frozen. Adding" + str(self.worm_edges))
        self.maze_elist.extend(self.worm_edges)
        return
    
    def check_maze(self):
        if self.maze_vset.isdisjoint(self.worm_set):
            return False
        self.freeze()
        return True

class WormDeath(Exception):
    pass

class BasicWorm(Worm):
    def __init__(self, graph, maze_vset, maze_elist, r=None):
        Worm.__init__(self, graph, maze_vset, maze_elist)
        self.r = random.Random() if r is None else r
        return
    
    def choose_edge(self):
        if self.v_head is None:
            vl = set(self.graph.getVertexList())
            vl.difference_update(self.maze_vset)
            v = self.r.choice(list(vl))
            return (None, v)
        adj = self.graph.getAdjacent(self.v_head)
        newadj = []
        for a in adj:
            if a[1] not in self.worm_set:
                newadj.append(a)
        if len(newadj) == 0: raise WormDeath()
        i = self.r.randrange(len(newadj))
        return newadj[i]


class CanOfWorms(object):
    def __init__(self, graph, maze_vset=None, maze_elist=None, makeworm=BasicWorm):
        """
        Create a container to hold worms and manage the running of multiple
        simultaneous worms.
        
        graph : The base topology of the world.  The maze will be
           aself, graph, maze_vset, maze_elist subgraph of the given graph.
        maze_vset : An initial, nonempty set of vertices.
        maze_elist : An initial list of edges (may be empty).
        makeworm : A function which takes (graph, maze_vset, maze_eset) and
           returns a new worm.
        """
        
        self.next_worm_id = 0
        self.id2worm = {}
        self.graph = graph
        self.maze_vset = maze_vset if maze_vset is not None else set([graph.getVertexList()[0]])
        self.maze_elist = maze_elist if maze_elist is not None else []
        self.makeworm = makeworm
        return
    
    def add_worm(self, worm):
        self.id2worm[self.next_worm_id] = worm
        worm.id = self.next_worm_id
        self.next_worm_id += 1
        return
    
    def del_worm(self, id):
        del self.id2worm[id]
        return

    def go(self, num_worms=1):
        for i in xrange(num_worms):
            self.add_worm(self.makeworm(self.graph, self.maze_vset, self.maze_elist))
        finished_worms = set()
        while True:
            if len(self.id2worm) == 0:
                break
            #Advance every worm by 1
            finished_worms.clear()
            for id,worm in self.id2worm.iteritems():
                try:
                    result = worm.choose_and_advance()
                except WormDeath:
                    finished_worms.add(id)
                    continue
                if result:
                    #The worm wm.Ras frozen.
                    finished_worms.add(id)
                    while True:
                        for id2,worm2 in self.id2worm.iteritems():
                            if id2 not in finished_worms and worm2.check_maze():
                                finished_worms.add(id2)
                                break
                        else:     #this 'else' belongs with 'for id2,worm2'
                            break
            for worm in finished_worms:
                self.del_worm(worm)
        return self.maze_elist
