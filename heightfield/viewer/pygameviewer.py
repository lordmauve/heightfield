import sys
import pygame
import threading
from numpy import ndenumerate

pygame.display.init()


class Viewer(threading.Thread):
    def __init__(self, surface, colormapfile):
        threading.Thread.__init__(self)
        self.surface = surface
        self.screen = pygame.display.set_mode((surface.size, surface.size))
        self.img = pygame.Surface((surface.size, surface.size), depth=32)
        self.load_colormap(colormapfile)

    def load_colormap(self, mapfile):
        map = pygame.image.load(mapfile).convert(self.img)
        self.colormap = pygame.surfarray.pixels2d(map)[..., 0]

    def repaint_rgb(self):
        """Draw the surface to the screen"""
        if self.surface.dirty:
            surf = pygame.surfarray.pixels2d(self.img)
            for pos, h in ndenumerate(self.surface.surface):
                val = max(0, min(255, int(h * 25.5)))
                col = self.colormap[val]
                surf[pos] = col
            self.surface.dirty = False
            del surf
            self.screen.blit(self.img, (0, 0))

    def progress_callback(self, surface, pass_, passes, fraction):
        """Use this viewer to show the progress of the deposition"""
        self.repaint_rgb()

    def run(self):
        """Run the event loop"""
        clock = pygame.time.Clock()
        while True:
            clock.tick(6)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
            pygame.display.flip()
