import random
from .surface import Surface


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


def deposit(landscape, octaves, base_height=0, progress_callback=None):
    w = h = landscape.size
    landscape.surface += base_height

    total_area = 0.0
    scaled_octaves = []
    for size, height, number in octaves:
        number = int(number * (w / 512.0) * (h / 512.0))
        total_area += number * size * size
        scaled_octaves.append((size, height, number))

    passes = len(octaves)
    progress = 0
    for pass_, (size, height, number) in enumerate(scaled_octaves):
        c = Surface.make_cone(size, height)

        progress_step = (number // 5) * size * size
        for j in xrange(5):
            for _ in xrange(number // 5):
                xpos = random.randint(-size, w)
                ypos = random.randint(-size, h)
                landscape.blit(c, xpos, ypos)
            progress += progress_step
            if progress_callback:
                progress_callback(landscape, pass_, passes, progress / total_area)

    progress_callback(landscape, passes, passes, 1)
