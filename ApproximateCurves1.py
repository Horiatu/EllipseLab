
import math
from Tkinter import *
import turtle
import re


precision = 25
def setpos(t, x, y, ):
    t.setpos(x*precision, y*precision)

def atan2(x, y, deg=False):
    if (x==0) & (y==0):
        return 0
    a = math.atan2(x, y)
    if a < 0:
        a = 2*math.pi+a
    if deg:
        a = a*180/math.pi
    return a


dd, ll = 60,60
xl = 0 # int(-ll * 1.5)
xr = 2*int((2 * dd - ll) * 1.5)
yl, yr = -dd, dd


class Sketch:
    def __init__(self, xl, xr, yl, yr, title):
        self.screen = turtle.Screen()

        self.pen = turtle.Turtle()
        self.penEllipse = turtle.Turtle()
        self.penTolerance = turtle.Turtle()
        self.penApproximate = turtle.Turtle()

        self.pen.ht()
        self.penEllipse.ht()
        self.penTolerance.ht()
        self.penApproximate.ht()

        self.setupGrid(xl, xr, yl, yr, title)
        self.penDown = False
        self.LastPoint = None

    def setupGrid(self, xl, xr, yl, yr, title):
        if self.screen.window_width > self.screen.window_height:
            max_size = self.screen.window_height()
        else:
            max_size = self.screen.window_width()

        screen = turtle.Screen()
        screen.title(title)
        r = (yl - yr) / (xl - xr + 0.0)
        screen.setup(width=max_size / r, height=int(max_size), startx=None, starty=10)
        screen.setworldcoordinates(xl * precision, yl * precision, xr * precision + 4, yr * precision + 4)
        t = turtle.Turtle()
        t.ht()
        t.speed(0)

        for x in range(xl, xr + 1):
            if x == 0:
                t.pencolor("darkgray")
                t.pensize(3)
            else:
                t.pensize(1)
                if x % 10 == 0:
                    t.pencolor("black")
                else:
                    t.pencolor("gray")
            t.pu()
            setpos(t, x, yr)
            t.pd()
            setpos(t, x, yl)

        for y in range(yl, yr + 1):
            if y == 0:
                t.pensize(3)
                t.pencolor("darkgray")
            else:
                t.pensize(1)
                if y % 10 == 0:
                    t.pencolor("black")
                else:
                    t.pencolor("gray")
            t.pu()
            setpos(t, xl, y)
            t.pd()
            setpos(t, xr, y)
        return

    def Clear(self):
        sketch.pen.clear()
        sketch.penEllipse.clear()
        sketch.penTolerance.clear()
        sketch.penApproximate.clear()
        self.penDown = False
        return self.penDown

    def PenUp(self):
        sketch.pen.pu()
        sketch.penEllipse.pu()
        sketch.penTolerance.pu()
        sketch.penApproximate.pu()
        self.penDown = False
        return self.penDown

    def PenDown(self):
        sketch.pen.pd()
        sketch.penEllipse.pd()
        sketch.penTolerance.pd()
        sketch.penApproximate.pd()
        self.penDown = True
        return self.penDown


sketch = Sketch(-40, 140, -30, 70, ['Sketch'])


