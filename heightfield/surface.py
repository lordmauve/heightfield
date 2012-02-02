import math
from PIL import Image
from pkg_resources import resource_stream

colours = Image.open(resource_stream(__name__, 'data/heightmap.png'))


class Surface(object):
    def __init__(self, size, fill=0):
        self.surface = [fill] * size * size
        self.size = size

    def _index(self, pos):
        """Compute the index in self.surface of a given position pos"""
        x, y = pos
        if 0 <= x < self.size:
            if 0 <= y < self.size:
                return x + y * self.size
        raise IndexError("out of range")

    def __getitem__(self, pos):
        return self.surface[self._index(pos)]

    def __setitem__(self, pos, value):
        self.surface[self._index(pos)] = value

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
