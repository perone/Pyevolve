"""

:mod:`Interaction` -- interaction module
==========================================================================

In this module, you will find the funcionality for the :term:`Interactive mode`.
When you enter in the Interactive Mode, Pyevolve will automatic import this module
and exposes to you in the name space called "it".

To use this mode, the parameter *interactiveMode* must be enabled in the
:class:`GSimpleGA.GSimpleGA`.

You can use the manual method to enter in the Interactive Mode at specific
generation using the :meth:`GSimpleGA.GSimpleGA.setInteractiveGeneration` method.

"""
import logging

try:
   import pylab
except:
   logging.debug("cannot import Matplotlib ! Plots will not be available !")
   print "Warning: cannot import Matplotlib ! Plots will not be available !"

try:
   import numpy
except:
   logging.debug("cannot import Numpy ! Some functions will not be available !")
   print "Warning: cannot import Numpy ! Some functions will not be available !"

def getPopScores(population, fitness=False):
   """ Returns a list of population scores

   Example:
      >>> lst = Interaction.getPopScores(population)

   :param population: population object (:class:`GPopulation.GPopulation`)
   :param fitness: if is True, the fitness score will be used, otherwise, the raw.
   :rtype: list of population scores

   """
   score_list = []
   for individual in population:
      score_list.append(individual.fitness if fitness else individual.score)
   return score_list

def plotPopScore(population, fitness=False):
   """ Plot the population score distribution 

   Example:
      >>> Interaction.plotPopScore(population)

   :param population: population object (:class:`GPopulation.GPopulation`)
   :param fitness: if is True, the fitness score will be used, otherwise, the raw.
   :rtype: None

   """
   score_list = getPopScores(population, fitness)
   pylab.plot(score_list, 'o')
   pylab.title("Plot of population score distribution")
   pylab.xlabel('Individual')
   pylab.ylabel('Score')
   pylab.grid(True)
   pylab.show()

def plotHistPopScore(population, fitness=False):
   """ Population score distribution histogram 

   Example:
      >>> Interaction.plotHistPopScore(population)

   :param population: population object (:class:`GPopulation.GPopulation`)
   :param fitness: if is True, the fitness score will be used, otherwise, the raw.
   :rtype: None
   
   """
   score_list = getPopScores(population, fitness)
   n, bins, patches = pylab.hist(score_list, 50, facecolor='green', alpha=0.75, normed=1)
   pylab.plot(bins, pylab.normpdf(bins, numpy.mean(score_list), numpy.std(score_list)), 'r--')
   pylab.xlabel('Score')
   pylab.ylabel('Frequency')
   pylab.grid(True)
   pylab.title("Plot of population score distribution")
   pylab.show()

