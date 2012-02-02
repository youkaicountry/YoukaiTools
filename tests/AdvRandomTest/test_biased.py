import YoukaiTools.AdvRandom as AdvRandom

bc = AdvRandom.BiasedChoice([1,2,3,4])

for i in xrange(1000):
    print(bc.getChoice())
