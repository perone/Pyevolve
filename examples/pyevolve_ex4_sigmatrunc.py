from pyevolve import G1DList
from pyevolve import GSimpleGA
from pyevolve import Selectors
from pyevolve import Initializators, Mutators
from pyevolve import Scaling
from pyevolve import Consts
import math

def eval_func(ind):
    score = 0.0
    var_x = ind[0]
    var_z = var_x**2+2*var_x+1*math.cos(var_x)
    return var_z

def run_main():
    # Genome instance
    genome = G1DList.G1DList(1)
    genome.setParams(rangemin=-60.0, rangemax=60.0)

    # Change the initializator to Real values
    genome.initializator.set(Initializators.G1DListInitializatorReal)

    # Change the mutator to Gaussian Mutator
    genome.mutator.set(Mutators.G1DListMutatorRealGaussian)

    # Removes the default crossover
    genome.crossover.clear()

    # The evaluator function (objective function)
    genome.evaluator.set(eval_func)

    # Genetic Algorithm Instance
    ga = GSimpleGA.GSimpleGA(genome)
    ga.setMinimax(Consts.minimaxType["minimize"])

    pop = ga.getPopulation()
    pop.scaleMethod.set(Scaling.SigmaTruncScaling)

    ga.selector.set(Selectors.GRouletteWheel)
    ga.setGenerations(100)

    # Do the evolution
    ga.evolve(10)

    # Best individual
    print ga.bestIndividual()

if __name__ == "__main__":
    run_main()
