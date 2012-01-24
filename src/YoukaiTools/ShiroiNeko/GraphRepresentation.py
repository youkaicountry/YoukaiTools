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

basic_global = None
basic_particle = None
basic_bond = None

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
        if 'type' not in graph.getVertexDataKeys(vertex): continue
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
        if 'type' not in graph.getEdgeDataKeys(edge): continue
        d = graph.getEdgeData(edge, bonddef['type'])
        if d == bonddef['typeval']: #then we have a bond
            calclength = bonddef['length'] not in graph.getEdgeDataKeys(edge)
            ei = graph.getEdgeInfo(edge)
            p = sn2d.newBond(ei[0], ei[1], edge, calclength = calclength)
            sn2d.breakforce[p] = graph.getEdgeData(edge, bonddef['breakforce'])
            sn2d.spring[p] = graph.getEdgeData(edge, bonddef['spring'])
            if not calclength: 
                sn2d.length[p] = graph.getEdgeData(edge, bonddef['length'])
    vid = globaldef['id']
    sn2d.dt = graph.getVertexData(vid, globaldef['dt'])
    sn2d.macrogravityon = graph.getVertexData(vid, globaldef['macrogravityon'])
    sn2d.time = graph.getVertexData(vid, globaldef['time'])
    sn2d.collisionson = graph.getVertexData(vid, globaldef['collisionson'])
    sn2d.macrogravity = graph.getVertexData(vid, globaldef['macrogravity'])
    sn2d.fluidfriction = graph.getVertexData(vid, globaldef['fluidfriction'])
    sn2d.coulombon = graph.getVertexData(vid, globaldef['coulomb_constant'])
    return sn2d

def physicsToGraph(sn2d, graph, globaldef=None, particledef=None, bonddef=None):
    if globaldef is None:
        globaldef = getBasicGlobalDef()
    if particledef is None:
        particledef = getBasicParticleDef()
    if bonddef is None:
        bonddef = getBasicBondDef()
    addGlobalToGraph(graph, sn2d.dt, sn2d.macrogravityon, sn2d.macrogravity, sn2d.time, sn2d.collisionson, sn2d.fluidfriction, sn2d.coulombon, sn2d.coulomb_constant, globaldef)
    for p in sn2d.particlelist:
        addParticleToGraph(graph, sn2d.xposition[p], sn2d.yposition[p], sn2d.xvelocity[p], sn2d.yvelocity[p], sn2d.xacceleration[p], sn2d.yacceleration[p], sn2d.mass[p], sn2d.fixed[p], sn2d.charge[p], particledef)
    for b in sn2d.bondlist:
        addBondToGraph(graph, sn2d.p1[b], sn2d.p2[b], sn2d.spring[b], sn2d.breakforce[b], sn2d.length[b], bonddef)
    return
    

def addGlobalToGraph(graph, dt, macrogravityon, macrogravity, time, collisionson, fluidfriction, coulombon, coulomb_constant, globaldef=None):
    if globaldef is None:
        globaldef = getBasicGlobalDef()
    vid = graph.addVertex(globaldef['id'])
    graph.setVertexData(vid, globaldef['dt'], dt)
    graph.setVertexData(vid, globaldef['macrogravityon'], macrogravityon)
    graph.setVertexData(vid, globaldef['macrogravity'], macrogravity)
    graph.setVertexData(vid, globaldef['time'], time)
    graph.setVertexData(vid, globaldef['collisionson'], collisionson)
    graph.setVertexData(vid, globaldef['fluidfriction'], fluidfriction)
    graph.setVertexData(vid, globaldef['coulombon'], coulombon)
    graph.setVertexData(vid, globaldef['coulomb_constant'], coulomb_constant)
    return vid

def addParticleToGraph(graph, xposition, yposition, xvelocity, yvelocity, xacceleration, yacceleration, mass, fixed, charge, important = False, particledef=None):
    if particledef is None:
        particledef = getBasicParticleDef()
    vid = graph.addVertex()
    graph.setVertexData(vid, particledef['xposition'], xposition)
    graph.setVertexData(vid, particledef['yposition'], yposition)
    graph.setVertexData(vid, particledef['xvelocity'], xvelocity)
    graph.setVertexData(vid, particledef['yvelocity'], xvelocity)
    graph.setVertexData(vid, particledef['xacceleration'], xacceleration)
    graph.setVertexData(vid, particledef['yacceleration'], yacceleration)
    graph.setVertexData(vid, particledef['mass'], mass)
    graph.setVertexData(vid, particledef['fixed'], fixed)
    graph.setVertexData(vid, particledef['charge'], charge)
    graph.setVertexData(vid, 'type', particledef['typeval'])
    if important:
        graph.setVertexData(vid, 'important', True)
    return vid

