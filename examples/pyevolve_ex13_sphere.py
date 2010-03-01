from pyevolve import G1DList
from pyevolve import Mutators, Initializators
from pyevolve import GSimpleGA, Consts

# This is the Sphere Function
def sphere(xlist):
   total = 0
   for i in xlist:
      total += i**2
   return total

def run_main():
   genome = G1DList.G1DList(140)
   genome.setParams(rangemin=-5.12, rangemax=5.13)
   genome.initializator.set(Initializators.G1DListInitializatorReal)
   genome.mutator.set(Mutators.G1DListMutatorRealGaussian)
   genome.evaluator.set(sphere)

   ga = GSimpleGA.GSimpleGA(genome, seed=666)
   ga.setMinimax(Consts.minimaxType["minimize"])
   ga.setGenerations(1500)
   ga.setMutationRate(0.01)
   ga.evolve(freq_stats=500)

   best = ga.bestIndividual()

if __name__ == "__main__":
   run_main()
   