class Point:
    def __init__(self, x=0, y=0, color='black', size=1, width=3, speed=0):
        self.x, self.y = x, y

        sketch.pen.pencolor(color)
        sketch.pen.pensize(width)
        sketch.pen.speed(speed)

    def __str__(self):
        if isinstance(self.x, int) & isinstance(self.y, int):
            return str((self.x, self.y))
        else:
            return str((int(self.x * 100) / 100., int(self.y * 100) / 100.))

    # def __str__(self):
    #     return '(' + str(self.x) +', '+ str(self.y) +')'

    def __repr__(self):
        return self.__str__()

    def moveTo(self, p):
        self.x, self.y = p.x, p.y

    def draw(self, color='black', size=1, width=3, speed=0):
        sketch.pen.pu()
        sketch.pen.pencolor(color)
        sketch.pen.pensize(width)
        sketch.pen.speed(speed)
        size__ = size / 10.
        setpos(sketch.pen, self.x - size__, self.y)
        sketch.pen.pd()
        setpos(sketch.pen, self.x + size__, self.y)
        sketch.pen.pu()
        setpos(sketch.pen, self.x, self.y - size__)
        sketch.pen.pd()
        setpos(sketch.pen, self.x, self.y + size__)
        sketch.pen.pu()
        return

    def drawline(self, p, color='black', width=3, speed=0):
        sketch.pen.pu()
        sketch.pen.ht()
        sketch.pen.pencolor(color)
        sketch.pen.pensize(width)
        sketch.pen.speed(speed)
        setpos(sketch.pen, self.x, self.y)
        sketch.pen.pd()
        setpos(sketch.pen, p.x, p.y)
        sketch.pen.pu()
        return

    def distance(self, p):
        return math.sqrt((self.x - p.x) ** 2 + (self.y - p.y) ** 2)

    def label(self, l='', color='black', align='center', font=("Arial", 8, "normal")):
        if l == '':
            l = (int(self.x * 100) / 100., int(self.y * 100) / 100.0)
        sketch.pen.pencolor(color)
        sketch.pen.pu()
        # assert isinstance(self, Point)
        setpos(sketch.pen, self.x, self.y + 0.1)
        sketch.pen.write(l, align=align, font=font)

    def equals(self, p):
        return (p.x == self.x) & (p.y == self.y)

    def get_good_aprox(self, tol):
        p = self.match(tol)
        if (p):
            # print p
            return Point(int(p.x), int(p.y))
        return None

    def match(self, tol):
        point = Point(math.floor(self.x), math.floor(self.y))
        d = self.distance(point)
        if (d <= tol):
            return point
        point = Point(math.ceil(self.x), math.floor(self.y))
        d = self.distance(point)
        if (d <= tol):
            return point
        point = Point(math.floor(self.x), math.ceil(self.y))
        d = self.distance(point)
        if (d <= tol):
            return point
        point = Point(math.ceil(self.x), math.ceil(self.y))
        d = self.distance(point)
        if (d <= tol):
            return point
        return None

    def translate(self, point):
        self.x, self.y = self.x + point.x, self.y + point.y


