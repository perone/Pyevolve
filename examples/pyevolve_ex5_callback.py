# $Id: pyevolve_ex5_callback.py 151 2009-01-19 01:23:22Z christian.perone $
from pyevolve import G1DList
from pyevolve import GSimpleGA
from pyevolve import Selectors
import pyevolve

# The step callback function, this function
# will be called every step (generation) of the GA evolution
def evolve_callback(ga_engine):
   generation = ga_engine.getCurrentGeneration()
   if generation % 100 == 0:
      print "Current generation: %d" % (generation,)
      print ga_engine.getStatistics()
   return False

# This function is the evaluation function, we want
# to give high score to more zero'ed chromosomes
def eval_func(chromosome):
   score = 0.0

   # iterate over the chromosome
   for value in chromosome:
      if value==0:
         score += 0.1
   return score

# Enable the logging system
pyevolve.logEnable()

# Genome instance
genome = G1DList.G1DList(200)
genome.setParams(rangemin=0, rangemax=10)

# The evaluator function (objective function)
genome.evaluator.set(eval_func)

# Genetic Algorithm Instance
ga = GSimpleGA.GSimpleGA(genome)
ga.selector.set(Selectors.GRouletteWheel)
ga.setGenerations(800)
ga.stepCallback.set(evolve_callback)

# Do the evolution, with stats dump
# frequency of 10 generations
ga.evolve()

# Best individual
print ga.bestIndividual()
