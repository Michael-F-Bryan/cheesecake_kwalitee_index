import subprocess
import sys


class Runner:
    def __init__(self, package, version):
        self.package = package
        self.version = version

    def run(self):
        cmd = 'cheesecake-eval '
        proc = subprocess.Popen()
