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
