Examples
============================================================================

All the examples can be download from the :ref:`download_sec` section, **they are not**
included in the installation package.

Example 1 - Simple example
---------------------------------------------------------------------------

Filename: :file:`examples/pyevolve_ex1_simple.py`

This is the Example #1, it is a very simple example: 

.. literalinclude:: ../../examples_rel_0_5/pyevolve_ex1_simple.py

Example 2 - Real numbers, Gaussian Mutator
-------------------------------------------------------------------------------

Filename: :file:`examples/pyevolve_ex2_realgauss.py`

This example uses the :func:`Initializators.G1DListInitializatorReal` initializator
and the :func:`Mutators.G1DListMutatorRealGaussian` mutator:

.. literalinclude:: ../../examples_rel_0_5/pyevolve_ex2_realgauss.py

Example 3 - Schaffer F6 deceptive function
-------------------------------------------------------------------------------

Filename: :file:`examples/pyevolve_ex3_schaffer.py`

This examples tries to minimize the Schaffer F6 function, this function is a
deceptive function, considered a GA-hard function to optimize: 

.. literalinclude:: ../../examples_rel_0_5/pyevolve_ex3_schaffer.py

Example 4 - Using Sigma truncation scaling
-------------------------------------------------------------------------------

Filename: :file:`examples/pyevolve_ex4_sigmatrunc.py`

This example shows the use of the sigma truncation scale method, it tries
to minimize a function with negative results:

.. literalinclude:: ../../examples_rel_0_5/pyevolve_ex4_sigmatrunc.py

Example 5 - Step callback function
-------------------------------------------------------------------------------

Filename: :file:`examples/pyevolve_ex5_callback.py`

This example shows the use of the :term:`step callback function`: 

.. literalinclude:: ../../examples_rel_0_5/pyevolve_ex5_callback.py


Example 6 - The DB Adapters
-------------------------------------------------------------------------------

Filename: :file:`examples/pyevolve_ex6_dbadapter.py`

This example show the use of the DB Adapters (:mod:`DBAdapters`) : 

.. literalinclude:: ../../examples_rel_0_5/pyevolve_ex6_dbadapter.py


Example 7 - The Rastringin function
-------------------------------------------------------------------------------

Filename: :file:`examples/pyevolve_ex7_rastringin.py`

This example minimizes the deceptive function Rastringin with 20 variables: 

.. literalinclude:: ../../examples_rel_0_5/pyevolve_ex7_rastringin.py


Example 8 - The Gaussian Integer Mutator
-------------------------------------------------------------------------------

Filename: :file:`examples/pyevolve_ex8_gauss_int.py`

This example shows the use of the Gaussian Integer Mutator
(:class:`Mutators.G1DListMutatorIntegerGaussian`): 

.. literalinclude:: ../../examples_rel_0_5/pyevolve_ex8_gauss_int.py

Example 9 - The 2D List genome
-------------------------------------------------------------------------------

Filename: :file:`examples/pyevolve_ex9_g2dlist.py`

This example shows the use of the 2d list genome (:class:`G2DList.G2DList`):

.. literalinclude:: ../../examples_rel_0_5/pyevolve_ex9_g2dlist.py

Example 10 - The 1D Binary String
-------------------------------------------------------------------------------

Filename: :file:`examples/pyevolve_ex10_g1dbinstr.py`

This example shows the use of the 1D Binary String genome: 

.. literalinclude:: ../../examples_rel_0_5/pyevolve_ex10_g1dbinstr.py

Example 11 - The use of alleles
-------------------------------------------------------------------------------

Filename: :file:`examples/pyevolve_ex11_allele.py`

This example shows the use of alleles: 

.. literalinclude:: ../../examples_rel_0_5/pyevolve_ex11_allele.py

Example 12 - The Travelling Salesman Problem (TSP)
-------------------------------------------------------------------------------

Filename: :file:`examples/pyevolve_ex12_tsp.py`

This example shows the use of Pyevolve to solve the `TSP <http://en.wikipedia.org/wiki/Traveling_salesman_problem>`_:

.. literalinclude:: ../../examples_rel_0_5/pyevolve_ex12_tsp.py

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

.. literalinclude:: ../../examples_rel_0_5/pyevolve_ex13_sphere.py

Example 14 - The Ackley function
-------------------------------------------------------------------------------

Filename: :file:`examples/pyevolve_ex14_ackley.py`

This example minimizes the Ackley F1 function, a deceptive function: 

.. literalinclude:: ../../examples_rel_0_5/pyevolve_ex14_ackley.py

Example 15 - The Rosenbrock function
-------------------------------------------------------------------------------

Filename: :file:`examples/pyevolve_ex15_rosenbrock.py`

This example minimizes the Rosenbrock function, another deceptive function: 

.. literalinclude:: ../../examples_rel_0_5/pyevolve_ex15_rosenbrock.py

