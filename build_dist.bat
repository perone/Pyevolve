@echo off
python setup.py build

python setup.py bdist_wininst --target-version="2.5"
python setup.py bdist_wininst --target-version="2.6"
python setup.py sdist --formats=gztar,zip
python setup.py bdist --formats=egg


