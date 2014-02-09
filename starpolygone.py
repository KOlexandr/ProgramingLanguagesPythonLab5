import pygame as pg
import geometry as gm
from sys import exit

surface = gm.initGraphics("Creating of starlike polygone")

# setPts = gm.SetPoints("input.txt")
# setPts.draw(surface,(255,255,255))
lst = gm.inputPoints(surface,(255,255,255))
setPts = gm.SetPoints(lst)
idx = setPts.minX()

surface.fill((0,0,0))
gm.grid(surface)
setPts.draw(surface,(255,255,255),1)
pg.display.update()
surfaceOriginal = surface.copy()
gm.waiting()

if (len(setPts) < 2):
	pg.quit()
	exit(0)

poly = gm.Polygon()
if (idx != 0):
	poly.insert(gm.Edge(setPts[idx],setPts[0]))
	poly.insert(gm.Edge(setPts[0],setPts[idx]),1)
	startIdx = 1
else:
	poly.insert(gm.Edge(setPts[0],setPts[1]))
	poly.insert(gm.Edge(setPts[1],setPts[0]),1)
	startIdx = 2

surface.blit(surfaceOriginal,(0,0))
poly.draw(surface,(255,0,0))
pg.display.update()
gm.waiting()

for i in range(startIdx,len(setPts)):
	if (i != idx):
		s = setPts[i]

		flag = True
		roS,phiS = gm.Point(s.x-poly[0].org.x,s.y-poly[0].org.y).toPolar()
		for j in range(0,len(poly)-1):
			roP,phiP = gm.Point(poly[j].dst.x-poly[0].org.x,poly[j].dst.y-poly[0].org.y).toPolar()
			if (phiS > phiP) or ((phiS == phiP) and (roS > roP)):
				removed = poly.remove(j)
				poly.insert(gm.Edge(removed.org,s),j)
				poly.insert(gm.Edge(s,removed.dst),j+1)
				flag = False
				break
		if flag:
			removed = poly.remove(len(poly))
			poly.insert(gm.Edge(removed.org,s),len(poly))
			poly.insert(gm.Edge(s,removed.dst),len(poly))

		surface.blit(surfaceOriginal,(0,0))
		poly.draw(surface,(255,0,0))
		s.draw(surface,(0,255,0))
		pg.display.update()
		gm.waiting()

pg.quit()
