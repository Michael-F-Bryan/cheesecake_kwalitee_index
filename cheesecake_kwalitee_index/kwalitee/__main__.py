#!/usr/bin/env python3

"""
Install a package and go through the test suite in order to get a "cheesecake
kwalitee score" for the specific package and version.

Usage: kwalitee [options] <package>

Options:
    -h --help               View this help test.
    -v=PKG_VERSION --package-version=PKG_VERSION
                            The version number of the package to install.
    -V --version            Print the cheesecake_kwalitee_index version number.
"""

from cheesecake_kwalitee_index.kwalitee import models, evaluator
from cheesecake_kwalitee_index import __version__


def main():
    args = docopt.docopt(__doc__, version=__version__)

    package = args['<package>']
    version = args.get('--package-version', '*')
    ev = evaluator.Evaluator(package, version)

    score, total = ev.evaluate_score()
    print('package = {}'.format(package)
