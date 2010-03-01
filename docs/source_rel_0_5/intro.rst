
Introduction
============================================================

This is the documentation of the Pyevolve release |release|. Since the version 0.4, Pyevolve has changed too much, many new features was added and **many** bugs was fixed, this documentation describes those changes, the new API and new features.

Pyevolve was developed to be a *complete genetic algorithm framework written in pure python*, the main objectives of Pyevolve is:

* **written in pure python**, to maximize the cross-platform issue;
* **easy to use API**, the API must be easy for end-user;
* **see the evolution**, the user can and must see and *interact* with the evolution statistics, *graphs* and etc;
* **extensible**, the API must be extensible, the user can create new representations, genetic operators like crossover, mutation and etc;
* **fast**, the design must be optimized for performance;
* **common features**, the framework must implement the most common features: selectors like roulette wheel, tournament, ranking, uniform. Scaling schemes like linear scaling, etc;
* **default parameters**, we must have default operators, settings, etc in all options;
* **open-source**, the source is for everyone, not for only one.

.. _requirements:

Requirements
-----------------------------------

Pyevolve can be executed on **Windows**, **Linux** and **Mac** platforms.

.. note:: On the Mac platform, it's reported that *Pyevolve 0.5* can't enter on the
          :term:`Interactive Mode`.

Pyevolve can be executed under `Jython 2.5b1+ <http://www.jython.org>`_, but with some restrictions:
   * You can't use some features like the *SQLite3* adapter to dump statistics and *graphs*
     (unless you install Matplotlib on Jython, but I think that still is not possible).

Pyevolve can be executed under `IronPython 2.x <http://www.codeplex.com/IronPython>`_, but with some restrictions:
   * You can't use some features like the *SQLite3* adapter to dump statistics and *graphs*
     (unless you install Matplotlib on Jython, but I think that still is not possible).
   * You must install a `zlib module <https://svn.sourceforge.net/svnroot/fepy/trunk/lib/zlib.py>`_ for IronPython.

Pyevolve requires the follow modules:

* `Python 2.5+ <http://www.python.org>`_

