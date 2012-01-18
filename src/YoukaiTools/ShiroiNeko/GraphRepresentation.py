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

import random
from math import sqrt, cos, sin
import math
twopi = math.pi*2.0

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
            sn2d.breakforce[p] = graph.getEdgeData(edge, bonddef['breakforce'])
            sn2d.spring[p] = graph.getEdgeData(edge, bonddef['spring'])
            if not calclength: 
                sn2d.length[p] = graph.getEdgeData(edge, bonddef['length'])
    vid = globaldef['id']
    sn2d.dt = graph.getVertexData(vid, globaldef['dt'])
    sn2d.macrogravity = graph.getVertexData(vid, globaldef['macrogravity'])
    sn2d.time = graph.getVertexData(vid, globaldef['time'])
    sn2d.collisionson = graph.getVertexData(vid, globaldef['collisionson'])
    sn2d.macrogravity = graph.getVertexData(vid, globaldef['macrogravity'])
    sn2d.fluidfriction = graph.getVertexData(vid, globaldef['fluidfriction'])
    sn2d.coulombon = graph.getVertexData(vid, globaldef['coulombconstant'])
    return sn2d

def getBasicGlobalDef():
    out = {}
    names = ['macrogravity', 'time', 'collisionson', 'macrogravity', 'fluidfriction', 'coulombon', 'coulombconstant', 'dt']
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
    names = ['type', 'p1', 'p2', 'spring', 'length', 'breakforce']
    for name in names:
        out[name] = name
    out['typeval'] = 'bond'
    return out

def randomAddBond(graph, maxdist, r=None, globaldef=None, particledef=None):
    if r is None:
        r = random.Random()
    if globaldef is None:
        globaldef = getBasicGlobalDef()
    if particledef is None:
        particledef = getBasicParticleDef()
    n = graph.getOrder() - 1
    maxbonds = n * (n-1) / 2
    if maxbonds == graph.getSize():
        return None
    bondlist = [x for x in graph.getVertexList() if ((len(graph.getAdjacentEdges(x)) < (n-1)) and x != globaldef['id'])]
    if len(bondlist) < 2: raise Exception("Nonsensical input.")
    r.shuffle(bondlist)
    for one in xrange(len(bondlist)-1):
        for two in xrange(one+1, len(bondlist)):
            p1 = bondlist[one]
            p2 = bondlist[two]
            dx = graph.getVertexData(p1, particledef['xposition']) - graph.getVertexData(p2, particledef['xposition'])
            dy = graph.getVertexData(p1, particledef['yposition']) - graph.getVertexData(p2, particledef['yposition'])
            dist = sqrt(dx*dx + dy*dy)
            if dist <= maxdist:
                return (p1, p2)
    return None

def randomDelBond(graph, r=None, particledef=None):
    if graph.getSize() < 1:
        return None
    if r is None:
        r = random.Random()
    if particledef is None:
        particledef = getBasicParticleDef()
    bonds = graph.getEdgeList()
    r.shuffle(bonds)
    bond = bonds[0]
    bi = graph.getEdgeInfo(bond)
    p1 = bi[0]
    p2 = bi[1]
    graph.removeEdge(bond)
    if len(graph.getAdjacentEdges(p1)) < 1:
        if not graph.getVertexData(p1, particledef['fixed']):
            graph.removeVertex(p1)
    if len(graph.getAdjacentEdges(p2)) < 1:
        if not graph.getVertexData(p2, particledef['fixed']):
            graph.removeVertex(p2)
    return True

def randomAddParticle(graph, maxdist, r=None, globaldef=None, particledef=None):
    if r is None:
        r = random.Random()
    if globaldef is None:
        globaldef = getBasicGlobalDef()
    if particledef is None:
        particledef = getBasicParticleDef()
    if graph.getOrder() < 2:
        return None
    vertices = [x for x in graph.getVertexList() if x != globaldef['id']]
    if len(vertices) < 1:
        return None
    r.shuffle(vertices)
    vertex = vertices[0]
    dist = r.random()*maxdist
    angle = r.random()*twopi
    newx = graph.getVertexData(vertex, particledef['xposition']) + (cos(angle)*dist)
    newy = graph.getVertexData(vertex, particledef['yposition']) + (cos(angle)*dist)
    return (vertex, newx, newy)
