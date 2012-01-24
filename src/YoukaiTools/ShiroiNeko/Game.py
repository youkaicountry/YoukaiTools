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

from YoukaiTools.AdvMath.Statistics import mean

def settleStructure2D(sn2d, ke_decrease_period=5.0, degenerate_time_per_particle=3.0, degenerate_time_per_bond=1.0, grace_per_particle=.5, grace_per_bond=.1, ke_threshold_per_particle=.1, break_degenerate=True):
    ke_dec = 0.0
    bonds = sn2d.numbonds
    grace_time = (sn2d.numparticles*grace_per_particle) + (sn2d.numbonds*grace_per_bond)
    ke_thresh = sn2d.numparticles*ke_threshold_per_particle
    eff_degenerate_time = (sn2d.numparticles*degenerate_time_per_particle) + (sn2d.numbonds*degenerate_time_per_bond)
    
    #Grace time
    for i in xrange(int(grace_time/sn2d.dt)):
        sn2d.update()
        if break_degenerate:
            if sn2d.numbonds < bonds:
                return False

    #Ensure steadily decreasing KE
    ke = sn2d.getKineticEnergy()
    for i in xrange(int(eff_degenerate_time/sn2d.dt)):
        sn2d.update()
        if break_degenerate:
            if sn2d.numbonds < bonds:
                return False
        new_ke = sn2d.getKineticEnergy()
        if new_ke <= ke:
            ke_dec += sn2d.dt
            if ke_dec >= ke_decrease_period:
                if new_ke <= ke_thresh:
                    return True
        else:
            ke_dec = 0.0
    return False

def scoreHeight(sn2d, points_per_height=1):
    height = -min(sn2d.yposition[p] for p in sn2d.particlelist)
    #print(height)
    score = height*points_per_height
    return score

def clipBelow(sn2d, below = 0):
    for p in sn2d.particlelist:
        if sn2d.yposition[p] > below:
            return False
    return True

def scoreSumHeight(sn2d, points_per_height=1):
    height = -sum(sn2d.yposition[p] for p in sn2d.particlelist)
    #print(height)
    score = height*points_per_height
    return score

def scoreAverageHeight(sn2d, points_per_height = 1):
    avg_height = -mean([sn2d.yposition[p] for p in sn2d.particlelist])
    score = avg_height*points_per_height
    return score

def scoreWeightHeight(sn2d, points_per_height=30000, points_per_average_height=10000, points_per_sum_height=5, points_per_force=.000001, force_inc=1000):
    bonds = sn2d.numbonds
    if bonds < 1:
        return 0
    #upph = points_per_height * sn2d.dt
    #uppf = (points_per_force*force_inc) * sn2d.dt
    uforceinc = force_inc * sn2d.dt
    
    adder = 0
    force = 0
    adder += scoreHeight(sn2d, points_per_height/2.0)
    adder += scoreAverageHeight(sn2d, points_per_average_height/2.0)
    adder += scoreSumHeight(sn2d, points_per_sum_height/2.0)
    while bonds == sn2d.numbonds:
        
        force += uforceinc
        for pid in sn2d.particlelist:
            sn2d.applyForce(pid, 0, force)
        #adder += uppf
        sn2d.update()
    adder += scoreHeight(sn2d, points_per_height/2.0)
    adder += scoreAverageHeight(sn2d, points_per_average_height/2.0)
    adder += scoreSumHeight(sn2d, points_per_sum_height/2.0)
    adder += force*points_per_force
    return adder

def scoreWeight(sn2d, points_per_force=1, force_inc=30, vertices=None):
    bonds = sn2d.numbonds
    if bonds < 1:
        return 0
    #upph = points_per_height * sn2d.dt
    #uppf = (points_per_force*force_inc) * sn2d.dt
    uforceinc = force_inc * sn2d.dt
    
    if vertices is None:
        vertices = sn2d.particlelist
    
    adder = 0
    force = 0
    while bonds == sn2d.numbonds:
        force += uforceinc
        for pid in vertices:
            sn2d.applyForce(pid, 0, force)
        #adder += uppf
        sn2d.update()
    adder += force*points_per_force
    return adder
