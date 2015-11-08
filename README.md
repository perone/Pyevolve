## Pyevolve [![Build Status](https://travis-ci.org/erikreed-public/Pyevolve.svg)](https://travis-ci.org/erikreed-public/Pyevolve)
This is a fork of [perone/Pyevolve](https://github.com/perone/Pyevolve) that attempts to continue where Pyevolve left off by merging outstanding pull requests, cleaning up the codebase, and adding new features. Pyevolve is a great package that has not been actively maintained by the owner.

#### Notable changes
At the moment, the APIs are consistent/extended from the most recent Pyevolve Pypi package. This corresponds to _Pyevolve 0.6rc1_, updated Dec. 2014.
* Source code is now all PEP8 compliant (or at least, tries to be).
* All outstanding/useful merge requests from [perone/Pyevolve](https://github.com/perone/Pyevolve) pulled in.
* Multiprocessing is now fully featured/customizable.
* Updated dependencies and dropped support for Python <=2.6; Python 2.7+ only now (no Python 3 yet -- see https://github.com/greole/Pyevolve instead)

#### Goals
Python is slow and genetic algorithms (and programs) require immense computation. One major goal is to reimplement much of the evolving and function evaluation (i.e. GAPopulation) in Cython, as well as leveraging _compiled_ GP expressions for performance. I've benchmarked Numba/Pypy and both are promising as well -- a critical aspect is online/JIT compilation of a dynamically generated expression.

Additionally:
* Backwards compatibility with original Pyevolve repo
* Actively maintained/benchmarked/tested (add CI, coverage, perf, etc)
* Switch documentation to readthedocs.org

