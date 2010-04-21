from pyevolve import GSimpleGA
from pyevolve import GTree
from pyevolve import Crossovers
from pyevolve import Mutators
import time
import random

def eval_func(chromosome):
   score = 0.0
   # If you want to add score values based
   # in the height of the Tree, the extra
   # code is commented.

   #height = chromosome.getHeight()

   for node in chromosome:
      score += (100 - node.getData())*0.1

   #if height <= chromosome.getParam("max_depth"):
   #   score += (score*0.8)

   return score

def run_main():
   genome = GTree.GTree()
   root = GTree.GTreeNode(2)
   genome.setRoot(root)
   genome.processNodes()

   genome.setParams(max_depth=3, max_siblings=2, method="grow")
   genome.evaluator.set(eval_func)
   genome.crossover.set(Crossovers.GTreeCrossoverSinglePointStrict)

   ga = GSimpleGA.GSimpleGA(genome)
   ga.setGenerations(100)
   ga.setMutationRate(0.05)
   
   ga.evolve(freq_stats=10)
   print ga.bestIndividual()

if __name__ == "__main__":
   run_main()

  
