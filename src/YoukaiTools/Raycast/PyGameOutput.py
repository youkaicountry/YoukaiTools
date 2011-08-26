import pygame

class PyGameOutput:
    def __init__(self, size):
        self.tiles = {}
        self.size = size
        self.temptile = {}
        self.tempsurf = []
        self.tcache = {}
        self.tempsurf.append(None)
        for i in range(1, size[1]+1):
           self.tempsurf.append(pygame.Surface((1, i)))
        return
    
    def addTile(self, filename, idnum):
        self.tiles[idnum] = pygame.image.load(filename)
        self.temptile[idnum] = pygame.Surface((1, self.tiles[idnum].get_height()))
        return
    
    def drawScreen(self, screen, rayresult):
        for x in range(self.size[0]):
            r = rayresult[x]
            if r[0] == None: continue
            if r[0] > self.size[1]:
                frac = self.size[1] / r[0]
                h = self.size[1]
                s = self.tiles[r[3]]
                theight = s.get_height()
                th = frac * theight
                tstrt = int((theight / 2) - .5*th)
                tend = int((theight / 2) + .5*th)+1
                #if tend - tstrt <= 2: tstrt - 2; tend + 2;
                th = tend-tstrt
                ts = self.tempsurf[self.size[1]]
                
                #tt = pygame.Surface((1, th))
                #tt.blit(s, (0, 0), pygame.Rect(r[2]*s.get_width(), tstrt, 1, th))
                #print(tstrt, tend, th)
                #pygame.transform.scale(tt, (1, h), ts)
                
                
                if th not in self.tcache:
                    self.tcache[th] = pygame.Surface((1, th))
                self.tcache[th].blit(s, (0, 0), pygame.Rect(r[2]*s.get_width(), tstrt, 1, th))
                #print(h, ts.get_width())
                pygame.transform.scale(self.tcache[th], (1, h), ts)
                screen.blit(ts, (x, 0))
            else:
                h = r[1][1] - r[1][0]
                s = self.tiles[r[3]]
                ts = self.tempsurf[h]
                self.temptile[r[3]].blit(s, (0, 0), pygame.Rect(r[2]*s.get_width(), 0, 1, s.get_height()))
                pygame.transform.scale(self.temptile[r[3]], (1, h), ts)
                screen.blit(ts, (x, r[1][0]))
        return