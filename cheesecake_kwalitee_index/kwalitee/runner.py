"""
"""

import os
import re
import subprocess
from collections import namedtuple
import tempfile
import shutil
import pip

from cheesecake_kwalitee_index.utils import get_logger
from cheesecake_kwalitee_index.kwalitee.models import Score


logger = get_logger(__name__, 'stderr')


def download(package, dest):
    """
    Download a package to a specified location. Making sure to get a source
    distribution.
    """
    logger.info('Downloading %s', package)
    return pip.main(['install',
                     '--target', dest,
                     '--no-binary', ':all:',
                     package])


def lint(dest, name):
    """
    Run Pylint and get the overall score of a package.
    """
    package = os.path.join(dest, name)
    logger.info('Lint checking %s', name)

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
        logger.error('Error while lint checking %s', package)
        logger.error('Stdout = \n%s', proc.stdout.read().strip())
        logger.error('Stderr = \n%s', proc.stderr.read().strip())
        raise RuntimeError('Linter failed with error code: {}'.format(
            proc.returncode))


class Evaluater:
    """
    The Evaluator is in charge of downloading a package and evaluating
    it against the cheesecake kwalitee index.
    """

    def __init__(self, package, version='*'):
        self.package = package
        self.version = version
        self.score = {
            'install': Score(0, 10),
            'lint': Score(0, 100),
        }
        self.dest = tempfile.mkdtemp(prefix='cheesecake_')

    def evaluate_score(self):
        logger.info('Evaluating score for %s', self.package)
        try:
            ins = self.score['install']
            ins.value = self.install_package()

            # Stop early if we couldn't install
            if self.score['install'].value == 0:
                print('EXITING EARLY!!!')
                print(self.score)
                return

            self.score['lint'].value = self.install_package()
        finally:
            self.clean_up()

        # Let the tempdir be deleted and return the final score as a tuple
        final_score = sum(s.value for s in self.score.values())
        total = sum(s.total for s in self.score.values())
        return final_score, total

    def lint_test(self):
        """
        Pass the package through the linter.
        """
        temp = lint(self.dest, self.package.replace('-', '_'))
        return 10 * temp

    def install_package(self):
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

    def clean_up(self):
        """
        Remove the installed directory and do any other necessary clean up.
        """
        if self.dest is not None:
            logger.info('Cleaning up %s', self.dest)
            shutil.rmtree(self.dest)
            self.dest = None