def addBondToGraph(graph, p1, p2, spring, breakforce, important = False, length = None, bonddef=None):
    if bonddef is None:
        bonddef = getBasicBondDef()
    eid = graph.addEdge(p1, p2)
    graph.setEdgeData(eid, bonddef['spring'], spring)
    graph.setEdgeData(eid, bonddef['breakforce'], breakforce)
    if length is not None:
        graph.setEdgeData(eid, bonddef['length'], length)
    graph.setEdgeData(eid, 'type', bonddef['typeval'])
    if important:
        graph.setEdgeData(eid, 'important', True)
    return eid

def getBasicGlobalDef():
    global basic_global
    if basic_global is None:
        basic_global = {}
        names = ['macrogravityon', 'time', 'collisionson', 'macrogravity', 'fluidfriction', 'coulombon', 'coulomb_constant', 'dt']
        for name in names:
            basic_global[name] = name
        basic_global["id"] = "global"
    return basic_global

def getBasicParticleDef():
    global basic_particle
    if basic_particle is None:
        basic_particle = {}
        names = ['type', 'xposition', 'yposition', 'xvelocity', 'yvelocity', 'xacceleration', 'yacceleration', 'mass', 'fixed', 'charge']
        for name in names:
            basic_particle[name] = name
        basic_particle['typeval'] = 'particle'
    return basic_particle

def getBasicBondDef():
    global basic_bond
    if basic_bond is None:
        basic_bond = {}
        names = ['type', 'spring', 'length', 'breakforce']
        for name in names:
            basic_bond[name] = name
        basic_bond['typeval'] = 'bond'
    return basic_bond

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
    #if len(bondlist) < 2: raise Exception("Nonsensical input.")
    if len(bondlist) < 2: return None
    r.shuffle(bondlist)
    for one in xrange(len(bondlist)-1):
        for two in xrange(one+1, len(bondlist)):
            if one == two: continue
            p1 = bondlist[one]
            p2 = bondlist[two]
            if graph.getVertexData(p1, particledef['fixed']) and graph.getVertexData(p2, particledef['fixed']):
                continue 
            if p2 in graph.getAdjacentVertices(p1):
                continue
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
    bonds = [x for x in graph.getEdgeList() if 'important' not in graph.getEdgeDataKeys(x)]
    if len(bonds) < 1: return None
    r.shuffle(bonds)
    bond = bonds[0]
    bi = graph.getEdgeInfo(bond)
    p1 = bi[0]
    p2 = bi[1]
    graph.removeEdge(bond)
    if len(graph.getAdjacentEdges(p1)) < 1:
        if 'important' not in graph.getVertexDataKeys(p1):
            graph.removeVertex(p1)
    if len(graph.getAdjacentEdges(p2)) < 1:
        if 'important' not in graph.getVertexDataKeys(p2):
            graph.removeVertex(p2)
    return True

def randomAddParticle(graph, mindist, maxdist, r=None, globaldef=None, particledef=None):
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
    dist = (r.random()*(maxdist-mindist)) + mindist
    angle = r.random()*twopi
    newx = graph.getVertexData(vertex, particledef['xposition']) + (cos(angle)*dist)
    newy = graph.getVertexData(vertex, particledef['yposition']) + (sin(angle)*dist)
    return (vertex, newx, newy)

def randomJostleParticle(graph, mindist, maxdist, minedgedist, maxedgedist, retries = 3, r=None, globaldef=None, particledef=None):
    if r is None:
        r = random.Random()
    if globaldef is None:
        globaldef = getBasicGlobalDef()
    if particledef is None:
        particledef = getBasicParticleDef()
    if graph.getOrder() < 2:
        return None
    vertices = [x for x in graph.getVertexList() if ((x != globaldef['id']) and (not graph.getVertexData(x, particledef['fixed'])) and ('important' not in graph.getVertexDataKeys(x)))]
    if len(vertices) < 1:
        return None
    r.shuffle(vertices)
    vertex = vertices[0]
    edges = graph.getAdjacentEdges(vertex)
    tries = 0
    while True:
        dist = (r.random()*(maxdist-mindist)) + mindist
        angle = r.random()*twopi
        newx = graph.getVertexData(vertex, particledef['xposition']) + (cos(angle)*dist)
        newy = graph.getVertexData(vertex, particledef['yposition']) + (sin(angle)*dist)
        done = False
        for edge in edges:
            #vertex1, vertex2, direction = graph.getEdgeInfo(edge)
            #print("   EDGE " + str(edge) + ": " + str(vertex1) + ", " + str(vertex2) + " dir: " + str(direction))
            
            othervertex = graph.getEdgeEnd(vertex, edge)
            dx = newx - graph.getVertexData(othervertex, particledef['xposition'])
            dy = newy - graph.getVertexData(othervertex, particledef['yposition'])
            tdist = sqrt(dx*dx + dy*dy)
            if tdist >= minedgedist and tdist <= maxedgedist:
                done = True
                break
        if done:
            break
        tries += 1
        if tries >= retries:
            return None
    #print(graph.getVertexData(vertex, particledef['xposition']), graph.getVertexData(othervertex, particledef['yposition']), " -> ", newx, newy)
    graph.setVertexData(vertex, particledef['xposition'], newx)
    graph.setVertexData(vertex, particledef['yposition'], newy)
    return
