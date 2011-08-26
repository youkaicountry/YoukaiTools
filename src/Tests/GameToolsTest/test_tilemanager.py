from YoukaiTools import GameTools






tiles = [[1, 3, 5, 3, 2, 5, 6, 1],
         [1, 3, 5, 3, 2, 5, 6, 1],
         [1, 3, 5, 3, 2, 5, 6, 1],
         [1, 3, 5, 3, 2, 5, 6, 1],
         [1, 3, 5, 3, 2, 5, 6, 1],
         [1, 3, 5, 3, 2, 5, 6, 1],
         [1, 3, 5, 3, 2, 5, 6, 1],
         [1, 3, 5, 3, 2, 5, 6, 1]]

cam = GameTools.Camera2D((1.2, 2.3, 5.1, 6.3), (100, 100))

tm = GameTools.TileManager(cam, 8, 8, tiles)

print(tm.getShownTiles())
cam.zoom(2)
print(tm.getShownTiles())

ss = GameTools.SpriteSheet((8, 0, 0, 8), (8, 0, 0, 8), 20)
print(ss.getSprite(3))
print(ss.getSprite(9))
print(ss.getSprite(19))
print(ss.getSpriteFromCache(3))
print(ss.getSpriteFromCache(9))
print(ss.getSpriteFromCache(19))

