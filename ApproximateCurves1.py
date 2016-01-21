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


dd, ll = 30,30
xl, xr = int(-ll*1.5), int((2*dd - ll)*1.5)
yl, yr = -dd, dd

ts = turtle.Screen()
def setupGrid(xl, xr, yl, yr, title):
    # ts = turtle.Screen()
    if ts.window_width > ts.window_height:
        max_size = ts.window_height()
    else:
        max_size = ts.window_width()

    screen = turtle.Screen()
    screen.title(title)
    r = (yl-yr)/(xl-xr+0.0)
    screen.setup(width=max_size/r, height=int(max_size), startx=None, starty=10)
    screen.setworldcoordinates(xl * precision, yl * precision, xr * precision + 4, yr * precision + 4)
    t = turtle.Turtle()
    t.ht()
    t.speed(0)

    for x in range(xl, xr + 1):
        if x == 0:
            t.pencolor("black")
        else:
            t.pencolor("gray")
        t.pu()
        setpos(t, x, yr)
        t.pd()
        setpos(t, x, yl)

    for y in range(yl, yr + 1):
        if y == 0:
            t.pencolor("black")
        else:
            t.pencolor("gray")
        t.pu()
        setpos(t, xl, y)
        t.pd()
        setpos(t, xr, y)
    return

setupGrid(xl, xr, yl, yr, ['Approximate Ellipse'])

_t = turtle.Turtle()
class Point:
    def __init__(self, x, y, color='black', size=1, width=3, speed=0):
        self.x, self.y = x,y
        self.t = _t
        self.t.pencolor(color)
        self.t.pensize(width)
        self.t.speed(speed)

    def __str__(self):
        if isinstance(self.x, int) & isinstance(self.y, int):
            return str(( self.x , self.y ))
        else:
            return str(( int(self.x*100)/100. , int(self.y*100)/100. ))

    # def __str__(self):
    #     return '(' + str(self.x) +', '+ str(self.y) +')'

    def __repr__(self):
        return self.__str__()

    def draw(self, color='black', size=1, width=3, speed=0):
        self.t.pu()
        self.t.pencolor(color)
        self.t.pensize(width)
        self.t.speed(speed)
        size__ = size / 10.
        setpos(self.t, self.x - size__, self.y)
        self.t.pd()
        setpos(self.t, self.x + size__, self.y)
        self.t.pu()
        setpos(self.t, self.x, self.y - size__)
        self.t.pd()
        setpos(self.t, self.x, self.y + size__)
        self.t.pu()
        return

    def drawline(self, p, color='black', width=3, speed=0):
        self.t.pu()
        # t.ht()
        self.t.pencolor(color)
        self.t.pensize(width)
        self.t.speed(speed)
        setpos(self.t, self.x, self.y)
        self.t.pd()
        setpos(self.t, p.x, p.y)
        self.t.pu()
        return

    def distance(self, p):
        return math.sqrt((self.x-p.x)**2 + (self.y-p.y)**2)

    def label(self, l='', color='black', align='center', font=("Arial", 8, "normal")):
        if l == '':
            l = (int(self.x*100)/100., int(self.y*100)/100.0)
        self.t.pencolor(color)
        self.t.pu()
        # assert isinstance(self, Point)
        setpos(self.t, self.x, self.y+0.1)
        self.t.write(l, align=align, font=font)

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

_telipse = turtle.Turtle()
_ttolerance = turtle.Turtle()
_taprox = turtle.Turtle()
class Bow:
    def __init__(self, spec='', p1=Point(0,0), p2=Point(0,0), arrow=0):
        self.spec, self.arrow = spec, arrow
        self._p1 = p1
        self._p2 = p2
        self._approximates = None
        self.samples = None
        self._init_()

        self.telipse = _telipse
        self.telipse.pu()
        self.telipse.pensize(2)
        self.telipse.speed(0)
        self.telipse.pencolor('red')

        self.ttolerance = _ttolerance
        self.ttolerance.pencolor("pink")
        self.ttolerance.fillcolor("magenta")
        self.ttolerance.pensize(1)

        self.taprox = _taprox
        self.taprox.speed(0)
        self.taprox.pencolor('black')
        self.taprox.pensize(3)

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
        setpos(self.taprox, self.approximates[0].x, self.approximates[0].y)
        self.taprox.pd()
        for p in self.approximates:
            p.draw('black', 2)
            setpos(self.taprox, p.x, p.y)
        self.taprox.pu()
        return

    def show_tolerance(self, p, r, fill=True):
        # self.ttolerance.pu()
        # self.ttolerance.fill(fill)
        # self.ttolerance.setpos(p.x*precision, (p.y - r) * precision)
        # self.ttolerance.pd()
        # self.ttolerance.circle(r*precision)
        return

    def draw(self, steps=1):
        # self.p1.draw()
        # self.p2.draw()
        # self.pa.draw('red')

        self.p1.drawline(self.p2, 'red', 1)

        r = self.p1.distance(self.p2)/2
        q = self.arrow / r
        self.telipse.pu()
        for a in range(-90, 91, steps):
            ar = a * math.pi / 180
            p = self.rotate(Point(r * math.sin(ar) + self.p0.x, q * r * math.cos(ar) + self.p0.y))
            setpos(self.telipse, p.x, p.y)
            self.telipse.pd()

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

        t = turtle.Turtle()
        t.pensize(1)
        t.pu()

        self.ttolerance.pu()

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




allellispses = []

def decodeEllipses(spec):
    regex = "(B[V|U|D|L|R]([L\d+|R\d+|U\d+|D\d+])+[I|O]\d+)"
    s = re.findall(regex, spec)
    # print spec
    # print s
    specEllipses=[]
    for el in s:
        specEllipses.append(el[0])

    # print specEllipses

    if len(specEllipses) > 0:
        # print specEllipses

        ellipses = []
        for specEllipse in specEllipses:
            e = specEllipse.strip('BV')
            if not e in allellispses:
                allellispses.append(e)
                ellipses.append(decodeEllipse(e))

        return ellipses

    return

def decodeEllipse(spec):
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

    bows = decodeEllipses(line)
    showBows(index, bows)

    fn = ''
    for b in bows:
        if b.approximates is not None:
            err = math.fabs((b.area - b.approximate_area) / (b.area + b.approximate_area))*2
            av +=err
            nv += 1

        b.get_best_point_for_label().label(
                b.get_area_error(),
            'red', 'center', ("Arial", 14, "normal"))

        if fn != '':
            fn += '+'
        fn += b.spec

    if fn != '':
        s = str(index)
        while len(s)<3:
            s = '0'+s
        ts.getcanvas().postscript(file="C:\Users\htudosie\Desktop\E\\"+s+'.'+fn+ ".eps")
        _t.clear()
        _telipse.clear()
        _ttolerance.clear()
        _taprox.clear()

turtle.Screen().exitonclick()
