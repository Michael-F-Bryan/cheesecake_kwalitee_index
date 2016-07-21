"""
The main suite of tests that are run to generate the cheesecake kwalitee
index of a package.
"""

import os
import re
import subprocess
import tempfile
import shutil
import pip
import importlib
import sys

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
            break
    else:
        # It couldn't find our score so there must have been an error
        logger.error('Error while lint checking %s', package)
        logger.error('Stdout = \n%s', proc.stdout.read().strip())
        logger.error('Stderr = \n%s', proc.stderr.read().strip())
        raise RuntimeError('Linter failed with error code: {}'.format(
            proc.returncode))

    return float(score.group(1))


def get_version_number(file_path, name):
    # Add the file_path to sys.path
    sys.path.append(file_path)

    # Then import the package and bind it to a variable
    pkg = importlib.import_module(name)
    try:
        return pkg.__version__
    except AttributeError:
        return None


class Evaluator:
    """
    The Evaluator is in charge of downloading a package and evaluating
    it against the cheesecake kwalitee index.
    """

    def __init__(self, package, version='*'):
        self.package = package
        self.name = package.replace('-', '_')
        self.version = version
        self.score = {
            'install': Score(0, 10),
            'version_number': Score(0, 10),
            'lint': Score(0, 100),
        }
        self.dest = tempfile.mkdtemp(prefix='cheesecake_')
        self.version_number = None

    def evaluate_score(self):
        """
        Run the entire test suite and get the package's score.
        """
        logger.info('Evaluating score for %s', self.package)
        try:
            ins = self.score['install']
            ins.value = self.install_package()

            # Stop early if we couldn't install
            if self.score['install'].value == 0:
                return

            self.score['version_number'].value = self.get_version()
            self.score['lint'].value = self.lint_test()
        finally:
            self.clean_up()

        # Let the tempdir be deleted and return the final score as a tuple
        final_score = sum(s.value for s in self.score.values())
        total = sum(s.total for s in self.score.values())
        return final_score, total

    def get_version(self):
        """
        Get __version__. If __version__ exists then give 10 points, otherwise
        zero.
        """
        file_path = os.path.join(self.dest, self.name)
        version_number = get_version_number(file_path, self.name)

        # Save the version number for later
        self.version_number = version_number

        if version_number is not None:
            return 10
        else:
            return 0

    def lint_test(self):
        """
        Pass the package through the linter.
        """
        temp = lint(self.dest, self.name)
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
