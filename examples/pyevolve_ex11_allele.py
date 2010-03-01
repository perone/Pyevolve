from pyevolve import G1DList
from pyevolve import GSimpleGA
from pyevolve import Selectors
from pyevolve import Mutators
from pyevolve import Initializators
from pyevolve import GAllele

# This function is the evaluation function, we want
# to give high score to more zero'ed chromosomes
def eval_func(chromosome):
   score = 0.0

   # iterate over the chromosome
   for value in chromosome:
      if value == 0:
         score += 0.5
   return score

# Genome instance
setOfAlleles = GAllele.GAlleles()
for i in xrange(11):
   a = GAllele.GAlleleRange(0, i)
   setOfAlleles.add(a)

for i in xrange(11, 20):
   # You can even add an object to the list
   a = GAllele.GAlleleList(['a','b', 'xxx', 666, 0])
   setOfAlleles.add(a)
   
genome = G1DList.G1DList(20)
genome.setParams(allele=setOfAlleles)

# The evaluator function (objective function)
genome.evaluator.set(eval_func)
genome.mutator.set(Mutators.G1DListMutatorAllele)
genome.initializator.set(Initializators.G1DListInitializatorAllele)

# Genetic Algorithm Instance
ga = GSimpleGA.GSimpleGA(genome)
ga.selector.set(Selectors.GRouletteWheel)
ga.setGenerations(500)

# Do the evolution, with stats dump
# frequency of 10 generations
ga.evolve(freq_stats=50)

# Best individual
print ga.bestIndividual()
