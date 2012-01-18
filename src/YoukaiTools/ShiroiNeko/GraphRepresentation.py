#Copyright (c) <2012> <Nathaniel Caldwell>

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

import SN2D

"""
This module contains functions which handle conversions of physics objects to and from
graph representations.
"""

def graphToPhysics(graph, globaldef=None, particledef=None, bonddef=None):
    if globaldef is None:
        globaldef = getBasicGlobalDef()
    if particledef is None:
        particledef = getBasicParticleDef()
    if bonddef is None:
        bonddef = getBasicBondDef()
    sn2d = SN2D.SN2D()
    for vertex in graph.getVertexList():
        d = graph.getVertexData(vertex, particledef['type'])
        if d == particledef['typeval']: #then we have a particle
            p = sn2d.newParticle([vertex])[0]
            sn2d.xposition[p] = graph.getVertexData(vertex, particledef['xposition'])
            sn2d.yposition[p] = graph.getVertexData(vertex, particledef['yposition'])
            sn2d.xvelocity[p] = graph.getVertexData(vertex, particledef['xvelocity'])
            sn2d.yvelocity[p] = graph.getVertexData(vertex, particledef['yvelocity'])
            sn2d.xacceleration[p] = graph.getVertexData(vertex, particledef['xacceleration'])
            sn2d.yacceleration[p] = graph.getVertexData(vertex, particledef['yacceleration'])
            sn2d.fixed[p] = graph.getVertexData(vertex, particledef['fixed'])
            sn2d.mass[p] = graph.getVertexData(vertex, particledef['mass'])
            sn2d.charge[p] = graph.getVertexData(vertex, particledef['charge'])
    for edge in graph.getEdgeList():
        d = graph.getEdgeData(edge, bonddef['type'])
        if d == bonddef['typeval']: #then we have a bond
            calclength = 'length' in graph.getEdgeDataKeys()
            p = sn2d.newBond([edge], calclength = calclength)[0]
            sn2d.p1[p] = graph.getEdgeData(edge, bonddef['p1'])
            sn2d.p2[p] = graph.getEdgeData(edge, bonddef['p2'])
            sn2d.spring[p] = graph.getEdgeData(edge, bonddef['spring'])
            if not calclength: 
                sn2d.length[p] = graph.getEdgeData(edge, bonddef['length'])
    vid = globaldef['id']
    sn2d.dt = graph.getVertexData(vid, globaldef['dt'])
    sn2d.macrogravity = graph.getVertexData(vid, globaldef['macrogravity'])
    sn2d.time = graph.getVertexData(vid, globaldef['time'])
                
            
            

def getBasicGlobalDef():
    out = {}
    names = ['macrogravity', 'time', 'collisionson', 'macrogravity', 'fluidfriction', 'coulonbon', 'coulombconstant', 'dt']
    for name in names:
        out[name] = name
    out["id"] = "global"
    return out

def getBasicParticleDef():
    out = {}
    names = ['type', 'xposition', 'yposition', 'xvelocity', 'yvelocity', 'xacceleration', 'yacceleration', 'mass', 'fixed', 'charge']
    for name in names:
        out[name] = name
    out['typeval'] = 'particle'
    return out

def getBasicBondDef():
    out = {}
    names = ['type', 'p1', 'p2', 'spring', 'length']
    for name in names:
        out[name] = name
    out['typeval'] = 'bond'
    return out
