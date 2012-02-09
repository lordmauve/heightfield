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
    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option('-d', '--display', help='Incremental rendering of the heightfield generation', action='store_true')
    parser.add_option('-s', '--size', type='int', help='Size of heightfield to generate', default=SIZE)
    parser.add_option('-o', '--output', help='File to write output to')

    options, args = parser.parse_args()

    if not options.output and not options.display:
        parser.error("You must specify a file to output to (-o) if incremental rendering is not enabled (-d).")

    landscape = Surface(options.size)
    if options.display:
        from .viewer.pygameviewer import Viewer
        from pkg_resources import resource_stream
        landscape = Surface(SIZE)
        viewer = Viewer(landscape, resource_stream(__name__, 'data/heightmap.png'))
        viewer.start()
        callback = viewer.progress_callback
    else:
        callback = get_cli_callback()

    deposit(landscape, ISLANDS, progress_callback=callback)

    if options.output:
        print "Writing %s..." % options.output
        landscape.to_pil().save(options.output)
