from pyevolve import G2DList
from pyevolve import GSimpleGA
from pyevolve import Selectors
from pyevolve import Crossovers
from pyevolve import Mutators

# This function is the evaluation function, we want
# to give high score to more zero'ed chromosomes
def eval_func(chromosome):
   score = 0.0

   # iterate over the chromosome
   for i in xrange(chromosome.getHeight()):
      for j in xrange(chromosome.getWidth()):
         # You can use the chromosome.getItem(i, j)
         if chromosome[i][j]==0:
            score += 0.1
   return score

# Genome instance
genome = G2DList.G2DList(8, 5)
genome.setParams(rangemin=0, rangemax=10)

# The evaluator function (objective function)
genome.evaluator.set(eval_func)
genome.crossover.set(Crossovers.G2DListCrossoverSingleHPoint)
genome.mutator.set(Mutators.G2DListMutatorIntegerGaussian)

# Genetic Algorithm Instance
ga = GSimpleGA.GSimpleGA(genome)
ga.selector.set(Selectors.GRouletteWheel)
ga.setGenerations(1200)

# Do the evolution, with stats dump
# frequency of 10 generations
ga.evolve(freq_stats=100)

# Best individual
print ga.bestIndividual()
