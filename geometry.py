from math import sqrt
from sys import float_info
import pygame as pg

maxx = 500
maxy = 500
playing = False

# upper or lower chain in monotone polygon
class ChainType:
    UPPER = 1
    LOWER = -1
    NONE = 0

# order of vertex's visiting
class Order:
    CW = 1                # clockwise
    CCW = -1            # counter-clockwise

# position of one point by another points
class Position:
    LEFT = 1
    RIGHT = 2
    AHEAD = 4
    BEHIND = 8
    BETWEEN = 16
    START = 32
    END = 64

    # convert position into the string
    # input: pos - integer with position mean
    # output: string with answer
    @staticmethod
    def say(pos):
        ans = {1: 'LEFT',
               2: 'RIGHT',
               4: 'AHEAD',
               8: 'BEHIND',
               16: 'BETWEEN',
               32: 'START',
               64: 'END'
        }
        return ans[pos]

# one point
class Point:
    # members:
    #   x,y - coordinates

    # constructor
    # input: x,y - coordinates of point
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # convert to string
    # output: string "(x,y)"
    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

    # compare current point with another
    # input: point p
    # output: boolean value
    def __eq__(self, p):
        return (self.x == p.x) and (self.y == p.y)

    # subtraction second point from current
    # input: point p
    # output: point
    def __sub__(self, p):
        return Point(self.x - p.x, self.y - p.y)

    # Euclidian distance to another point
    # input: p - point
    # output: distance, float
    def distanceTo(self, p):
        return sqrt((self.x - p.x) ** 2 + (self.y - p.y) ** 2)

    # get like-polar coordinates
    # output: ro,phi (BEWARE!!! ro without sqrt, phi is a tangent)
    def toPolar(self):
        ro = float(self.x) * self.x + self.y * self.y
        if self.x == 0.0:
            if self.y > 0.0:
                phi = sys.float_info.max
            elif self.y < 0.0:
                phi = -sys.float_info.max
            else:
                phi = 0.0
        else:
            phi = float(self.y) / self.x
        return (ro, phi)

    # draw point with color and label (text)
    # input: surface
    #        color
    #        text
    def draw(self, surface, color, text=""):
        pg.draw.circle(surface, color, (self.x, maxy - self.y), 3)
        if text != "":
            myfont = pg.font.SysFont("Courier New", 12)
            label = myfont.render(text, 1, color)
            surface.blit(label, (self.x + 4, maxy - self.y + 4))

# set of points
class SetPoints:
    # members:
    #   points - array of points
    #   count - number of points

    # constructor
    # input: fileName - name of txt-file
    # BEWARE!!! each string must be in format "int int"
    def __init__(self, arg):
        if type(arg) == str:
            f = open(arg, "r")
            lines = f.readlines()
            f.close()
            self.points = []
            for line in lines:
                coords = map(int, line.split(' '))
                self.points.append(Point(coords[0], coords[1]))
            self.count = len(self.points)
        elif type(arg) == list:
            self.points = []
            for p in arg:
                self.points.append(p)
            self.count = len(self.points)
        else:
            self.points = []
            self.count = 0

    # convert to string (print all point's coordinates)
    # output: string "(x1,y1) (x2,y2) "
    def __str__(self):
        s = ""
        for p in self.points:
            s = s + str(p) + " "
        return s

    # return power of set (number of points)
    # output: integer number - count
    def __len__(self):
        return self.count

    # add point to set
    # input: p - point to be added
    def add(self, p):
        self.points.append(p)
        self.count += 1

    # get i-th point
    # input: i - index of point
    # output: point, if i correct, or None
    def __getitem__(self, i):
        if (i >= 0) and (i < self.count):
            return self.points[i]
        else:
            return None

    # sort points in order by rule
    # input: f - lambda-expression or function
    def rearrange(self, f):
        if (self.count == 0):
            return
        lst = []
        lst.append(self.points[0])
        for i in range(1, self.count):
            p = self.points[i]
            j = 0
            while (j < len(lst)) and (f(p, lst[j])):
                j += 1
            lst.insert(j, p)
        self.points = lst

    # sort points in ascending by polar of vector (p_0,p_i)
    def sortByPolar(self):
        p = self.points[0]
        for j in range(2, self.count):
            ro1, phi1 = (self.points[j] - p).toPolar()
            for i in range(1, j):
                ro2, phi2 = (self.points[i] - p).toPolar()
                if (phi1 > phi2) or ((phi1 == phi2) and (ro1 > ro2)):
                    self.points.insert(i, self.points.pop(j))
                    break;

    # find point with minimal x-coordinate
    # output: index of point
    def minX(self):
        minIdx = 0
        minX = self.points[minIdx].x
        for i in range(1, self.count):
            if self.points[i].x < minX:
                minX = self.points[i].x
                minIdx = i
        return minIdx

    # draw points in set
    # input: surface - drawing context
    #        color
    #        labels (if not 0 - draw point numbers)
    def draw(self, surface, color, labels=0):
        if labels == 0:
            for p in self.points:
                p.draw(surface, color)
        else:
            for i in range(0, self.count):
                self.points[i].draw(surface, color, str(i + 1))

