import sys
import random
from .surface import Surface


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: heightfield <output file>")

    outfile = sys.argv[1]
    SIZE = 512
    landscape = Surface(256, fill=-0.25)

    for i in range(4):
        d = 25 * i + 20
        c = Surface.make_cone(d, (i + 1) * 0.2)
        sys.stdout.write('.')
        sys.stdout.flush()
        for i in range(100 * (5 - i)):
            xpos = random.randint(-d, SIZE)
            ypos = random.randint(-d, SIZE)
            landscape.blit(c, xpos, ypos)
    print

    landscape.to_pil().save(outfile)


ISLAND_CHAIN = [
    # size, height, number
    (100, 0.8, 200),
    (75, 0.6, 300),
    (50, 0.4, 400),
    (25, 0.2, 500),
]

CONTINENTAL = [
    (200, 0.7, 150),
    (50, 0.5, 300),
    (30, 0.2, 1000),
]

ISLANDS = [
    (200, 1, 50),
    (50, 0.3, 500),
    (30, 0.1, 2000),
]

def visible_deposition():
    from .viewer.pygameviewer import Viewer
    from pkg_resources import resource_stream
    SIZE = 768
    landscape = Surface(SIZE, fill=-0.25)
    viewer = Viewer(landscape, resource_stream(__name__, 'data/heightmap.png'))
    viewer.start()

    octaves = ISLANDS

    for size, height, number in octaves:
        number = int(number * (SIZE / 512.0) ** 2)
        c = Surface.make_cone(size, height)
        sys.stdout.write('.')
        sys.stdout.flush()
        for j in xrange(5):
            with viewer.lock:
                for i in range(number // 5):
                    xpos = random.randint(-size, SIZE)
                    ypos = random.randint(-size, SIZE)
                    landscape.blit(c, xpos, ypos)

    print "finished."
