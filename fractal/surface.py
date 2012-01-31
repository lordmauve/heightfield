import os
import random
from PIL import Image


class Surface(object):
    def __init__(self, size):
        self.surface = [0] * size * size
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
    def make_cone(size):
        s = Surface(size)
        w = float(size - 1)
        for x in range(size):
            for y in range(size):
                dx = 2.0 * x / w - 1.0
                dy = 2.0 * y / w - 1.0
                h = max(0, (1 - abs(dx)) * (1 - abs(dy)))
                s[x, y] = h
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
        im = Image.new('L', (self.size, self.size))
        for y in xrange(self.size):
            for x in xrange(self.size):
                h = self[x, y]
                im.putpixel((x, y), min(1.0, h * 0.1) * 255)
        return im


SIZE = 256
landscape = Surface(256)
c = Surface.make_cone(32)

for i in range(SIZE * 5):
    landscape.blit(c, random.randint(0, SIZE), random.randint(0, SIZE))

print landscape
landscape.to_pil().save('out.png')
os.system('gnome-open out.png')
