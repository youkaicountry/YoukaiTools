from YoukaiTools import GameTools

an = GameTools.Animated()

an.addAnimation("test1", [0,1,2,3,4], [1,1,1,1,1], 1, "test2")
an.addAnimation("test2", ["a", "b", "c"], [1, 1, 1], 0, "test1")
an.setAnimation("test1")

for x in range(40):
   #an.update()
   print("ITERATION: " + str(x) + " SPRITE: " + str(an.update()))

