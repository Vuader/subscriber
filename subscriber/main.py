import sys
from luxon.core.handlers.cmd import Cmd
import subscriber.cmd


def main(argv):
    sub = Cmd('subscriber', path='/tmp')
    sub()


def entry_point():
    """Zero-argument entry point for use with setuptools/distribute."""
    raise SystemExit(main(sys.argv))


if __name__ == '__main__':
    entry_point()