# edges
class Edge:
    # members:
    #    org - begin of edge (point)
    #    dst - end of edge (point)

    # constructor
    def __init__(self, p1, p2):
        self.org = p1
        self.dst = p2

    # convert into string
    # output: string "(x1,y1)->(x2,y2)"
    def __str__(self):
        return str(self.org) + "->" + str(self.dst)

    # comparing current edge with another
    # output: boolean value (BEWARE!!! direction must be the same)
    def __eq__(self, e):
        return (self.org == e.org) and (self.dst == e.dst)

    # soft comparing (without direction)
    # output: boolean value
    def __ge__(self, e):
        ans1 = (self.org == e.org) and (self.dst == e.dst)
        ans2 = (self.org == e.dst) and (self.dst == e.org)
        return ans1 or ans2

    # check position of point p by (org,dst)
    # input: p
    # output: integer number - position
    def classify(self, p):
        v1 = Point(self.dst.x - self.org.x, self.dst.y - self.org.y)
        v2 = Point(p.x - self.org.x, p.y - self.org.y)
        r = v1.x * v2.y - v2.x * v1.y
        if r > 0:
            return Position.LEFT
        elif r < 0:
            return Position.RIGHT
        else:
            if (v1.x * v2.x < 0) and (v1.y * v2.y < 0):
                return Position.BEHIND
            elif v2.x ** 2 + v2.y ** 2 > v1.x ** 2 + v1.y ** 2:
                return Position.AHEAD
            elif (self.org.x == p.x) and (self.org.y == p.y):
                return Position.START
            elif (self.dst.x == p.x) and (self.dst.y == p.y):
                return Position.END
            else:
                return Position.BETWEEN

    # rotate by pi/2 clockwise
    def rotate(self):
        AB = Point(self.dst.x - self.org.x, self.dst.y - self.org.y)
        nAB = Point(AB.y, -AB.x)
        self.org = Point(0.5 * (self.org.x + self.dst.x - nAB.x), 0.5 * (self.org.y + self.dst.y - nAB.y))
        self.dst = Point(0.5 * (self.org.x + self.dst.x + nAB.x), 0.5 * (self.org.y + self.dst.y + nAB.y))

    # find parameter t by intersection current edge by e
    # input: e - edge
    # output: t - float number from P(t)=A+t(B-A)
    def intersect(self, e):
        v = Point(e.dst.x - e.org.x, e.dst.y - e.org.y)
        n = Point(-v.y, v.x)
        ca = Point(e.org.x - self.org.x, e.org.y - self.org.y)
        ba = Point(self.dst.x - self.org.x, self.dst.y - self.org.y)
        return (n.x * ca.x + n.y * ca.y) / float(n.x * ba.x + n.y * ba.y)

    # return point's coordinates by parameter
    # input: t - parameter
    # output: point P(t)=A+t(B-A)
    def pointByT(self, t):
        return Point(org.x + t * (dst.x - org.x), org.y + t * (dst.y - org.y))

    # draw edge (line)
    # input: surface - drawing context
    #        color
    def draw(self, surface, color):
        pg.draw.line(surface, color, (self.org.x, maxy - self.org.y), (self.dst.x, maxy - self.dst.y), 1)

# triangle
class Triangle:
    # members:
    #   vertexes - array of points

    # constructor
    def __init__(self, p1, p2, p3):
        self.vertexes = []
        self.vertexes.append(p1)
        self.vertexes.append(p2)
        self.vertexes.append(p3)

    # draw triangle
    # input: surface - drawing context
    #        color
    def draw(self, surface, color):
        for i in range(0, 3):
            self.vertexes[i].draw(surface, color)
            pg.draw.line(surface, color, (self.vertexes[i].x, maxy - self.vertexes[i].y), \
                         (self.vertexes[(i + 1) % 3].x, maxy - self.vertexes[(i + 1) % 3].y), 1)

