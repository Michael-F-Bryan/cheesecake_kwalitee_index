============
Architecture
============

Overall Design
==============

The system is designed in largely two parts, a front end and a back end. The
back end will download and test all the packages on PyPI_, recording the results
to a database. The front end then uses this data to compile an index that shows
the *kwalitee* of each version of each package that has been tested.

Due to the sheer number of packages already uploaded to PyPI_ it will be
necessary to distribute the testing among a large number of computers. Each
testing node should test a package in a sandboxed environment (i.e. Docker_),
be almost completely stateless, and be designed in such a way that horizontal
scaling is effortless.


Front End
---------

The front end website should be fairly simple. It will most probably just be a
Django_ site that reads from the central database and displays the data in an
easily readable form.


Back End
--------

The back-end will consist of a couple services working together, which may or
may not be on the same box. These services are:

Relational Database
    Preferably Postgres.
Testing Daemon 
    A program that will sit on a box, starting up new tests in
    their own Docker container when necessary and reporting test results to 
    the database.
Message Queue 
    To let the testing daemons know what package and version they
    should test next. Will most probably be implemented with a simple Redis_
    queue
Master Node 
    to keep an eye on the testing daemons and monitor their status,
    occasionally giving out new commands for it to execute (e.g. update,
    shut down, reload config etc.)


.. _PyPI: https://pypi.python.org/pypi
.. _Docker: https://www.docker.com/
.. _Django: https://www.djangoproject.com/
.. _Redis: http://redis.io/
