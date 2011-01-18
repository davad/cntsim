
"""
Simulation of carbon nanotube growth using a dynamic mass-spring model for nanotubes
"""


from __future__ import print_function

import sys
import optparse


class optopt(optparse.OptionParser):
    """
	Subclassed OptionParser, to prevent exiting from the interpreter when
    called interactively.
	"""

    class optexit(Exception):
        def __init__(self, msg, status):
            self.msg = msg
            self.status = status

        def __str__(self):
            return self.msg

    def exit(self, status=0, msg=None):
        """Base class version with sys.exit() replaced by raise."""

        if msg:
            sys.stderr.write(msg)
        raise self.optexit(msg, status)


def adjutant(a, b, c):
    """The starting point for code."""

    print(a, b, c)

    return 0


def main(argv=None):
    """Parse and check options, and then call adjutant()."""

    if argv is None:
        argv = sys.argv[1:]

    try:
        parser = optopt("%prog [options] arg")

        parser.add_option("-f", "--file", dest="filename", help="read data from FILENAME")
        parser.add_option("-v", "--verbose", action="store_true", dest="verbose")
        parser.add_option("-q", "--quiet", action="store_false", dest="verbose")

        (options, args) = parser.parse_args(argv)

        if len(args) != 1:
            parser.error("incorrect number of arguments")
        if options.verbose:
            print("reading ... {0:s} ".format(options.filename))

        return adjutant(1, 2, 3)

    except optopt.optexit as e:
        return e.status


if __name__ == "__main__":
    sys.exit(main())
else:
    sys.argv = [ "interpreter" ]