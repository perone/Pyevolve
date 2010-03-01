Examples
============================================================================

All the examples can be download from the :ref:`download_sec` section, **they are not**
included in the installation package.

Example 1 - Simple example
---------------------------------------------------------------------------

Filename: :file:`examples/pyevolve_ex1_simple.py`

This is the Example #1, it is a very simple example: 

.. literalinclude:: ../../examples/pyevolve_ex1_simple.py

Example 2 - Real numbers, Gaussian Mutator
-------------------------------------------------------------------------------

Filename: :file:`examples/pyevolve_ex2_realgauss.py`

This example uses the :func:`Initializators.G1DListInitializatorReal` initializator
and the :func:`Mutators.G1DListMutatorRealGaussian` mutator:

.. literalinclude:: ../../examples/pyevolve_ex2_realgauss.py

Example 3 - Schaffer F6 deceptive function
-------------------------------------------------------------------------------

Filename: :file:`examples/pyevolve_ex3_schaffer.py`

This examples tries to minimize the Schaffer F6 function, this function is a
deceptive function, considered a GA-hard function to optimize: 

.. literalinclude:: ../../examples/pyevolve_ex3_schaffer.py

Example 4 - Using Sigma truncation scaling
-------------------------------------------------------------------------------

Filename: :file:`examples/pyevolve_ex4_sigmatrunc.py`

This example shows the use of the sigma truncation scale method, it tries
to minimize a function with negative results:

.. literalinclude:: ../../examples/pyevolve_ex4_sigmatrunc.py

Example 5 - Step callback function
-------------------------------------------------------------------------------

Filename: :file:`examples/pyevolve_ex5_callback.py`

This example shows the use of the :term:`step callback function`: 

.. literalinclude:: ../../examples/pyevolve_ex5_callback.py


Example 6 - The DB Adapters
-------------------------------------------------------------------------------

Filename: :file:`examples/pyevolve_ex6_dbadapter.py`

This example show the use of the DB Adapters (:mod:`DBAdapters`) : 

.. literalinclude:: ../../examples/pyevolve_ex6_dbadapter.py


Example 7 - The Rastrigin function
-------------------------------------------------------------------------------

Filename: :file:`examples/pyevolve_ex7_rastrigin.py`

This example minimizes the deceptive function Rastrigin with 20 variables: 

.. literalinclude:: ../../examples/pyevolve_ex7_rastrigin.py


Example 8 - The Gaussian Integer Mutator
-------------------------------------------------------------------------------

Filename: :file:`examples/pyevolve_ex8_gauss_int.py`

This example shows the use of the Gaussian Integer Mutator
(:class:`Mutators.G1DListMutatorIntegerGaussian`): 

.. literalinclude:: ../../examples/pyevolve_ex8_gauss_int.py

Example 9 - The 2D List genome
-------------------------------------------------------------------------------

Filename: :file:`examples/pyevolve_ex9_g2dlist.py`

This example shows the use of the 2d list genome (:class:`G2DList.G2DList`):

.. literalinclude:: ../../examples/pyevolve_ex9_g2dlist.py

Example 10 - The 1D Binary String
-------------------------------------------------------------------------------

Filename: :file:`examples/pyevolve_ex10_g1dbinstr.py`

This example shows the use of the 1D Binary String genome: 

.. literalinclude:: ../../examples/pyevolve_ex10_g1dbinstr.py

Example 11 - The use of alleles
-------------------------------------------------------------------------------

Filename: :file:`examples/pyevolve_ex11_allele.py`

This example shows the use of alleles: 

.. literalinclude:: ../../examples/pyevolve_ex11_allele.py

Example 12 - The Travelling Salesman Problem (TSP)
-------------------------------------------------------------------------------

Filename: :file:`examples/pyevolve_ex12_tsp.py`

This example shows the use of Pyevolve to solve the `TSP <http://en.wikipedia.org/wiki/Traveling_salesman_problem>`_:

.. literalinclude:: ../../examples/pyevolve_ex12_tsp.py

This example will plot a file called :file:`tsp_result.png` in the same
directory of the execution, this image will be the best result of the
TSP, it looks like:

   .. image:: imgs/ex_12_tsp_result.png
      :align: center

To plot this image, you will need the Python Imaging Library (PIL).

.. seealso::

   `Python Imaging Library (PIL) <http://www.pythonware.com/products/pil/>`_
      The Python Imaging Library (PIL) adds image processing capabilities to your
      Python interpreter. This library supports many file formats, and provides
      powerful image processing and graphics capabilities.

Example 13 - The sphere function
-------------------------------------------------------------------------------

Filename: :file:`examples/pyevolve_ex13_sphere.py`

This is the GA to solve the sphere function: 

.. literalinclude:: ../../examples/pyevolve_ex13_sphere.py

Example 14 - The Ackley function
-------------------------------------------------------------------------------

Filename: :file:`examples/pyevolve_ex14_ackley.py`

This example minimizes the Ackley F1 function, a deceptive function: 

.. literalinclude:: ../../examples/pyevolve_ex14_ackley.py

Example 15 - The Rosenbrock function
-------------------------------------------------------------------------------

Filename: :file:`examples/pyevolve_ex15_rosenbrock.py`

This example minimizes the Rosenbrock function, another deceptive function: 

.. literalinclude:: ../../examples/pyevolve_ex15_rosenbrock.py

Example 16 - The 2D Binary String
-------------------------------------------------------------------------------

Filename: :file:`examples/pyevolve_ex16_g2dbinstr.py`

This example shows the use of the 2D Binary String genome: 

.. literalinclude:: ../../examples/pyevolve_ex16_g2dbinstr.py

Example 17 - The Tree genome example
-------------------------------------------------------------------------------

Filename: :file:`examples/pyevolve_ex17_gtree.py`

This example shows the use of the Tree genome: 

.. literalinclude:: ../../examples/pyevolve_ex17_gtree.py

.. _pyevolve-example18:

Example 18 - The Genetic Programming example
-------------------------------------------------------------------------------

Filename: :file:`examples/pyevolve_ex18_gp.py`

This example shows the use of the GTreeGP genome (for Genetic Programming): 

.. literalinclude:: ../../examples/pyevolve_ex18_gp.py

Example 21 - The n-queens problem (64x64 chess board)
-------------------------------------------------------------------------------

Filename: :file:`examples/pyevolve_ex21_nqueens.py`

This example shows the use of GA to solve the n-queens problem for a 
chess board of size 64x64: 

.. literalinclude:: ../../examples/pyevolve_ex21_nqueens.py


Example 22 - The Infinite Monkey Theorem
-------------------------------------------------------------------------------

Filename: :file:`examples/pyevolve_ex22_monkey.py`

This example was a kindly contribution by Jelle Feringa, it shows the
`Infinite Monkey Theorem <http://en.wikipedia.org/wiki/Infinite_monkey_theorem>`_:

.. literalinclude:: ../../examples/pyevolve_ex22_monkey.py

