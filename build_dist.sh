#!/bin/sh
python setup.py build
python setup.py bdist_wininst --target-version="2.5"
python setup.py bdist_wininst --target-version="2.6"
python setup.py sdist
python setup.py bdist
python setup.py bdist_egg

