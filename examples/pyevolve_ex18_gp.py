from pyevolve import Util
from pyevolve import GTree
from pyevolve import GSimpleGA
from pyevolve import Consts
import math

rmse_accum = Util.ErrorAccumulator()

def gp_add(a, b): return a+b
def gp_sub(a, b): return a-b
def gp_mul(a, b): return a*b
def gp_sqrt(a):   return math.sqrt(abs(a))
   
def eval_func(chromosome):
   global rmse_accum
   rmse_accum.reset()
   code_comp = chromosome.getCompiledCode()
   
   for a in xrange(0, 5):
      for b in xrange(0, 5):
         evaluated     = eval(code_comp)
         target        = math.sqrt((a*a)+(b*b))
         rmse_accum   += (target, evaluated)

   return rmse_accum.getRMSE()

def main_run():
   genome = GTree.GTreeGP()
   genome.setParams(max_depth=4, method="ramped")
   genome.evaluator += eval_func

   ga = GSimpleGA.GSimpleGA(genome)
   ga.setParams(gp_terminals       = ['a', 'b'],
                gp_function_prefix = "gp")

   ga.setMinimax(Consts.minimaxType["minimize"])
   ga.setGenerations(50)
   ga.setCrossoverRate(1.0)
   ga.setMutationRate(0.25)
   ga.setPopulationSize(800)
   
   ga(freq_stats=10)
   best = ga.bestIndividual()
   print best

if __name__ == "__main__":
   main_run()
