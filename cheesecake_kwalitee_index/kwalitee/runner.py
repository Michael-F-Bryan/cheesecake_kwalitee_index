"""
"""

import os
import re
import glob
import pip
import subprocess

from cheesecake_kwalitee_index.utils import get_logger


logger = get_logger(__name__, 'stderr')

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