class Bow:
    def __init__(self, spec='', p1=Point(0,0), p2=Point(0,0), arrow=0):
        self.spec, self.arrow = spec, arrow
        self._p1 = p1
        self._p2 = p2
        self._approximates = None
        self.samples = None
        self._init_()

        sketch.penEllipse.pu()
        sketch.penEllipse.pensize(2)
        sketch.penEllipse.speed(0)
        sketch.penEllipse.pencolor('red')

        sketch.penTolerance.pencolor("pink")
        sketch.penTolerance.fillcolor("magenta")
        sketch.penTolerance.pensize(1)

        sketch.penApproximate.pu()
        sketch.penApproximate.speed(0)
        sketch.penApproximate.pencolor('black')
        sketch.penApproximate.pensize(3)

    def _init_(self):
        self._p0 = Point((self.p1.x+self.p2.x)/2.0, (self.p1.y+self.p2.y)/2.0)
        self._alpha = atan2(self.p2.y - self.p1.y, self.p2.x - self.p1.x)
        self._pa = self.rotate(Point(self.p0.x, self.p0.y+self.arrow))
        diameter = self.p1.distance(self.p2)
        self.area = math.pi * diameter * self.arrow / 4.
        self.approximate_area = None
        return

    @property
    def approximates(self):
        return self._approximates

    @property
    def p0(self):
        return self._p0

    @property
    def pa(self):
        return self._pa

    @property
    def alpha(self):
        return self._alpha

    @property
    def arrow(self):
        return self._arrow

    @arrow.setter
    def arrow(self, value):
        self._arrow=value

    @property
    def p1(self):
        return self._p1

    # @p1.setter
    # def p1(self, value):
    #     self._p1=value

    @property
    def p2(self):
        return self._p2

    # @p2.setter
    # def p2(self, value):
    #     self._p2=value

    def get_area_error(self):
        s = str(math.fabs(int(self.area * 100) / 100.))
        if self.approximate_area is not None:
            s += ', '+str(math.fabs(self.approximate_area)) +' ~ '+str(int(math.fabs((self.area-self.approximate_area)/(self.area+self.approximate_area))*2000.)/10.)+'%'
        return s

    def __str__(self):
        s = '( "' + self.spec +'"'
        s += ', ' + str(self.p1) +', ' + str(self.p2)
        # s += ', '+ str(self.p0)
        # s += ', (' + str(int(self.pa.x*10)/10.)+', '+ str(int(self.pa.y*10)/10.)+')'
        # s+= ', ' + str(self.arrow)
        s += ', areas=(' + self.get_area_error() + '}'
        if self.samples is not None:
            s += ', samples=' + str(self.samples)
        if self.approximates is not None:
            s += ', onGrid=' + str(self.approximates)
        s += ' )'
        return s

    def __repr__(self):
        return self.__str__()

    def rotate(self, p, alpha=None, orig=None):
        if alpha is None:
            alpha = self.alpha
        if orig is None:
            orig = self.p0
        sin, cos = math.sin(alpha), math.cos(alpha)
        return Point(cos * (p.x-orig.x) - sin * (p.y-orig.y) + orig.x, sin * (p.x-orig.x) + cos * (p.y-orig.y) + orig.y)

    def draw_approximates(self):
        setpos(sketch.penApproximate, self.approximates[0].x, self.approximates[0].y)
        sketch.penApproximate.pd()
        for p in self.approximates:
            p.draw('black', 2)
            setpos(sketch.penApproximate, p.x, p.y)
        sketch.penApproximate.pu()
        return

    def show_tolerance(self, p, r, fill=True):
        # sketch.penTolerance.pu()
        # sketch.penTolerance.fill(fill)
        # sketch.penTolerance.setpos(p.x*precision, (p.y - r) * precision)
        # sketch.penTolerance.pd()
        # sketch.penTolerance.circle(r*precision)
        return

    def translate(self, point):
        self._p0.translate(point)
        self._p1.translate(point)
        self._p2.translate(point)
        self._pa.translate(point)

        if (self._approximates != None):
            for p in self._approximates:
                p.translate(point)

        if (self.samples != None):
            for p in self.samples:
                p.translate(point)


    def draw(self, steps=1):
        # self.p1.draw()
        # self.p2.draw()
        # self.pa.draw('red')

        self.p1.drawline(self.p2, 'red', 1)

        r = self.p1.distance(self.p2)/2
        q = self.arrow / r
        sketch.penEllipse.pu()
        for a in range(-90, 91, steps):
            ar = a * math.pi / 180
            p = self.rotate(Point(r * math.sin(ar) + self.p0.x, q * r * math.cos(ar) + self.p0.y))
            setpos(sketch.penEllipse, p.x, p.y)
            sketch.penEllipse.pd()

        if self.samples is not None:
            for p in self.samples:
                p.draw('red')

        if self.approximates is not None:
            self.draw_approximates()

        return

    def sample(self, steps=15):
        r = self.p1.distance(self.p2)/2
        q = self.arrow / r
        self.samples = []
        for a in range(-90, 91, steps):
            ar = a * math.pi / 180
            p = self.rotate(Point(r * math.sin(ar) + self.p0.x, q * r * math.cos(ar) + self.p0.y))
            self.samples.append(p)
        return

    def approximate(self, tol=0.25):

        t = sketch.penApproximate
        t.pensize(3)
        t.pu()

        sketch.penTolerance.pu()

        self._approximates = []
        r = self.p1.distance(self.p2)/2
        q = self.arrow / r
        last = Point(0,0)
        ff = 0
        pl1 = None
        pl2 = None
        for a in range(-90, 91):
            ar = a * math.pi / 180
            p = self.rotate(Point(r * math.sin(ar) + self.p0.x, q * r * math.cos(ar) + self.p0.y))
            # setpos(t, p.x, p.y)
            # t.pd()

            if len(self.approximates) > 0:
                ff = (p.distance(last) - 29./precision)
                if ff < 0:
                    ff = 0
                else:
                    ff /=  29./precision
                # print ff, last, pr

            rr = tol * (1 + ff)
            pa = p.get_good_aprox(rr)

            if pa is not None:

                self.show_tolerance(pa, rr)

                last = p
                if pl1 is None:
                    self.approximates.append(pa)
                    pl1 = pa
                else:
                    if not pl1.equals(pa):
                        if len(self.approximates)>1:
                            a1 = atan2(self.approximates[-1].x - pa.x, self.approximates[-1].y - pa.y)
                            a2 = atan2(self.approximates[-2].x - pa.x, self.approximates[-2].y - pa.y)
                            if a1 != a2:
                                if not self.is_concave(pa, pl1, pl2):
                                    self.approximates.append(pa)
                                    pl2 = pl1
                                    pl1 = pa
                                else:
                                    self.approximates.remove(self.approximates[-1])
                                    self.approximates.append(pa)
                                    # pl2 = pl1
                                    pl1 = pa
                                    pl2 = self.approximates[-2]
                            else:
                                self.approximates[-1] = pa
                                # pl2 = pl1
                                pl1 = pa
                        else:
                            self.approximates.append(pa)
                            pl1 = pl2
                            pl2 = pa

        self.get_approximate_area()
        return

    def is_concave(self, p, p1, p2):
        if p2 is None:
            return False

        a1 = math.atan2(p2.y - p1.y, p2.x - p1.x) * 180 / math.pi
        a2 = math.atan2(p1.y - p.y, p1.x - p.x) * 180 / math.pi

        if a1 >= 180:
            a1 = 360 - a1
        if a2 >= 180:
            a2 = 360 - a2

        if a1*a2 < 0:
            a1 = 360-a1

        if math.fabs(a1) == 180:
            a1 = math.copysign(a1, a2)

        if math.fabs(a2) == 180:
            a2 = math.copysign(a2, a1)

        sign =  math.copysign(1, (a1 - a2) * self.arrow)


        if sign <= 0:
            # p2.draw('green', 3,5)
            p1.draw('gray', 3)
            # p.draw('cyan', 3,5)
            # print 'p2',p2, 'p1',p1, 'p',p, 'a2',int(a2), 'a1',int(a1), 'sign',sign, int(a1 - a2), self.arrow
            return True
        else:
            return False

    def get_approximate_area(self):
        last = Point(0, 0)
        a = 0.
        for i in range(1, len(self.approximates)):
            p=self.rotate(self.approximates[i], -self.alpha, self.p1)
            # p.draw()
            a = a+(last.y+p.y)*(p.x-last.x)/2.
            last = p
        self.approximate_area = a
        return

    def get_best_point_for_label(self):
        if self.approximates is not None:
            points = self.approximates
        else:
            if self.samples is not None:
                points = self.samples
            else:
                return self.p0

        p = self.p1
        m = 0
        a = (self.p1.x - self.p2.x)*self.arrow
        if a<=0:
            for pp in points:
                if pp.y > p.y:
                    p = pp
                    m = p.y
            if p.y < self.pa.y:
                p = self.pa
            return Point((self.pa.x + self.p0.x)/2., p.y+0.5)
        else:
            for pp in points:
                if pp.y <= p.y:
                    p = pp
                    m = p.y
            if p.y > self.pa.y:
                p = self.pa
            return Point((self.pa.x + self.p0.x)/2., p.y-2)


