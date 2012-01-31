import sys
import os
import math
import random
from PIL import Image

colours = Image.open('colours.png')

class Surface(object):
    def __init__(self, size, fill=0):
        self.surface = [fill] * size * size
        self.size = size

    def index(self, pos):
        x, y = pos
        if 0 <= x < self.size:
            if 0 <= y < self.size:
                return x + y * self.size
        raise IndexError("out of range")

    def __getitem__(self, pos):
        return self.surface[self.index(pos)]

    def __setitem__(self, pos, value):
        self.surface[self.index(pos)] = value

    def __repr__(self):
        s = []
        for y in xrange(self.size):
            for x in xrange(self.size):
                h = self[x, y]
                s.append("%5.2f " % h)
            s.append('\n')
        return ''.join(s)
            

    @staticmethod
    def make_cone(size, height):
        s = Surface(size)
        w = float(size - 1)
        for x in range(size):
            for y in range(size):
                dx = 2.0 * x / w - 1.0
                dy = 2.0 * y / w - 1.0
                h = max(0, 1.0 - math.sqrt(dx ** 2 + dy ** 2))
                s[x, y] = h * height
        return s

    def blit(self, img, x, y):
        for sy in range(img.size): 
            for sx in range(img.size):
                dx = sx + x
                dy = sy + y
                try:
                    self[dx, dy] += img[sx, sy]
                except IndexError:
                    pass

    def to_pil(self):
        im = Image.new(colours.mode, (self.size, self.size))
        for y in xrange(self.size):
            for x in xrange(self.size):
                h = self[x, y]
                val = max(0, min(1.0, h * 0.1) * 255)
                col = colours.getpixel((int(val), 0))
                im.putpixel((x, y), col)
        return im


SIZE = 512
landscape = Surface(256, fill=-0.25)

for i in range(4):
    d = 25 * i + 20
    c = Surface.make_cone(d, (i + 1) * 0.2)
    sys.stdout.write('.')
    sys.stdout.flush()
    for i in range(100 * (5 - i)):
        landscape.blit(c, random.randint(-d, SIZE), random.randint(-d, SIZE))
print

landscape.to_pil().save('out.png')
os.system('gnome-open out.png')
