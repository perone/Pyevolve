Running Pyevolve tests
======================

1. Install appropriate packages with::

    pip install -r requirements_test.txt
2. Run tests with coverage::

    coverage run runtests.py
3. Create coverage report and it's html presentation::

    coverage report -m
    coverage html
4. Now you can find report in `htmlcov/index.html`
