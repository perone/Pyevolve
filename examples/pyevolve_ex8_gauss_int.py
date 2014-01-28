from pyevolve import G1DList
from pyevolve import GSimpleGA
from pyevolve import Selectors
from pyevolve import Mutators

# This function is the evaluation function, we want
# to give high score to more zero'ed chromosomes
def eval_func(chromosome):
    score = 0.0

    # iterate over the chromosome
    for value in chromosome:
        if value==0:
            score += 0.1
    return score


def run_main():
    # Genome instance
    genome = G1DList.G1DList(40)

    # The gauss_mu and gauss_sigma is used to the Gaussian Mutator, but
    # if you don't specify, the mutator will use the defaults
    genome.setParams(rangemin=0, rangemax=10, gauss_mu=4, gauss_sigma=6)
    genome.mutator.set(Mutators.G1DListMutatorIntegerGaussian)

    # The evaluator function (objective function)
    genome.evaluator.set(eval_func)

    # Genetic Algorithm Instance
    ga = GSimpleGA.GSimpleGA(genome)
    #ga.selector.set(Selectors.GRouletteWheel)
    ga.setGenerations(800)

    # Do the evolution, with stats dump
    # frequency of 10 generations
    ga.evolve(freq_stats=150)

    # Best individual
    print ga.bestIndividual()


if __name__ == "__main__":
    run_main()
