from pyevolve import GSimpleGA
from pyevolve import GTree
from pyevolve import Consts
from pyevolve import Selectors
from pyevolve import Mutators
from math import sqrt
import pydot   
import random

def gp_add(a, b):
   assert len(a)==len(b)
   new_list = [x+y for x,y in zip(a,b)]
   return new_list

#def gp_sub(a, b):
#   assert len(a)==len(b)
#   new_list = [x-y for x,y in zip(a,b)]
#   return new_list

def prot_div(a, b):
   if b==0:
      return b
   else:
      return a/b

#def gp_div(a,b):
#   assert len(a)==len(b)
#   new_list = [prot_div(x,float(y)) for x,y in zip(a,b)]
#   return new_list

def gp_mul(a,b):
   assert len(a)==len(b)
   new_list = [x*y for x,y in zip(a,b)]
   return new_list

def random_lists(size):
   list_a = [random.randint(1,20) for i in xrange(size)]
   list_b = [random.randint(1,20) for i in xrange(size)]

   return (list_a, list_b)
   

def eval_func(chromosome):
   sz = 20
   code_comp     = chromosome.getCompiledCode()
   square_accum  = 0.0

   for j in xrange(sz):
         a, b = random_lists(5)
         target_list   = gp_add(gp_mul(a,b),gp_mul(a,b))
         ret_list      = eval(code_comp)
         square_accum += (sum(target_list)-sum(ret_list))**2

   RMSE = sqrt(square_accum / float(sz))
   score = (1.0 / (RMSE+1.0))
   return score

def main_run():
   genome = GTree.GTreeGP()
   root   = GTree.GTreeNodeGP('a', Consts.nodeType["TERMINAL"])
   genome.setRoot(root)

   genome.setParams(max_depth=2, method="ramped")
   genome.evaluator += eval_func
   genome.mutator.set(Mutators.GTreeGPMutatorSubtree)

   ga = GSimpleGA.GSimpleGA(genome)
   ga.setParams(gp_terminals       = ['a', 'b'],
                gp_function_prefix = "gp")

   ga.setMinimax(Consts.minimaxType["maximize"])
   ga.setGenerations(500)
   ga.setCrossoverRate(1.0)
   ga.setMutationRate(0.08)
   ga.setPopulationSize(80)
   
   ga(freq_stats=1)
   print ga.bestIndividual()

   graph = pydot.Dot()
   ga.bestIndividual().writeDotGraph(graph)
   graph.write_jpeg('tree.png', prog='dot')

if __name__ == "__main__":
   main_run()
   #import hotshot, hotshot.stats
   #prof = hotshot.Profile("ev.prof")
   #prof.runcall(main_run)
   #prof.close()
   #stats = hotshot.stats.load("ev.prof")
   #stats.strip_dirs()
   #stats.sort_stats('time', 'calls')
   #stats.print_stats(20)