def decodeEllipse(spec):
    print spec
    regex = "([L|R|U|D|I|O]\d+)"
    tok = re.findall(regex, spec)
    # nn = []

    x, y, arrow = 0,0,0
    for t in tok:
        n = int(t.strip('LRUDOI'))
        if t[0] == 'U':
            y = n
        else:
            if t[0]=='D':
                y = -n
            else :
                if t[0] == 'L':
                    x = -n
                else:
                    if t[0] == 'R':
                        x = n
                    else:
                        if t[0] == 'O':
                            arrow = n
                        else:
                            if t[0] == 'I':
                                arrow = -n

    bow = Bow(spec, Point(0,0), Point(x, y), arrow)
    # nn.append((p1,p2,d))

    return bow

def gepenEllipsePoints(b, approximateMode=False):
    if(approximateMode):
        b.aproximate()
        return b.approximates
    else:
        b.sample()
        return b.samples


# points = decodeEllipse('...').gepenEllipsePoints()  # get samples
# or
# points = gepenEllipsePoints(decodeEllipse('...'), True)  # get approximates


def showBows(index, bows):
    a = []
    for b in bows:
        b.sample()
        b.approximate()

        b.draw()

        a.append(b)

    if len(a)>0:
        print index, a
    return

def decodeLength(spec):
    x, y = 0, 0
    s = spec[0]
    n = int(spec.strip('VLRUD'))
    if s == 'U':
        y = n
    else:
        if s == 'D':
            y = -n
        else:
            if s == 'L':
                x = -n
            else:
                if s == 'R':
                    x = n
    return Point(x, y)


