"""
A system that evaluates the kwalitee of all the packages on PyPI.

The cheesecake_kwalitee_index is a multi-part distributed system that checks
out each version of each package on PyPI and runs the `cheesecake` ranking
algorithm on the package in a sandboxed environment and reports the results
to a central database server.
"""

__author__ = 'Michael F Bryan'
__email__ = 'michaelfbryan@gmail.com'
__version__ = '0.1.1'
