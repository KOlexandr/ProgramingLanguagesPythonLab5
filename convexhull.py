import pygame as pg
import geometry as gm
from sys import exit

surface = gm.initGraphics("Creating of convex hull")

# setPts = gm.SetPoints("input.txt")
# setPts.draw(surface,(255,255,255))
lst = gm.inputPoints(surface, (255, 255, 255))
setPts = gm.SetPoints(lst)

gm.grid(surface)
setPts.draw(surface, (255, 255, 255), 1)
pg.display.update()
surfaceOriginal = surface.copy()
gm.waiting()

if len(setPts) < 2:
    pg.quit()
    exit(0)

poly = gm.Polygon()
poly.insert(gm.Edge(setPts[0], setPts[1]))
poly.insert(gm.Edge(setPts[1], setPts[0]), 1)

surface.blit(surfaceOriginal, (0, 0))
poly.draw(surface, (255, 0, 0))
pg.display.update()
gm.waiting()

for i in range(2, len(setPts)):
    s = setPts[i]

    if not poly.isInside(s):
        idxLeft = gm.findTangent(poly, s, gm.Position.LEFT)
        idxRight = gm.findTangent(poly, s, gm.Position.RIGHT)

        key = len(poly) << 2
        poly2 = gm.Polygon()
        poly2.insert(gm.Edge(s, poly[idxLeft].org))
        if idxLeft > idxRight:
            idxRight += len(poly)
        for i in range(idxLeft, idxRight):
            poly2.insert(poly[i % len(poly)], key)
        poly2.insert(gm.Edge(poly[i % len(poly)].dst, s), key)

        poly = poly2

    surface.blit(surfaceOriginal, (0, 0))
    poly.draw(surface, (255, 0, 0))
    s.draw(surface, (0, 255, 0))
    pg.display.update()
    gm.waiting()

pg.quit()
