import math
from numpy import zeros
from PIL import Image
from pkg_resources import resource_stream

colours = Image.open(resource_stream(__name__, 'data/heightmap.png'))


class Surface(object):
    def __init__(self, size):
        self.surface = zeros((size, size))
        self.size = size
        self.dirty = True

    def __getitem__(self, pos):
        return self.surface[pos]

    def __setitem__(self, pos, value):
        self.surface[pos] = value
        self.dirty = False

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
        """Create a surface of size x size representing a cone of height"""
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
        """Add the heights in img to this surface at (x, y)"""
        if x < 0:
            sx = -x
            dx = 0
        else:
            sx = 0
            dx = x
        if y < 0:
            sy = -y
            dy = 0
        else:
            sy = 0
            dy = y
        w = img.size - sx
        h = img.size - sy
        dx2 = min(dx + w, self.size)
        dy2 = min(dy + h, self.size)
        sw, sh = self.surface[dx:dx2, dy:dy2].shape
        self.surface[dx:dx2, dy:dy2] += img.surface[sx:sx + sw, sy:sy + sh]
        self.dirty = True

    def to_pil(self):
        im = Image.new(colours.mode, (self.size, self.size))
        for y in xrange(self.size):
            for x in xrange(self.size):
                h = self[x, y]
                val = max(0, min(1.0, h * 0.1) * 255)
                col = colours.getpixel((int(val), 0))
                im.putpixel((x, y), col)
        return im
