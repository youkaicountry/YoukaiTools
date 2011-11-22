import YoukaiTools.ShiroiNeko as ShiroiNeko

sn2d = ShiroiNeko.SN2D()
sn2d.newParticle(["one", "two", "three", "four"])
sn2d.xposition["one"] = 0
sn2d.yposition["one"] = 0
sn2d.xposition["two"] = 10
sn2d.yposition["two"] = 0
sn2d.xposition["three"] = 0
sn2d.yposition["three"] = 20
sn2d.xposition["four"] = 10
sn2d.yposition["four"] = 20
sn2d.fixed["one"] = True
sn2d.newBond("one", "two", "b1")
sn2d.spring["b1"] = 100
sn2d.dt = .1
sn2d.fluidfriction = .99
sn2d.coulomb = True
sn2d.charge["three"] = 1
sn2d.charge["four"] = 1

print("BEFORE:")
for i in sn2d.particlelist:
    print "ID:"+str(i)+" X:"+str(sn2d.xposition[i])+" Y:"+str(sn2d.yposition[i])
for t in xrange(1000000):
   sn2d.update()
print("AFTER:")
for i in sn2d.particlelist:
    print "ID:"+str(i)+" X:"+str(sn2d.xposition[i])+" Y:"+str(sn2d.yposition[i])
   #if t%10 == 0:
   #    print "TIME:"+str(sn2d.time)
   #    for i in sn2d.particlelist:
   #       print "ID:"+str(i)+" X:"+str(sn2d.xposition[i])+" Y:"+str(sn2d.yposition[i])
