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

import math

class SN2D:
   def __init__(self):
      #globals
      self.dt = 1.0
      self.macrogravity = 9.81
      self.time = 0
      
      #settings
      self.collisionson = False
      self.macrogravityon = True
      self.fluidfriction = 1.0
      self.coulombon = False
      self.coulomb_constant = 1.0

      #particle definition
      self.particlelist = set()  #set of all particle IDs
      self.numparticles = 0      #the number of allocated particles
      self.particletop = 0       #the next unused ID
      self.xposition = {}        #the x position of the particle
      self.yposition = {}        #the y position of the particle
      self.xvelocity = {}        #the x velocity of the particle
      self.yvelocity = {}        #the y velocity of the particle
      self.xacceleration = {}    #the x acceleration of the particle
      self.yacceleration = {}    #the y acceleration of the particle
      self.mass = {}             #the mass of the particle
      self.fixed = {}
      self.charge = {}


      #bond definition
      self.bondlist = set()
      self.numbonds = 0
      self.bondtop = 0
      self.p1 = {}
      self.p2 = {}
      self.spring = {}
      self.length = {}

   def newParticle(self, names=None, num=1):
       if names is None:
           names = []
           for i in range(num):
               names.append(self.particletop)
               self.particletop+=1
       else:
           self.particletop+=1
       out = []
       for x in names:
           self.particlelist.add(x)
           self.numparticles += 1
           self.xposition[x] = 0
           self.yposition[x] = 0
           self.xvelocity[x] = 0
           self.yvelocity[x] = 0
           self.xacceleration[x] = 0
           self.yacceleration[x] = 0
           self.fixed[x] = False
           self.mass[x] = 1
           self.charge[x] = 0
           out.append(x)
       return out

   def removeParticle(self, name):
      self.particlelist.remove(name)
      self.numparticles -= 1
      del self.xposition[name]
      del self.yposition[name]
      del self.xposition[name]
      del self.yposition[name]
      del self.xvelocity[name]
      del self.yvelocity[name]
      del self.xacceleration[name]
      del self.yacceleration[name]
      del self.mass[name]
      del self.fixed[name]
      del self.charge[name]
      return
   
   def newBond(self, p1, p2, name=None, calclength=True):
       if name is None:
           name = self.bondtop
           self.bondtop+=1
       self.bondlist.add(name)
       self.numbonds += 1
       self.p1[name] = p1
       self.p2[name] = p2
       self.spring[name] = 0
       self.length[name] = 0
       if calclength:
           dx = self.xposition[p1] - self.xposition[p2]
           dy = self.yposition[p1] - self.yposition[p2]
           self.length[name] = math.sqrt(dx*dx + dy*dy)
       return name

   def removeBond(self, name):
      self.bondlist.remove(name)
      self.numbonds -= 1
      del self.p1[name]
      del self.p2[name]
      del self.spring[name]
      del self.length[name]
      return
      
   def applyForce(self, pid, forcex, forcey):
      self.xacceleration[pid] += forcex/self.mass[pid]
      self.yacceleration[pid] += forcey/self.mass[pid]
      return
      
   def applyAcceleration(self, pid, xaccel, yaccel):
      self.xacceleration[pid] = xaccel
      self.yacceleration[pid] = yaccel
      return
   
   def getKineticEnergy(self, particles=None):
       if particles is None:
           particles = self.particlelist
       ke = 0
       for p in particles:
           vx = self.xvelocity[p]
           vy = self.yvelocity[p]
           v = math.sqrt(vx*vx + vy*vy)
           v2 = v*v
           ke += self.mass[p] * v2
       return ke


   def update(self):
      self.time += self.dt
      
      #macrogravity
      if self.macrogravityon:
         for pid in self.particlelist:
            self.yacceleration[pid] += self.macrogravity
            
      #bonds
      for bid in self.bondlist:
          p1 = self.p1[bid]
          p2 = self.p2[bid]
          dx = self.xposition[p1] - self.xposition[p2]
          dy = self.yposition[p1] - self.yposition[p2]
          l = math.sqrt(dx*dx + dy*dy)
          diff = self.length[bid] - l
          nl = -(diff / l) * self.spring[bid]
          tempa = dx*nl
          tempb = dy*nl
          self.applyForce(p2, tempa, tempb)
          self.applyForce(p1, -tempa, -tempb)
      
      #coulomb
      if self.coulombon:
          for pid in self.particlelist:
              for pid2 in self.particlelist:
                  if pid == pid2: continue
                  dx = self.xposition[pid] - self.xposition[pid2]
                  dy = self.yposition[pid] - self.yposition[pid2]
                  dist = math.sqrt(dx*dx + dy*dy)
                  if dist == 0: continue
                  nx = (self.xposition[pid] - self.xposition[pid2]) / dist
                  ny = (self.yposition[pid] - self.yposition[pid2]) / dist
                  dist_sq = dist*dist
                  charge_mult = self.charge[pid] * self.charge[pid2]
                  f = self.coulomb_constant*(charge_mult/dist_sq)
                  fx = f*nx
                  fy = f*ny
                  self.applyForce(pid, fx, fy)
                  self.applyForce(pid2, -fx, -fy)
                  #xforce[ii] += coulomb_constant*((charge[ii]*charge[jj])/(cc*cc))*nx;
                  #   yforce[ii] += coulombconstant*((charge[ii]*charge[jj])/(cc*cc))*ny;
                  #   xforce[jj] -= coulombconstant*((charge[ii]*charge[jj])/(cc*cc))*nx;
                  #   yforce[jj] -= coulombconstant*((charge[ii]*charge[jj])/(cc*cc))*ny;
      
      #collisions

      #integrator
      for pid in self.particlelist:
         if not self.fixed[pid]: 
             self.xvelocity[pid] += self.xacceleration[pid]*self.dt
             self.yvelocity[pid] += self.yacceleration[pid]*self.dt
             self.xposition[pid] += self.xvelocity[pid]*self.dt
             self.yposition[pid] += self.yvelocity[pid]*self.dt

         #clear acceleration
         self.xacceleration[pid] = 0
         self.yacceleration[pid] = 0
         
         #fluid friction
         self.xvelocity[pid] *= self.fluidfriction
         self.yvelocity[pid] *= self.fluidfriction

      return