* **Optional, for graph plotting**: `Matplotlib 0.98.4+ <http://matplotlib.sourceforge.net/>`_
     The matplotlib [#matplotlib]_ is required to plot the graphs.

.. rubric:: Footnotes

.. [#matplotlib] Matplotlib is Copyright (c) 2002-2008 John D. Hunter; All Rights Reserved

.. _download_sec:

Downloads
----------------------------------------------

Windows
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ 

Installers for Microsoft Windows platform:

`Pyevolve v.0.5 <http://downloads.sourceforge.net/pyevolve/Pyevolve-0.5.win32-py2.5.exe?use_mirror=>`__ (*installer*) for Python 2.5
   *This is an .exe installer for Microsoft Windows XP/Vista*

`Pyevolve v.0.5 <http://downloads.sourceforge.net/pyevolve/Pyevolve-0.5.win32-py2.6.exe?use_mirror=>`__ (*installer*) for Python 2.6
   *This is an .exe installer for Microsoft Windows XP/Vista*

Linux
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ 

Installation package for Linux platform:

`Pyevolve v.0.5 <http://downloads.sourceforge.net/pyevolve/Pyevolve-0.5-py2.5.egg?use_mirror=>`__ (*egg package*) for Python 2.5
   *This is an egg package file*

`Pyevolve v.0.5 <http://downloads.sourceforge.net/pyevolve/Pyevolve-0.5-py2.6.egg?use_mirror=>`__ (*egg package*) for Python 2.6
   *This is an egg package file*


Examples and Source code 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ 

Examples and source code for Pyevolve 0.5:

`Pyevolve v.0.5 source code <http://downloads.sourceforge.net/pyevolve/Pyevolve-0.5-source.zip?use_mirror=>`__ (*package*)
   *This is an package with the Pyevolve source code*

`Examples for Pyevolve v.0.5 <http://downloads.sourceforge.net/pyevolve/ex_pyevolve0_5.zip?use_mirror=>`__ (*package*)
   *This is an package with the Pyevolve examples*



Installation
-----------------------------------

You can download the specific Pyevolve from the :ref:`download_sec` section, or using *easy_install*.

The installation can be easy done by using the *easy_install*: ::
   
   easy_install pyevolve

You can upgrade your older version too: ::

   easy_install --upgrade pyevolve


or install a downloaded *egg package*: ::
   
   easy_install /downloads/downloaded_package.egg

This command will automatic search, download and install a suitable version of pyevolve, once you have installed, you can test: ::

   >>> import pyevolve
   >>> print pyevolve.__version__
   '0.5'

*easy_install* utility is part of `setuptools <http://pypi.python.org/pypi/setuptools>`_. Once you have installed setuptools, you will find the easy_install.exe program in your Python Scripts subdirectory.

GA Features
-----------------------------------

**Chromosomes / Representations**
   **1D List**, **2D List** and the **1D Binary String**

   .. note:: it is important to note, that the 1D List and the 2D list can carry
             any type of python objects or primitives.
   
**Crossover Methods**

   **1D Binary String**
      Single Point Crossover, Two Point Crossover, Uniform Crossover

   **1D List** 
      Single Point Crossover, Two Point Crossover, Uniform Crossover, OX Crossover      

   **2D List**
      Uniform Crossover, Single Vertical Point Crossover, Single Horizontal Point Crossover

**Mutator Methods**

   **1D Binary String**
      Swap Mutator, Flip Mutator

   **1D List**
      Swap Mutator, Integer Range Mutator, Real Range Mutator, Integer Gaussian Mutator,
      Real Gaussian Mutator, Integer Binary Mutator, Allele Mutator

   **2D List**
      Swap Mutator, Integer Gaussian Mutator, Real Gaussian Mutator, Allele Mutator

**Initializators**

   **1D Binary String**
      Binary String Initializator

   **1D List**
      Allele Initializator, Integer Initializator, Real Initializator

   **2D List**
      Allele Initializator, Integer Initializator, Real Initializator

**Scaling Methods**

   Linear Scaling, Sigma Truncation Scaling and Power Law Scaling, Raw Scaling

**Selection Methods**

   Rank Selection, Uniform Selection, Tournament Selection, Roulette Wheel Selection


Genetic Algorithms Literature
------------------------------------

In this section, you will find study material to learn more about Genetic Algorithms.

Books
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Goldberg, David E (1989)**, *Genetic Algorithms in Search, Optimization and Machine Learning*, Kluwer Academic Publishers, Boston, MA.

**Goldberg, David E (2002)**, *The Design of Innovation: Lessons from and for Competent Genetic Algorithms*, Addison-Wesley, Reading, MA.

**Fogel, David B (2006)**, *Evolutionary Computation: Toward a New Philosophy of Machine Intelligence*, IEEE Press, Piscataway, NJ. Third Edition

**Holland, John H (1975)**, *Adaptation in Natural and Artificial Systems*, University of Michigan Press, Ann Arbor

**Michalewicz, Zbigniew (1999)**, *Genetic Algorithms + Data Structures = Evolution Programs*, Springer-Verlag.

.. seealso::

   `Wikipedia: Genetic Algorithms <http://en.wikipedia.org/wiki/Genetic_algorithm>`_
      The Wikipedia article about Genetic Algorithms.

Sites
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

`Introduction to Genetic Algorithms <http://www.obitko.com/tutorials/genetic-algorithms/index.php>`_
   A nice introduction by Marek Obitko.

`A Field Guide to Genetic Programming <http://www.gp-field-guide.org.uk/p>`_
   A book, freely downloadable under a Creative Commons license.

`A Genetic Algorithm Tutorial by Darrell Whitley Computer Science Department Colorado State University <http://samizdat.mines.edu/ga_tutorial/ga_tutorial.ps>`_
   An excellent tutorial with lots of theory


Glossary / Concepts
----------------------------------

.. glossary::

   Raw score
      The raw score represents the score returned by the :term:`Evaluation function`, this score
      is not scaled.

   Fitness score
      The fitness score is the scaled raw score, for example, if you use the Linear Scaling (:func:`Scaling.LinearScaling`),
      the fitness score will be the raw score scaled with the Linear Scaling method. The fitness score represents
      how good is the individual relative to our population.

   Evaluation function
      Also called *Fitness Function* or *Objective Function*, the evaluation function is the function which
      evaluates the genome, giving it a raw score. The objective of this function is to quantify the
      solutions (individuals, chromosomes)

      .. seealso::

         `Wikipedia: Fitness Function <http://en.wikipedia.org/wiki/Fitness_function>`_
            An article talking about the Evaluation function, or the "Fitness Function".

   Sample genome
      The sample genome is the genome which are used as configuration base for all the new replicated
      genomes.

   Interactive mode
      Pyevolve have an interactive mode, you can enter in this mode by pressing ESC key before the end of
      the evolution. When you press ESC, a python environment will be load. In this environment, you
      have some analysis functions and you can interact with the population of individuals at the
      specific generation.

      .. seealso::

         Module :mod:`Interaction`
            The Interaction module.

   Step callback function
      This function, when attached to the GA Engine (:class:`GSimpleGA.GSimpleGA`), will be called
      every generation. It receives one parameter, the GA Engine by itself.


.. seealso::

   `Wikipedia: Genetic Algorithm <http://en.wikipedia.org/wiki/Genetic_algorithm>`_
      An article talking about Genetic Algorithms.
