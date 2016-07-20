"""
"""

import os
import re
import glob
import pip
import subprocess
from collections import namedtuple

from cheesecake_kwalitee_index.utils import get_logger


logger = get_logger(__name__, 'stderr')
Score = namedtuple('Score', ['value', 'total'])



def download(package, dest):
    """
    Download a package to a specified location.
    """
    return pip.main(['install', 
                     '--target', dest, 
                     '--no-binary', ':all:', 
                     package])


def lint(dest, name):
    package = os.path.join(dest, name)

    cmd = 'pylint {}'.format(package)
    proc = subprocess.Popen(cmd, 
                          stdout=subprocess.PIPE, 
                          stderr=subprocess.PIPE,
                          shell=True)
    proc.wait()

    for line in proc.stdout.read().decode().splitlines():
        if line.startswith('Your code has been rated at'):
            score = re.search(r'(-?\d+(?:\.\d+)?)/10', line)
            return float(score.group(1))
    else:
        # It couldn't find our score so there must have been an error
        raise RuntimeError('Linter failed with error code: {}'.format(
            proc.returncode))


class Evaluater:
    def __init__(self, package, version='*'):
        self.package = package
        self.version = version
        self.score = {
                'install': Score(0, 10),
                'lint': Score(0, 100),
                }

    def score(self):
        with tempfile.mkdtemp(prefix='cheesecake_') as dest:
            self.dest = dest

            self.score['install'].value = self.install_test()

            # Stop early if we couldn't install
            if self.score['install'].value == 0:
                return

            self.score['lint'].value = self.install_test()

        # Let the tempdir be deleted and return the final score
        final_score = sum(s.value for s in self.score.values())
        total = sum(s.total for s in self.score.values())
        return final_score, total

    def lint_test(self):
        """
        Pass the package through the linter.
        """
        return 10 * lint(self.dest, self.package.replace('-', '_'))

    def install_test(self):
        """
        Try to install the package. If it installs, you get 10 points. 
        Otherwise you get nothing.
        """
        package_version = self.package + '==' + self.version
        ret = download(package_version, self.dest)

        if ret:
            return 0
        else:
            return self.score['install'].total



