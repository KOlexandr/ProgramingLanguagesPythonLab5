import pygame as pg
import geometry as gm
from sys import exit

surface = gm.initGraphics("Triangulation of monotone polygone")

# setPts = gm.SetPoints("input.txt")
# setPts.draw(surface,(255,255,255))
lst = gm.inputPoints(surface,(255,255,255))
setPts = gm.SetPoints(lst)
setPts.rearrange(lambda p1,p2: p1.x>p2.x)

mn = gm.monotone(setPts)

gm.grid(surface)
setPts.draw(surface,(255,255,255),1)
mn.draw(surface,(255,0,0))
pg.display.update()
surfaceOriginal = surface.copy()
gm.waiting()

triangles = []
stack = []
if len(mn) > 1:
	stack.append(setPts[0])
	stack.append(setPts[1])

	for i in range(2,len(setPts)):
		s = setPts[i]

		if (mn.haveEdge(gm.Edge(s,stack[0])) and not mn.haveEdge(gm.Edge(s,stack[len(stack)-1]))):
			while (len(stack)>1):
				triangles.append(gm.Triangle(s,stack[0],stack[1]))
				stack.pop(0)
			stack.append(s)
		elif (not mn.haveEdge(gm.Edge(s,stack[0])) and mn.haveEdge(gm.Edge(s,stack[len(stack)-1]))):
			if gm.whichChain(s,mn) == gm.ChainType.UPPER:
				side = gm.Position.RIGHT
			else:
				side = gm.Position.LEFT
			while (len(stack)>1) and (gm.Edge(stack[len(stack)-2],stack[len(stack)-1]).classify(s) == side):
				triangles.append(gm.Triangle(s,stack[len(stack)-2],stack[len(stack)-1]))
				stack.pop()
			stack.append(s)
		else:
			while (len(stack)>1):
				triangles.append(gm.Triangle(s,stack[0],stack[1]))
				stack.pop(0)
			stack = []

		surface.blit(surfaceOriginal,(0,0))
		for t in triangles:
			t.draw(surface,(0,0,255))
		s.draw(surface,(0,255,0))
		pg.display.update()
		gm.waiting()

pg.quit()
