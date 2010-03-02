from pyevolve import G1DList
from pyevolve import GSimpleGA
from pyevolve import Selectors
from pyevolve import Statistics
from pyevolve import DBAdapters
from pyevolve import Migration
from pyevolve import Util
import pyevolve
import cPickle
import zlib


def eval_func(chromosome):
   score = 0.0
   for value in chromosome:
      if value==0:
         score += 1
  
   return score

if __name__ == "__main__":
   genome = G1DList.G1DList(800)
   genome.setParams(rangemin=0, rangemax=10)
   genome.evaluator.set(eval_func)
   ga = GSimpleGA.GSimpleGA(genome)
   ga.selector.set(Selectors.GRouletteWheel)
   ga.setGenerations(8000000)

   mig = Migration.WANMigration("192.168.0.1", 666, "group_ex1_simple")
   topology = Util.Graph()
   topology.addEdge(("192.168.0.1", 666), ("192.168.0.10", 666))
   mig.setTopology(topology)

   ga.setMigrationAdapter(mig)

   ga(freq_stats=10)
   best = ga.bestIndividual()
