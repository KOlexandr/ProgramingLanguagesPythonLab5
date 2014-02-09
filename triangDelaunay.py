import pygame as pg
import geometry as gm
from sys import exit

surface = gm.initGraphics("Triangulation Delaunay")

# setPts = gm.SetPoints("input.txt")
# setPts.draw(surface,(255,255,255))
lst = gm.inputPoints(surface,(255,255,255))
setPts = gm.SetPoints(lst)

ch = gm.convexHull(setPts)

gm.grid(surface)
setPts.draw(surface,(255,255,255),1)
ch.draw(surface,(255,0,0))
pg.display.update()
surfaceOriginal = surface.copy()
gm.waiting()

chain = gm.Polygon()
if len(ch) <= 2:
	pg.quit()
	exit(0)

chain.insert(gm.Edge(ch[0].org,ch[0].dst))
triangles = []
while len(chain) > 0:
	e = chain.remove(0)

	s = gm.conjugate(e,setPts)
	triangles.append(gm.Triangle(e.org,e.dst,s))

	e1 = gm.Edge(e.org,s)
	e2 = gm.Edge(s,e.dst)

	index = 0
	# if e1 didn't alive and wasn't in convex hull - it will be alive
	inChain = chain.findEdge(e1)
	if inChain >= 0:
		chain.remove(inChain)
	inCH = ch.findEdge(e1)
	if not ((inChain >= 0) or (inCH >= 0)):
		chain.insert(e1)
		index = 1
	# if e2 didn't alive and wasn't in convex hull - it will be alive
	inChain = chain.findEdge(e2)
	if inChain >= 0:
		chain.remove(inChain)
	inCH = ch.findEdge(e2)
	if not ((inChain >= 0) or (inCH >= 0)):
		chain.insert(e2,index)

	surface.blit(surfaceOriginal,(0,0))
	ch.draw(surface,(255,0,0))
	for t in triangles:
		t.draw(surface,(0,0,255))
	chain.draw(surface,(0,255,0))
	pg.display.update()
	gm.waiting()

pg.quit()
