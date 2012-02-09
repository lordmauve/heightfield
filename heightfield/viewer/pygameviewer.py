import sys
import pygame
import threading

pygame.display.init()

class Viewer(threading.Thread):
    def __init__(self, surface, colormapfile):
        threading.Thread.__init__(self)
        self.surface = surface
        self.screen = pygame.display.set_mode((surface.size, surface.size))
        self.lock = threading.RLock()
        self.load_colormap(colormapfile)

    def load_colormap(self, mapfile):
        map = pygame.image.load(mapfile)
        self.colormap = [pygame.Color('black')] * 256
        for i in xrange(map.get_width()):
            self.colormap[i] = map.get_at((i, 0))
    
    def repaint_rgb(self):
        """Draw the surface to the screen"""
        if self.surface.dirty:
            with self.lock:
                self.screen.lock()
                try:
                    for y in xrange(self.surface.size):
                        for x in xrange(self.surface.size):
                            h = self.surface[x, y]
                            val = max(0, min(1.0, h * 0.1) * 255)
                            col = self.colormap[int(val)]
                            self.screen.set_at((x, y), col)
                    self.surface.dirty = False
                finally:
                    self.screen.unlock()


    def progress_callback(self, surface, pass_, passes, fraction):
        self.repaint_rgb()

    def run(self):
        clock = pygame.time.Clock()
        while True:
            clock.tick(6)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
            pygame.display.flip()