def decodeSketch(spec):
    sketch.penDown = True

    regex = "BV?(([L|R|U|D]\d+)?[L|R|U|D]\d+[I|O]\d+)|(?:V([L|R|U|D]\d+))?([L|R|U|D]\d+)|(A(\d+)|C)"
    # regex = "(B[V|U|D|L|R]([L\d+|R\d+|U\d+|D\d+])+[I|O]\d+)|(?:V)([L|R]\d+)([U|D]\d+)|([L|R]\d+)|([U|D]\d+)"
    print spec
    segments = re.findall(regex, spec)
    print segments
    # LastPoint.draw('Red', 6)
    for segment in segments:
        if(segment[5] != ''):
            sketch.penDown = sketch.PenUp()
        if (segment[5] == '0'):
            sketch.penDown = sketch.Clear()
            sketch.LastPoint = Point(0,0)
            sketch.penDown = False
        if (segment[4] == 'C'):
            sketch.penDown = sketch.PenDown()
        if(segment[0] != ''):
            b = decodeEllipse(segment[0])
            b.translate(sketch.LastPoint)
            # b.sample()
            b.approximate()
            b.draw()
            sketch.LastPoint.moveTo(b.p2)
            # LastPoint.draw('Black', 6)
        else:
            p0 = Point(sketch.LastPoint.x, sketch.LastPoint.y)
            if(segment[2] != ''):
                sketch.LastPoint.translate(decodeLength(segment[2]))
            if (segment[3] != ''):
                sketch.LastPoint.translate(decodeLength(segment[3]))

            if(sketch.penDown):
                p0.drawline(sketch.LastPoint, 'red', 3)
            # print p0, LastPoint

    # LastPoint.draw('Blue',6)



f = open('data.txt')
index = 0
av = 0
nv = 0
for line in f:
    index += 1
    if line.strip() == 'stop':
        if nv > 0:
            print str(int(av / nv * 100)/10.)+'%'
        k = raw_input("press [Enter] to end...")
        exit()

    # bows = decodeEllipses(line)
    decodeSketch(line)
    # //showBows(index, bows)
    k = raw_input("press [Enter] to continue...")
    # ClearSketch()

    # fn = ''
    # for b in bows:
    #     if b.approximates is not None:
    #         err = math.fabs((b.area - b.approximate_area) / (b.area + b.approximate_area))*2
    #         av +=err
    #         nv += 1
    #
    #     b.get_best_point_for_label().label(
    #             b.get_area_error(),
    #         'red', 'center', ("Arial", 14, "normal"))
    #
    #     if fn != '':
    #         fn += '+'
    #     fn += b.spec
    #
    # if fn != '':
    #     s = str(index)
    #     while len(s)<3:
    #         s = '0'+s
    #     ts.getcanvas().postscript(file="C:\Users\htudosie\Desktop\E\\"+s+'.'+fn+ ".eps")
    #     _t.clear()
    #     _penEllipse.clear()
    #     _penTolerance.clear()
    #     _penApproximate.clear()

# pen.Screen().exitonclick()
