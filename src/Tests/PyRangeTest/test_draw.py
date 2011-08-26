from YoukaiTools import PyRange
from YoukaiTools.PyRange.Draw import Draw1D
dg = PyRange.DataGraph1D()

#irregular
#dg.setFromPoints([ (0.0, .8), (1.2, .4), (3.0, .3), (5.2, .45), (6.0, .1), (7.22, .5), (7.6, .7), (8.0, .9) ])

#regular
dg.setFromPoints([ (1.0, 3.3), (2.0, 1.2), (3.0, 1.8), (4.0, 1.1), (5.0, 3.6), (6.0, .08), (7.0, 2.3), (8.0, 1.6) ])

s = Draw1D.makeDefaultSettings()
s["interpolation"] = PyRange.Interpolation.hermite
s["tension"] = 0
s["bias"] = 0
s["maxcolor"] = (1.0, 0.0, 0.0)
s["mincolor"] = (1.0, 0.0, 0.0)
s["markpoints"] = True
Draw1D.saveDataGraph1DFile("dg1d.png", dg, settings=s)
