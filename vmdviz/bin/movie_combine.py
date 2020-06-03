from vmdviz.tools import *
import sys
import argparse
import json

def main():
    """Simple script for viewing multiple movies in a single window.
    If an outfile is supplied, the combined videos are written to file.
    If an outfile is not specifed, the combined videos are viewed
    interactively, and the user can manipulate the video using keyboard
    commands.
    """

    args = sys.argv[1:]
    options, parser = argparser(args)
    if options.files == None:
        parser.print_help()
        sys.exit(0)


    if options.titles:
        if len(options.titles) != len(options.files):
            raise RuntimeError("If --titles is specified, it must "
                               "be the same length as --files")

    dash = Dashboard(options.files, labels=options.titles)

    if options.outfile != None:
        dash.write_movie(options.outfile, fourcc=options.fourcc)
    else:
        dash.play_movies()


def argparser(args):
    HOME = os.path.expanduser("~")
    parser = argparse.ArgumentParser(description='a tool for stacking videos '
                             'together within a single window and saving to file.',
                             formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("files", nargs="+", help="input movie files to stack "
                        "into a single window")
    parser.add_argument("--outfile", help='name of output movie file')
    parser.add_argument("--titles", nargs="+", help="optional titles for stacked "
                        "videos, following the same order as --files", default=None)
    parser.add_argument("--fourcc", help='FOURCC code for video writing.',
                        default='MJPG')

    return parser.parse_args(args), parser


if __name__ == 'movie_combine':
    main()
