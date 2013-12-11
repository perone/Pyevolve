#===============================================================================
# Pyevolve version of the Infinite Monkey Theorem
# See: http://en.wikipedia.org/wiki/Infinite_monkey_theorem
# By Jelle Feringa
#===============================================================================

from pyevolve import G1DList
from pyevolve import GSimpleGA, Consts
from pyevolve import Selectors
from pyevolve import Initializators, Mutators, Crossovers
import math

sentence = """
'Just living is not enough,' said the butterfly,
'one must have sunshine, freedom, and a little flower.'
"""
numeric_sentence = map(ord, sentence)

def evolve_callback(ga_engine):
    generation = ga_engine.getCurrentGeneration()
    if generation%50==0:
        indiv = ga_engine.bestIndividual()
        print ''.join(map(chr,indiv))
    return False

def run_main():
    genome = G1DList.G1DList(len(sentence))
    genome.setParams(rangemin=min(numeric_sentence),
                     rangemax=max(numeric_sentence),
                     bestrawscore=0.00,
                     gauss_mu=1, gauss_sigma=4)

    genome.initializator.set(Initializators.G1DListInitializatorInteger)
    genome.mutator.set(Mutators.G1DListMutatorIntegerGaussian)
    genome.evaluator.set(lambda genome: sum(
        [abs(a-b) for a, b in zip(genome, numeric_sentence)]
    ))

    ga = GSimpleGA.GSimpleGA(genome)
    #ga.stepCallback.set(evolve_callback)
    ga.setMinimax(Consts.minimaxType["minimize"])
    ga.terminationCriteria.set(GSimpleGA.RawScoreCriteria)
    ga.setPopulationSize(60)
    ga.setMutationRate(0.02)
    ga.setCrossoverRate(0.9)
    ga.setGenerations(5000)
    ga.evolve(freq_stats=100)

    best = ga.bestIndividual()
    print "Best individual score: %.2f" % (best.score,)
    print ''.join(map(chr, best))

if __name__ == "__main__":
    run_main()