# polygon - array of edges ordered by clockwise
class Polygon:
    # members:
    #   edges - array of edges in order of visit by clockwise
    #   len - number of edges
    #   win - index of current edge (window)

    # constructor
    def __init__(self):
        self.edges = []
        self.len = 0
        self.win = -1

    # convert polygon to string
    # output: string like "(x1,y1)-(x2,y2) > (x3,y3)-(x4,y4) > ..."
    def __str__(self):
        s = ""
        for v in self.edges:
            s = s + str(v.org) + "-" + str(v.dst) + " > "
        return s

    # count of edges
    # output: number
    def __len__(self):
        return self.len

    # insert edge with index key
    # if key <= 0 - insert from begin (prepend), if key >= length - insert at the end (append)
    # function changes window
    # input: e - edge needs to insert
    #        key
    def insert(self, e, key=0):
        if key < 0:
            self.win = 0
        elif key >= self.len:
            self.win = self.len
        else:
            self.win = key
        self.len += 1
        self.edges.insert(self.win, e)

    # remove edge with index key
    # if key <= 0 - remove first edge, if key >= length - remove last edge
    # output: removed edge or None (if has no edges)
    def remove(self, key):
        if self.len == 0:
            return None
        if key < 0:
            self.win = 0
        elif key >= self.len:
            self.win = self.len - 1
        else:
            self.win = key
        e = self.edges.pop(self.win)
        self.len -= 1
        if self.len == 0:
            self.win = -1
        if self.win == self.len:
            self.win -= 1
        return e

    # get current window
    # output: index of current window
    def getWin(self):
        return self.win

    # set current window
    # input: index of new window (if index incorrect - does nothing)
    def setWin(self, i):
        if (i >= 0) and (i < self.len):
            self.win = i

    # get edge from current window
    # output: edge
    def __getitem__(self, key):
        w = key
        if w == -1:
            w = self.win
        if w != -1:
            return self.edges[w]
        else:
            return None

    # move window to next edge in order
    # input: order
    # output: next edge
    def next(self, order):
        if order == Order.CW:
            self.win += 1
            if self.win >= self.len:
                self.win = 0
        else:
            self.win -= 1
            if self.win < 0:
                self.win = self.len - 1
        return self.edges[self.win]

    # check if point is inside the polygon
    # input: p - point to check
    # output: boolean value
    def isInside(self, p):
        pos = Position.RIGHT | Position.BETWEEN | Position.START | Position.END
        for e in self.edges:
            if (e.classify(p) & pos) == 0:
                return False
        return True

    # draw polygon
    # input: surface - drawing context
    #        color
    def draw(self, surface, color):
        for e in self.edges:
            e.org.draw(surface, color)
            e.dst.draw(surface, color)
            e.draw(surface, color)

    # copy of elements from other polygon
    # input: p - polygon
    def copy(self, p):
        self.edges = []
        for e in p.edges:
            self.edges.append(Edge(e.org, e.dst))
        self.win = 0
        self.len = len(self.edges)

    # check if edge is on the polygone's border
    # input: e - edge
    # output: boolean value
    def haveEdge(self, e):
        if (self.len == 0):
            return False
        for es in self.edges:
            if es >= e:
                return True
        return False

    # find edge in polygone's border
    # input: e - edge
    # output: index (-1 if has not edge)
    def findEdge(self, e):
        if (self.len == 0):
            return -1
        for i in range(0, self.len):
            if e >= self.edges[i]:
                return i
        return -1

    # check if point is on the polygone's border
    # input: e - edge
    # output: boolean value
    def havePoint(self, p):
        if (self.len == 0):
            return False
        for e in self.edges:
            if (e.org == p) or (e.dst == p):
                return True
        return False

# find tangent from side SIDE
# input: poly - polygon
#        p    - point
#        pos - side of tangent line
# output: index of tangent
def findTangent(poly, p, pos):
    ln = len(poly)
    if ln == 0:
        return None
    if pos == Position.LEFT:
        order = Order.CW
        side = Position.RIGHT
    else:
        order = Order.CCW
        side = Position.LEFT
    if Edge(p, poly[0].org).classify(poly[1].org) == side:
        i = -1
        while Edge(p, poly[i % ln].org).classify(poly[(i + 1) % ln].org) == side:
            i -= 1
        return (i + 1) % ln
    else:
        i = 1
        while Edge(p, poly[i % ln].org).classify(poly[(i + 1) % ln].org) != side:
            i += 1
        return i % ln

# initialisation of graphics
# input: title - window title
# output: surface (graphics context)
def initGraphics(title):
    pg.init()
    bits = 32
    surface = pg.display.set_mode((maxx, maxy), 0, bits)
    surface.fill((0, 0, 0))
    grid(surface)
    pg.event.clear()
    pg.event.set_allowed(pg.KEYUP | pg.MOUSEBUTTONUP)
    pg.display.set_caption(title)
    pg.display.update()
    return surface

# draw grid
# input: surface
def grid(surface):
    for i in range(100, maxx, 100):
        pg.draw.line(surface, (50, 50, 50), (i, 0), (i, maxy))
    for i in range(100, maxy, 100):
        pg.draw.line(surface, (50, 50, 50), (0, i), (maxx, i))

