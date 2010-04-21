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
         # You can use the chromosome.getItem(i, j) too
         if chromosome[i][j]==0:
            score += 0.1
   return score

def run_main():
   # Genome instance
   genome = G2DList.G2DList(8, 5)
   genome.setParams(rangemin=0, rangemax=100)

   # The evaluator function (objective function)
   genome.evaluator.set(eval_func)
   genome.crossover.set(Crossovers.G2DListCrossoverSingleHPoint)
   genome.mutator.set(Mutators.G2DListMutatorIntegerRange)

   # Genetic Algorithm Instance
   ga = GSimpleGA.GSimpleGA(genome)
   ga.setGenerations(800)

   # Do the evolution, with stats dump
   # frequency of 10 generations
   ga.evolve(freq_stats=100)

   # Best individual
   print ga.bestIndividual()


if __name__ == "__main__":
   run_main()
