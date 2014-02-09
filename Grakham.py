import pygame as pg
import geometry as gm
from sys import exit

surface = gm.initGraphics("Convex hull by Grakham")
pg.mixer.music.load("track.ogg")

# setPts = gm.SetPoints("input.txt")
# setPts.draw(surface,(255,255,255))
lst = gm.inputPoints(surface,(255,255,255))
setPts = gm.SetPoints(lst)
setPts.rearrange(lambda p1,p2: p1.x > p2.x)

surface.fill((0,0,0))
gm.grid(surface)
setPts.draw(surface,(255,255,255),1)
pg.display.update()
gm.waiting()

setPts.sortByPolar()

surface.fill((0,0,0))
gm.grid(surface)
setPts.draw(surface,(255,255,255),1)
pg.display.update()
surfaceOriginal = surface.copy()
gm.waiting()

ch = gm.Polygon()

if len(setPts) < 2:
	pg.quit()
	exit(0)
elif len(setPts) == 2:
	ch.insert(Edge(setPts[0],setPts[1]))
	ch.insert(Edge(setPts[1],setPts[0]))
else:
	setPts.add(setPts[0])
	stack = [gm.Edge(setPts[0],setPts[1])]
	for i in range(2,len(setPts)):
		p = setPts[i]

		while (stack[len(stack)-1].classify(p) != gm.Position.RIGHT):
			stack.pop()

		stack.append(gm.Edge(stack[len(stack)-1].dst,p))

		surface.blit(surfaceOriginal,(0,0))
		for s in stack:
			s.draw(surface,(255,0,0))
		p.draw(surface,(0,255,0))
		pg.display.update()
		gm.waiting()

	key = len(stack)
	for s in stack:
		ch.insert(s,key)

	surface.blit(surfaceOriginal,(0,0))
	ch.draw(surface,(255,0,0))
	pg.display.update()
	gm.waiting()

pg.quit()