# input points by mouse
# input: surface, color
# output: list of points
def inputPoints(surface, color):
    pg.event.clear()
    ps = []
    while True:
        event = pg.event.wait()
        if (event.type == pg.MOUSEBUTTONUP):
            p = Point(event.pos[0], maxy - event.pos[1])
            ps.append(p)
            p.draw(surface, color)
            pg.display.update()
        elif (event.type == pg.KEYUP) and (event.scancode == 57) and (event.key == 32):
            return ps
        elif (event.type == pg.KEYUP) and (event.scancode == 1) and (event.key == 27):
            pg.quit()
            exit(0)

# waiting and input processing
def waiting():
    global playing
    while True:
        event = pg.event.wait()
        # if space
        if (event.type == pg.KEYUP) and (event.scancode == 57) and (event.key == 32):
            return
        # if escape
        elif (event.type == pg.KEYUP) and (event.scancode == 1) and (event.key == 27):
            pg.quit()
            exit(0)
        # if "m"
        elif (event.type == pg.KEYUP) and (event.scancode == 50) and (event.key == 109):
            if not playing:
                pg.mixer.music.play()
                playing = True
            else:
                pg.mixer.music.stop()
                playing = False
        # if "="
        elif (event.type == pg.KEYUP) and (event.scancode == 13) and (event.key == 61):
            if playing:
                vol = pg.mixer.music.get_volume() + 0.05
                if (vol > 1.0):
                    vol = 1.0
                pg.mixer.music.set_volume(vol)
        # if "-"
        elif (event.type == pg.KEYUP) and (event.scancode == 12) and (event.key == 45):
            if playing:
                vol = pg.mixer.music.get_volume() - 0.05
                if (vol < 0.0):
                    vol = 0.0
                pg.mixer.music.set_volume(vol)

# create monotone polygon
# input: st - set of points
# output: mn - monotone polygon
def monotone(st):
    mn = Polygon()
    st2 = st
    st2.rearrange(lambda p1, p2: p1.x > p2.x)
    if (len(st2) <= 1):
        return mn

    left = st2[0]
    right = st2[len(st2) - 1]
    if (len(st2) == 2):
        mn.insert(Edge(left, right))
        mn.insert(Edge(right, left))
        return mn

    upper = [left]
    lower = []
    for i in range(1, len(st2) - 1):
        s = st2[i]
        if Edge(left, right).classify(s) == Position.LEFT:
            upper.append(s)
        else:
            lower.insert(0, s)
    upper.append(right)
    upper.extend(lower)
    upper.append(left)
    key = len(upper) << 1
    for i in range(0, len(upper) - 1):
        mn.insert(Edge(upper[i], upper[i + 1]), key)
    return mn

# return chain type for concrete point in monotone polygone
# input: p - point
#        mn - monotone polygone
# output: type of chain (if len of polygon = 0 or point is not in polygone -> return NONE)
def whichChain(p, mn):
    if (len(mn) == 0):
        return ChainType.NONE
    ans = ChainType.UPPER
    x = mn[0].org.x
    for i in range(1, len(mn)):
        if x > mn[i].org.x:
            ans = ChainType.LOWER
        x = mn[i].org.x
        if p == mn[i].org:
            return ans
    return ChainType.NONE

# create convex hull
# input: st - set of points
# output: ch - convex hull
def convexHull(st):
    ch = Polygon()

    if (len(st) < 2):
        return ch

    ch.insert(Edge(st[0], st[1]))
    ch.insert(Edge(st[1], st[0]), 1)

    for i in range(2, len(st)):
        s = st[i]

        if not ch.isInside(s):
            idxLeft = findTangent(ch, s, Position.LEFT)
            idxRight = findTangent(ch, s, Position.RIGHT)

            key = len(ch) << 1
            ch2 = Polygon()
            ch2.insert(Edge(s, ch[idxLeft].org))
            if idxLeft > idxRight:
                idxRight += len(ch)
            for i in range(idxLeft, idxRight):
                ch2.insert(ch[i % len(ch)], key)
            ch2.insert(Edge(ch[i % len(ch)].dst, s), key)

            ch = ch2

    return ch

# find conjugate point in set of points for edge
# input: e - edge for which needs to find conjugate point
#        st - set of points
# output: point
def conjugate(e, st):
    et = Edge(e.org, e.dst)
    et.rotate()
    s0 = et.org
    tMin = float_info.max
    pt = None
    for i in range(0, len(st)):
        s = st[i]
        if e.classify(s) == Position.RIGHT:
            CD = Edge(s0, s)
            CD.rotate()

            t = et.intersect(CD)
            if t < tMin:
                tMin = t
                pt = s

    return pt
