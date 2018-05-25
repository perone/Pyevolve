"""

:mod:`Selectors` -- selection methods module
==============================================================

This module have the *selection methods*, like roulette wheel, tournament, ranking, etc.

"""
from future.builtins import range

import random


def GRankSelector(population, **args):
    """ The Rank Selector - This selector will pick the best individual of
    the population every time.
    """
    from . import Consts
    count = 0

    if args["popID"] != GRankSelector.cachePopID:
        if population.sortType == Consts.sortType["scaled"]:
            best_fitness = population.bestFitness().fitness
            for index in range(1, len(population.internalPop)):
                if population[index].fitness == best_fitness:
                    count += 1
        else:
            best_raw = population.bestRaw().score
            for index in range(1, len(population.internalPop)):
                if population[index].score == best_raw:
                    count += 1

        GRankSelector.cachePopID = args["popID"]
        GRankSelector.cacheCount = count

    else:
        count = GRankSelector.cacheCount

    return population[random.randint(0, count)]


GRankSelector.cachePopID = None
GRankSelector.cacheCount = None


def GUniformSelector(population, **args):
    """ The Uniform Selector """
    return population[random.randint(0, len(population) - 1)]


def GTournamentSelector(population, **args):
    """ The Tournament Selector

    It accepts the *tournamentPool* population parameter.

    .. note::
       the Tournament Selector uses the Roulette Wheel to
       pick individuals for the pool

    .. versionchanged:: 0.6
       Changed the parameter `poolSize` to the `tournamentPool`, now the selector
       gets the pool size from the population.

    """
    from . import Consts
    choosen = None
    should_minimize = population.minimax == Consts.minimaxType["minimize"]
    minimax_operator = min if should_minimize else max

    poolSize = population.getParam("tournamentPool", Consts.CDefTournamentPoolSize)
    tournament_pool = [GRouletteWheel(population, **args) for i in range(poolSize)]

    if population.sortType == Consts.sortType["scaled"]:
        choosen = minimax_operator(tournament_pool, key=lambda ind: ind.fitness)
    else:
        choosen = minimax_operator(tournament_pool, key=lambda ind: ind.score)

    return choosen


def GTournamentSelectorAlternative(population, **args):
    """ The alternative Tournament Selector

    This Tournament Selector don't uses the Roulette Wheel

    It accepts the *tournamentPool* population parameter.

    .. versionadded: 0.6
       Added the GTournamentAlternative function.

    """
    from . import Consts
    pool_size = population.getParam("tournamentPool", Consts.CDefTournamentPoolSize)
    len_pop = len(population)
    should_minimize = population.minimax == Consts.minimaxType["minimize"]
    minimax_operator = min if should_minimize else max
    tournament_pool = [population[random.randint(0, len_pop - 1)] for i in range(pool_size)]

    if population.sortType == Consts.sortType["scaled"]:
        choosen = minimax_operator(tournament_pool, key=lambda ind: ind.fitness)
    else:
        choosen = minimax_operator(tournament_pool, key=lambda ind: ind.score)

    return choosen


def GRouletteWheel(population, **args):
    """ The Roulette Wheel selector """
    psum = None
    if args["popID"] != GRouletteWheel.cachePopID:
        GRouletteWheel.cachePopID = args["popID"]
        psum = GRouletteWheel_PrepareWheel(population)
        GRouletteWheel.cacheWheel = psum
    else:
        psum = GRouletteWheel.cacheWheel

    cutoff = random.random()
    lower = 0
    upper = len(population) - 1
    while(upper >= lower):
        i = lower + ((upper - lower) // 2)
        if psum[i] > cutoff:
            upper = i - 1
        else:
            lower = i + 1

    lower = min(len(population) - 1, lower)
    lower = max(0, lower)

    return population.bestFitness(lower)


GRouletteWheel.cachePopID = None
GRouletteWheel.cacheWheel = None


def GRouletteWheel_PrepareWheel(population):
    """ A preparation for Roulette Wheel selection """
    from . import Consts

    len_pop = len(population)

    psum = [i for i in range(len_pop)]

    population.statistics()

    if population.sortType == Consts.sortType["scaled"]:
        pop_fitMax = population.stats["fitMax"]
        pop_fitMin = population.stats["fitMin"]

        if pop_fitMax == pop_fitMin:
            for index in range(len_pop):
                psum[index] = (index + 1) / float(len_pop)
        elif (pop_fitMax > 0 and pop_fitMin >= 0) or (pop_fitMax <= 0 and pop_fitMin < 0):
            population.sort()
            if population.minimax == Consts.minimaxType["maximize"]:
                psum[0] = population[0].fitness
                for i in range(1, len_pop):
                    psum[i] = population[i].fitness + psum[i - 1]
                for i in range(len_pop):
                    psum[i] /= float(psum[len_pop - 1])
            else:
                psum[0] = -population[0].fitness + pop_fitMax + pop_fitMin
                for i in range(1, len_pop):
                    psum[i] = -population[i].fitness + pop_fitMax + pop_fitMin + psum[i - 1]
                for i in range(len_pop):
                    psum[i] /= float(psum[len_pop - 1])
    else:
        pop_rawMax = population.stats["rawMax"]
        pop_rawMin = population.stats["rawMin"]

        if pop_rawMax == pop_rawMin:
            for index in range(len_pop):
                psum[index] = (index + 1) / float(len_pop)

        elif (pop_rawMax > 0 and pop_rawMin >= 0) or (pop_rawMax <= 0 and pop_rawMin < 0):
            population.sort()
            if population.minimax == Consts.minimaxType["maximize"]:
                psum[0] = population[0].score
                for i in range(1, len_pop):
                    psum[i] = population[i].score + psum[i - 1]
                for i in range(len_pop):
                    psum[i] /= float(psum[len_pop - 1])
            else:
                psum[0] = - population[0].score + pop_rawMax + pop_rawMin
                for i in range(1, len_pop):
                    psum[i] = - population[i].score + pop_rawMax + pop_rawMin + psum[i - 1]
                for i in range(len_pop):
                    psum[i] /= float(psum[len_pop - 1])

    return psum
