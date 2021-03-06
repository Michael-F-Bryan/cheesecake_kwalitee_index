#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
        'rq',
        'SqlAlchemy',
        'psycopg2',
        'docopt',
        'auto-changelog',
]

test_requirements = [
]

setup(
    name='cheesecake_kwalitee_index',
    version='0.1.1',
    description="A system that evaluates the kwalitee of all the packages on PyPI",
    long_description=readme + '\n\n' + history,
    author="Michael F Bryan",
    author_email='michaelfbryan@gmail.com',
    url='https://github.com/Michael-F-Bryan/cheesecake_kwalitee_index',
    packages=[
        'cheesecake_kwalitee_index',
    ],
    package_dir={'cheesecake_kwalitee_index':
                 'cheesecake_kwalitee_index'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='cheesecake_kwalitee_index',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
)
