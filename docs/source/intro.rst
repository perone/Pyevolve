
Introduction
============================================================

This is the documentation of the Pyevolve release |release|. Since the version 0.5, Pyevolve has changed in many aspects, many new features was added and **many** bugs was fixed, this documentation describes those changes, the new API and new features.

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

* `Python 2.5+, v.2.6 is recommended <http://www.python.org>`_

* **Optional, for graph plotting**: `Matplotlib 0.98.4+ <http://matplotlib.sourceforge.net/>`_
     The matplotlib [#matplotlib]_ is required to plot the graphs.

* **Optional, for real-time statistics visualization**: `VPython <http://vpython.org/index.html>`_
     The VPython [#vvpython]_ is required to see real-time statistics visualization.

* **Optional, for drawing GP Trees**: `Pydot 1.0.2+ <http://code.google.com/p/pydot/>`_
     The Pydot [#pydot]_ is used to plot the Genetic Programming Trees.

* **Optional, for MySQL DB Adapter**: `MySQL for Python <http://sourceforge.net/projects/mysql-python/>`_
     The MySQL [#mysqldb]_ is used by the MySQL DB Adapter.

.. rubric:: Footnotes

.. [#matplotlib] Matplotlib is Copyright (c) 2002-2008 John D. Hunter; All Rights Reserved
.. [#vvpython] VPython was originated by David Scherer in 2000.
.. [#pydot] Pydot was developed by Ero Carrera.
.. [#mysqldb] MySQLdb was developed by Andy Dustman and contributors.

.. _download_sec:

Downloads
----------------------------------------------

Windows
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ 

Installers for Microsoft Windows platform:

`Pyevolve <http://pyevolve.sourceforge.net/distribution/0_6rc1/Pyevolve-0.6rc1.win32-py2.5.exe>`__ v.\ |release| (*installer*) for Python 2.5
   *This is an .exe installer for Microsoft Windows XP/Vista*

`Pyevolve <http://pyevolve.sourceforge.net/distribution/0_6rc1/Pyevolve-0.6rc1.win32-py2.6.exe>`__ v.\ |release| (*installer*) for Python 2.6
   *This is an .exe installer for Microsoft Windows XP/Vista*

`Pyevolve <http://pyevolve.sourceforge.net/distribution/0_6rc1/Pyevolve-0.6rc1.tar.gz>`__ v.\ |release| (*source code*) for Python 2.x
   *This is the source code*

Linux
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ 

Installation package for Linux platform:

`Pyevolve <http://pyevolve.sourceforge.net/distribution/0_6rc1/Pyevolve-0.6rc1.tar.gz>`__ v.\ |release| (*source code*) for Python 2.x
   *This is the source code*

Examples package
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ 

Examples package for Pyevolve v.\ |release|:

`Pyevolve examples <http://pyevolve.sourceforge.net/distribution/0_6rc1/Pyevolve-0.6rc1-examples.zip>`__ v.\ |release| (*examples*)
   *This is an package with the Pyevolve source code*


Installation
-----------------------------------

You can download the specific Pyevolve from the :ref:`download_sec` section, or using *easy_install*.

The installation can be easy done by using the *easy_install*: ::
   
   easy_install pyevolve

You can upgrade your older version too: ::

   easy_install --upgrade pyevolve


or install a downloaded *egg package*: ::
   
   easy_install /downloads/downloaded_package.egg

or install from an URL: ::

   easy_install http://site/package.egg

This command will automatic search, download and install a suitable version of pyevolve, once you have installed, you can test: ::

   >>> import pyevolve
   >>> print pyevolve.__version__
   'v.0.6rc1'

*easy_install* utility is part of `setuptools <http://pypi.python.org/pypi/setuptools>`_. Once you have installed setuptools, you will find the easy_install.exe program in your Python Scripts subdirectory.


Genetic Algorithm Features
-----------------------------------

**Chromosomes / Representations**
   **1D List**, **2D List**, **1D Binary String**, **2D Binary String** and **Tree**

   .. note:: it is important to note, that the 1D List, 2D List and Tree can carry
             any type of python objects or primitives.
   
**Crossover Methods**

   **1D Binary String**
      Single Point Crossover, Two Point Crossover, Uniform Crossover

   **1D List** 
      Single Point Crossover, Two Point Crossover, Uniform Crossover, OX Crossover, Edge Recombination
      Crossover, Cut and Crossfill Crossover, Real SBX Crossover

   **2D List**
      Uniform Crossover, Single Vertical Point Crossover, Single Horizontal Point Crossover

   **2D Binary String**
      Uniform Crossover, Single Vertical Point Crossover, Single Horizontal Point Crossover

   **Tree**
      Single Point Crossover, Strict Single Point Crossover

**Mutator Methods**

   **1D Binary String**
      Swap Mutator, Flip Mutator

   **2D Binary String**
      Swap Mutator, Flip Mutator

   **1D List**
      Swap Mutator, Integer Range Mutator, Real Range Mutator, Integer Gaussian Mutator,
      Real Gaussian Mutator, Integer Binary Mutator, Allele Mutator, Simple Inversion Mutator

   **2D List**
      Swap Mutator, Integer Gaussian Mutator, Real Gaussian Mutator, Allele Mutator,
      Integer Range Mutator

   **Tree**
      Swap Mutator, Integer Range Mutator, Real Range Mutator, Integer Gaussian Mutator,
      Real Gaussian Mutator

**Initializators**

   **1D Binary String**
      Binary String Initializator

   **2D Binary String**
      Binary String Initializator

   **1D List**
      Allele Initializator, Integer Initializator, Real Initializator

   **2D List**
      Allele Initializator, Integer Initializator, Real Initializator

   **Tree**
      Integer Initializator, Allele Initializator

**Scaling Methods**

   Linear Scaling, Sigma Truncation Scaling and Power Law Scaling, Raw Scaling,
   Boltzmann Scaling, Exponential Scaling, Saturated Scaling

**Selection Methods**

   Rank Selection, Uniform Selection, Tournament Selection, Tournament Selection
   Alternative (doesn't uses the Roulette Wheel), Roulette Wheel Selection


Genetic Programming Features
-----------------------------------

**Chromosomes / Representations**

   **Tree**

   .. warning:: the Tree of Genetic Programming is the class :class:`GTree.GTreeGP`
                and not the :class:`GTree.GTree` class of the Genetic Algorithm representation.
   
**Crossover Methods**

   **Tree**
      Single Point Crossover

**Mutator Methods**

   **Tree**
      Operation Mutator, Subtree mutator
      
**Initializators**

   **Tree**
      Grow Initializator, Full Initializator, Ramped Half-n-Half

**Scaling Methods**

   Linear Scaling, Sigma Truncation Scaling and Power Law Scaling, Raw Scaling,
   Boltzmann Scaling, Exponential Scaling, Saturated Scaling

**Selection Methods**

   Rank Selection, Uniform Selection, Tournament Selection, Tournament Selection
   Alternative (doesn't uses the Roulette Wheel), Roulette Wheel Selection


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


Genetic Programming Literature
------------------------------------

In this section, you will find study material to learn more about Genetic Programming.

Books
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Poli, Riccardo; Langdon, William B.; McPhee, Nicholas F.**, *A Field Guide to Genetic Programming*,
this book is also available online (a GREAT initiative from authors) in `Book Site <http://www.gp-field-guide.org.uk/>`_

**Koza, John R.**, *Genetic Programming: On the Programming of Computers by Means of Natural Selection*, MIT Press, 1992.

.. seealso::

   `Wikipedia: Genetic Programming <http://en.wikipedia.org/wiki/Genetic_programming>`_
      The Wikipedia article about Genetic Programming.

Sites
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

`Introduction to Genetic Programming <http://www.genetic-programming.org/>`_
   A nice collection of GP related content !

`A Field Guide to Genetic Programming <http://www.gp-field-guide.org.uk/p>`_
   A book, freely downloadable under a Creative Commons license.

`The Genetic Programming Bibliography <http://www.cs.bham.ac.uk/~wbl/biblio/README.html>`_
   A very interesting initiative mantained by William Langdon, Steven Gustafson, and John Koza.
   Over than 6000 GP references !


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

   Data Type Independent
      When a genetic operator is data type idependent, it will operates on different 
      data types but not with different chromosome representation, for example, the
      :func:`Mutators.G1DListMutatorSwap` mutator will operate on Real, Allele or
      Integer :class:`G1DList.G1DList` chromosome, but not on :class:`G2DList.G2DList`
      chromosome.


   Standardized Fitness
      The standardized fitness restates the raw score so that a lower numerical value is
      always a better value. 

      .. seealso::

         `Genetic Programming: On the Programming of Computers by Means of Natural Selection <http://www.amazon.com/Genetic-Programming-Computers-Selection-Adaptive/dp/0262111705>`_
            A book from John R. Koza about Genetic Programming.


   Adjusted Fitness
      The adjusted fitness is a measure computed from the Standardized Fitness, the Adjusted Fitness is always
      between 0 and 1 and it's always bigger for better individuals.

      .. seealso::

         `Genetic Programming: On the Programming of Computers by Means of Natural Selection <http://www.amazon.com/Genetic-Programming-Computers-Selection-Adaptive/dp/0262111705>`_
            A book from John R. Koza about Genetic Programming.

   Non-terminal node
      The non-terminal node or non-terminal function is a function in a parse tree which is either a root
      or a branch in that tree, in the GP we call non-terminal nodes as "functions", the opposite of
      terminal nodes, which are the variables of the GP.

.. seealso::

   `Wikipedia: Genetic Algorithm <http://en.wikipedia.org/wiki/Genetic_algorithm>`_
      An article talking about Genetic Algorithms.

   `Wikipedia: Genetic Programming <http://en.wikipedia.org/wiki/Genetic_programming>`_
      The Wikipedia article about Genetic Programming.


Other platforms and performance
============================================================

Running Pyevolve on Symbian OS (PyS60)
---------------------------------------------------------------------------
Pyevolve is compatible with PyS60 2.0 (but older versions of the 1.9.x trunk should work fine too); PyS60 
2.0 is a port of Python 2.5.4 core to the S60 smartphones, it was made by Nokia and it's Open Source.
All smartphones based on the `S60 2nd and 3rd editions <http://en.wikipedia.org/wiki/Nokia_S60_and_Symbian_OS#S60_editions>`_
should run PyS60, you can download it from the `Maemo garage project home <https://garage.maemo.org/projects/pys60/>`_.

To install Pyevolve in PyS60 you simple need to copy the "pyevolve" package (you can use the sources of Pyevolve
or even the "pyevolve" of your Python installation to the smartphone in a place that PyS60 can find it, usually
in :file:`c:\\resource\\Python25`, for more information read the PyS60 documentation. The Genetic Algorithms and the
Genetic Programming cores of Pyevolve was tested with PyS60 2.0, but to use Genetic Programming, you must
define explicitly the funtions of the GP, like in :ref:`snippet_gp_explicit`.

Of course not all features of Pyevolve are supported in PyS60, like for example some DBAdapters and the graphical
plotting tool, since no matplotlib port is available to PyS60 at the moment. Pyevolve was tested with PyS60 2.0
in a Nokia N78 and in a Nokia N73 smartphones.

.. seealso::

   `Croozeus.com -  home to PyS60 developers <http://croozeus.com/>`_
      A lot of information and tutorials about PyS60, very recommended.

   `Python for S60 - OpenSource <http://wiki.opensource.nokia.com/projects/PyS60>`_
      The PyS60 project wiki.

Running Pyevolve on Jython
---------------------------------------------------------------------------
Jython is an implementation of Python language and it's modules (not all unfortunatelly) which
is designed to run over the Java platform.
Pyevolve was tested against Jython 2.5.x and worked well, except for the Genetic Programming
core which is taking a lot of memory, maybe a Jython issue with the Java JVM.

You're highly encouraged to run Jython with the JVM "-server" option; this option will enable
anoter VM JIT which is optimal for applications where the fast startup times isn't important,
and the overall performance is what matters. This JIT of the "Server mode" has different
policies to compile your code into native code, and it's well designed for long running
applications, where the VM can profile and optimize better than the JIT of "Client mode".

Pyevolve was tested against Jython 2.5.1 in Java v.1.6.0_18
Java(TM) SE Runtime Environment (build 1.6.0_18-b07)
Java HotSpot(TM) Client VM (build 16.0-b13, mixed mode, sharing)

.. seealso::

   `Jython <http://www.jython.org/>`_
      Official Jython project home.

   `Java HotSpot <http://java.sun.com/products/hotspot/whitepaper.html#1>`_
      The Java HotSpot Performance Engine Architecture.


Running Pyevolve on IronPython
---------------------------------------------------------------------------
IronPython is an open-source implementation of the Python programming language targeting
the .NET Framework and Mono, written entirely in C# and created by Jim Hugunin.
IronPython is currently language-compatible with Python 2.6.

Pyevolve was tested against the IronPython 2.6 (2.6.10920.0) in a Windows XP SP3
with .NET 2.0.50727.3603.

.. seealso::

   `Official IronPython project home <http://www.ironpython.net>`_
      Official IronPython project home.

   `Differences between IronPython and CPython <http://ironpython.codeplex.com/wikipage?title=Differences>`_
      Documents with differences between IronPython and CPython (the official Python interepreter).

   `IronPython performance benchmarks <http://ironpython.codeplex.com/wikipage?title=IP26RC1VsCPy26Perf&referringTitle=Home&ProjectName=ironpython>`_
      A lot of benchmarks and comparisons between IronPython and CPython.

	  
Running Pyevolve on iPod/iPhone
---------------------------------------------------------------------------
The Genetic Algorithm core of Pyevolve was tested on iPod Touch 2G with the
firmware v.3.1.2. To use it, you first must install the port of Python 2.5+ to the
OS of iPod. You just need to put the Pyevolve package inside the directory where
you'll call your application or just put it inside another place where the Python
from iPod/iPhone can found in path.
	  
.. seealso::

	`Miniguide to install Python on iPhone <http://coding.derkeiler.com/Archive/Python/comp.lang.python/2008-11/msg00252.html>`_
		Miniguide on how to install Python on iPhone

		
Improving Pyevolve performance
---------------------------------------------------------------------------
Pyevolve, at least for the versions <= 0.6, have all modules written in pure Python, which enables some
very useful features and portability, but sometimes weights in performance. Here are some
ways users and developers uses to increase the performance of Pyevolve:

   **Psyco**
      Psyco is the well know Python specializing compiled, created by Armin Rigo. Psyco
      is very easy to use and can give you a lot of speed up.

   **Cython**
      Cython is a specific language used to create C/C++ extensions for Python, it is based
      on the Python language itself, so if you think Psyco is not enought or aren't giving
      too much optimizations, you can use Cython to create your own C/C++ extensions; the
      best approach is to use Cython to build your :term:`Evaluation function`, which is
      usually the most consuming part of Genetic Algorithms.

.. seealso::

   `Psyco at Sourceforge.net <http://psyco.sourceforge.net/>`_
      The official site of Psyco at Sourceforge.net

   `Psyco 2.0 binaries for Windows <http://www.voidspace.org.uk/python/modules.shtml#psyco>`_
      Development of psyco was recently done by Christian Tismer. Here you'll find the
      binaries of Psyco 2.0 (Python 2.4, 2.5 and 2.6) for Windows.

   `Cython - C-Extensions for Python <http://www.cython.org/>`_
      Official Cython project home.
