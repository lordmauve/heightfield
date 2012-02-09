import sys
from .surface import Surface
from .deposition import deposit, ISLANDS


# default heightfield size
SIZE = 768


def text_progress_callback(surface, pass_, passes, fraction):
    if fraction < 1:
        sys.stdout.write('.')
        sys.stdout.flush()
    else:
        print "finished."

try:
    import progressbar
except ImportError:
    get_cli_callback = lambda: text_progress_callback
else:
    def get_cli_callback():
        widgets = [
            '',
            progressbar.Percentage(),
            ' ',
            progressbar.Bar(),
            ' ',
            progressbar.ETA()
        ]
        pbar = progressbar.ProgressBar(widgets=widgets).start()

        def bar_progress_callback(surface, pass_, passes, fraction):
            widgets[0] = 'Pass %d of %d: ' % (pass_, passes)
            if fraction < 1:
                pbar.update(fraction * 100)
            else:
                pbar.finish()
        return bar_progress_callback


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: heightfield <output file>")

    outfile = sys.argv[1]
    landscape = Surface(SIZE)

    callback = get_cli_callback()
    deposit(landscape, ISLANDS, progress_callback=callback)
    print "Writing %s..." % outfile
    landscape.to_pil().save(outfile)


def visible_deposition():
    from .viewer.pygameviewer import Viewer
    from pkg_resources import resource_stream
    landscape = Surface(SIZE)
    viewer = Viewer(landscape, resource_stream(__name__, 'data/heightmap.png'))
    viewer.start()
    deposit(landscape, ISLANDS, progress_callback=viewer.progress_callback)
