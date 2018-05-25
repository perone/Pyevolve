"""

:mod:`Mutators` -- mutation methods module
=====================================================================

In this module we have the genetic operators of mutation for each chromosome representation.

"""
from future.builtins import range

from . import Util
from random import randint as rand_randint, gauss as rand_gauss, uniform as rand_uniform
from random import choice as rand_choice
from . import GTree


# 1D Binary String

def G1DBinaryStringMutatorSwap(genome, **args):
    """ The 1D Binary String Swap Mutator """

    if args["pmut"] <= 0.0:
        return 0
    stringLength = len(genome)
    mutations = args["pmut"] * (stringLength)

    if mutations < 1.0:
        mutations = 0
        for it in range(stringLength):
            if Util.randomFlipCoin(args["pmut"]):
                Util.listSwapElement(genome, it, rand_randint(0, stringLength - 1))
                mutations += 1

    else:
        for it in range(int(round(mutations))):
            Util.listSwapElement(genome, rand_randint(0, stringLength - 1),
                                 rand_randint(0, stringLength - 1))

    return int(mutations)


def G1DBinaryStringMutatorFlip(genome, **args):
    """ The classical flip mutator for binary strings """
    if args["pmut"] <= 0.0:
        return 0
    stringLength = len(genome)
    mutations = args["pmut"] * (stringLength)

    if mutations < 1.0:
        mutations = 0
        for it in range(stringLength):
            if Util.randomFlipCoin(args["pmut"]):
                if genome[it] == 0:
                    genome[it] = 1
                else:
                    genome[it] = 0
                mutations += 1

    else:
        for it in range(int(round(mutations))):
            which = rand_randint(0, stringLength - 1)
            if genome[which] == 0:
                genome[which] = 1
            else:
                genome[which] = 0

    return int(mutations)


# 1D List

def G1DListMutatorSwap(genome, **args):
    """ The mutator of G1DList, Swap Mutator

    .. note:: this mutator is :term:`Data Type Independent`

    """
    if args["pmut"] <= 0.0:
        return 0
    listSize = len(genome)
    mutations = args["pmut"] * listSize

    if mutations < 1.0:
        mutations = 0
        for it in range(listSize):
            if Util.randomFlipCoin(args["pmut"]):
                Util.listSwapElement(genome, it, rand_randint(0, listSize - 1))
                mutations += 1
    else:
        for it in range(int(round(mutations))):
            Util.listSwapElement(genome, rand_randint(0, listSize - 1), rand_randint(0, listSize - 1))

    return int(mutations)


def G1DListMutatorSIM(genome, **args):
    """ The mutator of G1DList, Simple Inversion Mutation

    .. note:: this mutator is :term:`Data Type Independent`

    """
    mutations = 0
    if args["pmut"] <= 0.0:
        return 0

    cuts = [rand_randint(0, len(genome)), rand_randint(0, len(genome))]

    if cuts[0] > cuts[1]:
        Util.listSwapElement(cuts, 0, 1)

    if (cuts[1] - cuts[0]) <= 0:
        cuts[1] = rand_randint(cuts[0], len(genome))

    if Util.randomFlipCoin(args["pmut"]):
        part = genome[cuts[0]:cuts[1]]
        if len(part) == 0:
            return 0
        part.reverse()
        genome[cuts[0]:cuts[1]] = part
        mutations += 1

    return mutations


def G1DListMutatorIntegerRange(genome, **args):
    """ Simple integer range mutator for G1DList

    Accepts the *rangemin* and *rangemax* genome parameters, both optional.

    """
    from . import Consts

    if args["pmut"] <= 0.0:
        return 0
    listSize = len(genome)
    mutations = args["pmut"] * listSize

    if mutations < 1.0:
        mutations = 0
        for it in range(listSize):
            if Util.randomFlipCoin(args["pmut"]):
                genome[it] = rand_randint(genome.getParam("rangemin", Consts.CDefRangeMin),
                                          genome.getParam("rangemax", Consts.CDefRangeMax))
                mutations += 1

    else:
        for it in range(int(round(mutations))):
            which_gene = rand_randint(0, listSize - 1)
            genome[which_gene] = rand_randint(genome.getParam("rangemin", Consts.CDefRangeMin),
                                              genome.getParam("rangemax", Consts.CDefRangeMax))

    return int(mutations)


def G1DListMutatorRealRange(genome, **args):
    """ Simple real range mutator for G1DList

    Accepts the *rangemin* and *rangemax* genome parameters, both optional.

    """
    from . import Consts

    if args["pmut"] <= 0.0:
        return 0
    listSize = len(genome)
    mutations = args["pmut"] * (listSize)

    if mutations < 1.0:
        mutations = 0
        for it in range(listSize):
            if Util.randomFlipCoin(args["pmut"]):
                genome[it] = rand_uniform(genome.getParam("rangemin", Consts.CDefRangeMin),
                                          genome.getParam("rangemax", Consts.CDefRangeMax))
                mutations += 1

    else:
        for it in range(int(round(mutations))):
            which_gene = rand_randint(0, listSize - 1)
            genome[which_gene] = rand_uniform(genome.getParam("rangemin", Consts.CDefRangeMin),
                                              genome.getParam("rangemax", Consts.CDefRangeMax))

    return int(mutations)


def G1DListMutatorIntegerGaussianGradient(genome, **args):
    """ A gaussian mutator for G1DList of Integers

    Accepts the *rangemin* and *rangemax* genome parameters, both optional. The
    random distribution is set with mu=1.0 and std=0.0333

    Same as IntegerGaussian, except that this uses relative gradient rather than
    absolute gaussian. A value is randomly generated about gauss(mu=1, sigma=.0333)
    and multiplied by the gene to drift it up or down (depending on what side of
    1 the random value falls on) and cast to integer

    """
    from . import Consts

    if args["pmut"] <= 0.0:
        return 0
    listSize = len(genome)
    mutations = args["pmut"] * (listSize)

    mu = Consts.CDefGaussianGradientMU
    sigma = Consts.CDefGaussianGradientSIGMA

    if mutations < 1.0:
        mutations = 0
        for it in range(listSize):
            if Util.randomFlipCoin(args["pmut"]):
                final_value = int(genome[it] * abs(rand_gauss(mu, sigma)))

                final_value = min(final_value, genome.getParam("rangemax", Consts.CDefRangeMax))
                final_value = max(final_value, genome.getParam("rangemin", Consts.CDefRangeMin))

                genome[it] = final_value
                mutations += 1
    else:
        for it in range(int(round(mutations))):
            which_gene = rand_randint(0, listSize - 1)
            final_value = int(genome[which_gene] * abs(rand_gauss(mu, sigma)))

            final_value = min(final_value, genome.getParam("rangemax", Consts.CDefRangeMax))
            final_value = max(final_value, genome.getParam("rangemin", Consts.CDefRangeMin))

            genome[which_gene] = final_value

    return int(mutations)


def G1DListMutatorIntegerGaussian(genome, **args):
    """ A gaussian mutator for G1DList of Integers

    Accepts the *rangemin* and *rangemax* genome parameters, both optional. Also
    accepts the parameter *gauss_mu* and the *gauss_sigma* which respectively
    represents the mean and the std. dev. of the random distribution.

    """
    from . import Consts

    if args["pmut"] <= 0.0:
        return 0
    listSize = len(genome)
    mutations = args["pmut"] * (listSize)

    mu = genome.getParam("gauss_mu")
    sigma = genome.getParam("gauss_sigma")

    if mu is None:
        mu = Consts.CDefG1DListMutIntMU

    if sigma is None:
        sigma = Consts.CDefG1DListMutIntSIGMA

    if mutations < 1.0:
        mutations = 0
        for it in range(listSize):
            if Util.randomFlipCoin(args["pmut"]):
                final_value = genome[it] + int(rand_gauss(mu, sigma))

                final_value = min(final_value, genome.getParam("rangemax", Consts.CDefRangeMax))
                final_value = max(final_value, genome.getParam("rangemin", Consts.CDefRangeMin))

                genome[it] = final_value
                mutations += 1
    else:
        for it in range(int(round(mutations))):
            which_gene = rand_randint(0, listSize - 1)
            final_value = genome[which_gene] + int(rand_gauss(mu, sigma))

            final_value = min(final_value, genome.getParam("rangemax", Consts.CDefRangeMax))
            final_value = max(final_value, genome.getParam("rangemin", Consts.CDefRangeMin))

            genome[which_gene] = final_value

    return int(mutations)


def G1DListMutatorRealGaussian(genome, **args):
    """ The mutator of G1DList, Gaussian Mutator

    Accepts the *rangemin* and *rangemax* genome parameters, both optional. Also
    accepts the parameter *gauss_mu* and the *gauss_sigma* which respectively
    represents the mean and the std. dev. of the random distribution.

    """
    from . import Consts

    if args["pmut"] <= 0.0:
        return 0
    listSize = len(genome)
    mutations = args["pmut"] * (listSize)

    mu = genome.getParam("gauss_mu")
    sigma = genome.getParam("gauss_sigma")

    if mu is None:
        mu = Consts.CDefG1DListMutRealMU

    if sigma is None:
        sigma = Consts.CDefG1DListMutRealSIGMA

    if mutations < 1.0:
        mutations = 0
        for it in range(listSize):
            if Util.randomFlipCoin(args["pmut"]):
                final_value = genome[it] + rand_gauss(mu, sigma)

                final_value = min(final_value, genome.getParam("rangemax", Consts.CDefRangeMax))
                final_value = max(final_value, genome.getParam("rangemin", Consts.CDefRangeMin))

                genome[it] = final_value
                mutations += 1
    else:
        for it in range(int(round(mutations))):
            which_gene = rand_randint(0, listSize - 1)
            final_value = genome[which_gene] + rand_gauss(mu, sigma)

            final_value = min(final_value, genome.getParam("rangemax", Consts.CDefRangeMax))
            final_value = max(final_value, genome.getParam("rangemin", Consts.CDefRangeMin))

            genome[which_gene] = final_value

    return int(mutations)


def G1DListMutatorRealGaussianGradient(genome, **args):
    """ The mutator of G1DList, Gaussian Gradient Mutator

    Accepts the *rangemin* and *rangemax* genome parameters, both optional. The
    random distribution is set with mu=1.0 and std=0.0333

    The difference between this routine and the normal Gaussian Real is that the
    other function generates a gaussian value and adds it to the value. If the
    mu is 0, and the std is 1, a typical value could be 1.8 or -0.5. These small
    values are fine if your range is 0-10, but if your range is much larger, like
    0-100,000, a relative gradient makes sense.

    This routine generates a gaussian value with mu=1.0 and std=0.0333 and then
    the gene is multiplied by this value. This will cause the gene to drift
    no matter how large it is.

    """
    from . import Consts

    if args["pmut"] <= 0.0:
        return 0
    listSize = len(genome)
    mutations = args["pmut"] * (listSize)

    mu = Consts.CDefGaussianGradientMU
    sigma = Consts.CDefGaussianGradientSIGMA

    if mutations < 1.0:
        mutations = 0
        for it in range(listSize):
            if Util.randomFlipCoin(args["pmut"]):
                final_value = genome[it] * abs(rand_gauss(mu, sigma))

                final_value = min(final_value, genome.getParam("rangemax", Consts.CDefRangeMax))
                final_value = max(final_value, genome.getParam("rangemin", Consts.CDefRangeMin))

                genome[it] = final_value
                mutations += 1
    else:
        for it in range(int(round(mutations))):
            which_gene = rand_randint(0, listSize - 1)
            final_value = genome[which_gene] * abs(rand_gauss(mu, sigma))

            final_value = min(final_value, genome.getParam("rangemax", Consts.CDefRangeMax))
            final_value = max(final_value, genome.getParam("rangemin", Consts.CDefRangeMin))

            genome[which_gene] = final_value

    return int(mutations)


def G1DListMutatorIntegerBinary(genome, **args):
    """ The mutator of G1DList, the binary mutator

    This mutator will random change the 0 and 1 elements of the 1D List.

    """
    if args["pmut"] <= 0.0:
        return 0
    listSize = len(genome)
    mutations = args["pmut"] * (listSize)

    if mutations < 1.0:
        mutations = 0
        for it in range(listSize):
            if Util.randomFlipCoin(args["pmut"]):
                if genome[it] == 0:
                    genome[it] = 1
                elif genome[it] == 1:
                    genome[it] = 0

                mutations += 1
    else:
        for it in range(int(round(mutations))):
            which_gene = rand_randint(0, listSize - 1)
            if genome[which_gene] == 0:
                genome[which_gene] = 1
            elif genome[which_gene] == 1:
                genome[which_gene] = 0

    return int(mutations)


def G1DListMutatorAllele(genome, **args):
    """ The mutator of G1DList, Allele Mutator

    To use this mutator, you must specify the *allele* genome parameter with the
    :class:`GAllele.GAlleles` instance.

    """
    if args["pmut"] <= 0.0:
        return 0
    listSize = len(genome)
    mutations = args["pmut"] * listSize

    allele = genome.getParam("allele", None)
    if allele is None:
        Util.raiseException("to use the G1DListMutatorAllele, you must specify the 'allele' parameter", TypeError)

    if mutations < 1.0:
        mutations = 0
        for it in range(listSize):
            if Util.randomFlipCoin(args["pmut"]):
                new_val = allele[it].getRandomAllele()
                genome[it] = new_val
                mutations += 1
    else:
        for it in range(int(round(mutations))):
            which_gene = rand_randint(0, listSize - 1)
            new_val = allele[which_gene].getRandomAllele()
            genome[which_gene] = new_val

    return int(mutations)


def G1DListMutatorAlleleGaussian(genome, **arguments):
    """An allele-based mutator based on G1DListMutatorRealGaussian.

    Accepts the parameter *gauss_mu* and the *gauss_sigma* which
    respectively represents the mean and the std. dev. of the random
    distribution.
    """
    from . import Consts

    if arguments["pmut"] <= 0.0:
        return 0
    listSize = len(genome)
    mutations = arguments["pmut"] * listSize

    mu = genome.getParam("gauss_mu")
    sigma = genome.getParam("gauss_sigma")
    if mu is None:
        mu = Consts.CDefG1DListMutRealMU
    if sigma is None:
        sigma = Consts.CDefG1DListMutRealSIGMA

    allele = genome.getParam("allele", None)
    if allele is None:
        Util.raiseException("to use this mutator, you must specify the 'allele' parameter", TypeError)

    if mutations < 1.0:
        mutations = 0
        for it in range(listSize):
            if Util.randomFlipCoin(arguments["pmut"]):
                final_value = genome[it] + rand_gauss(mu, sigma)
                assert len(allele[it].beginEnd) == 1, "only single ranges are supported"
                rangemin, rangemax = allele[it].beginEnd[0]
                final_value = min(final_value, rangemax)
                final_value = max(final_value, rangemin)
                genome[it] = final_value
                mutations += 1
    else:
        for it in range(int(round(mutations))):
            which_gene = rand_randint(0, listSize - 1)
            final_value = genome[which_gene] + rand_gauss(mu, sigma)
            assert len(allele[which_gene].beginEnd) == 1, "only single ranges are supported"
            rangemin, rangemax = allele[which_gene].beginEnd[0]
            final_value = min(final_value, rangemax)
            final_value = max(final_value, rangemin)
            genome[which_gene] = final_value
    return int(mutations)


# 2D List

def G2DListMutatorSwap(genome, **args):
    """ The mutator of G1DList, Swap Mutator

    .. note:: this mutator is :term:`Data Type Independent`

    """

    if args["pmut"] <= 0.0:
        return 0
    height, width = genome.getSize()
    elements = height * width

    mutations = args["pmut"] * elements

    if mutations < 1.0:
        mutations = 0
        for i in range(height):
            for j in range(width):
                if Util.randomFlipCoin(args["pmut"]):
                    index_b = (rand_randint(0, height - 1), rand_randint(0, width - 1))
                    Util.list2DSwapElement(genome.genomeList, (i, j), index_b)
                    mutations += 1
    else:
        for it in range(int(round(mutations))):
            index_a = (rand_randint(0, height - 1), rand_randint(0, width - 1))
            index_b = (rand_randint(0, height - 1), rand_randint(0, width - 1))
            Util.list2DSwapElement(genome.genomeList, index_a, index_b)

    return int(mutations)


def G2DListMutatorIntegerRange(genome, **args):
    """ Simple integer range mutator for G2DList

    Accepts the *rangemin* and *rangemax* genome parameters, both optional.

    """
    from . import Consts

    if args["pmut"] <= 0.0:
        return 0
    height, width = genome.getSize()
    elements = height * width

    mutations = args["pmut"] * elements

    range_min = genome.getParam("rangemin", Consts.CDefRangeMin)
    range_max = genome.getParam("rangemax", Consts.CDefRangeMax)

    if mutations < 1.0:
        mutations = 0
        for i in range(genome.getHeight()):
            for j in range(genome.getWidth()):
                if Util.randomFlipCoin(args["pmut"]):
                    random_int = rand_randint(range_min, range_max)
                    genome.setItem(i, j, random_int)
                    mutations += 1

    else:
        for it in range(int(round(mutations))):
            which_x = rand_randint(0, genome.getWidth() - 1)
            which_y = rand_randint(0, genome.getHeight() - 1)
            random_int = rand_randint(range_min, range_max)
            genome.setItem(which_y, which_x, random_int)

    return int(mutations)


def G2DListMutatorIntegerGaussianGradient(genome, **args):
    """ A gaussian mutator for G2DList of Integers

    Accepts the *rangemin* and *rangemax* genome parameters, both optional.

    This routine generates a gaussian value with mu=1.0 and std=0.0333 and then
    the gene is multiplied by this value. This will cause the gene to drift
    no matter how large it is.

    """
    from . import Consts

    if args["pmut"] <= 0.0:
        return 0
    height, width = genome.getSize()
    elements = height * width

    mutations = args["pmut"] * elements

    mu = Consts.CDefGaussianGradientMU
    sigma = Consts.CDefGaussianGradientSIGMA

    if mutations < 1.0:
        mutations = 0

        for i in range(genome.getHeight()):
            for j in range(genome.getWidth()):
                if Util.randomFlipCoin(args["pmut"]):
                    final_value = int(genome[i][j] * abs(rand_gauss(mu, sigma)))

                    final_value = min(final_value, genome.getParam("rangemax", Consts.CDefRangeMax))
                    final_value = max(final_value, genome.getParam("rangemin", Consts.CDefRangeMin))

                    genome.setItem(i, j, final_value)
                    mutations += 1
    else:

        for it in range(int(round(mutations))):
            which_x = rand_randint(0, genome.getWidth() - 1)
            which_y = rand_randint(0, genome.getHeight() - 1)

            final_value = int(genome[which_y][which_x] * abs(rand_gauss(mu, sigma)))

            final_value = min(final_value, genome.getParam("rangemax", Consts.CDefRangeMax))
            final_value = max(final_value, genome.getParam("rangemin", Consts.CDefRangeMin))

            genome.setItem(which_y, which_x, final_value)

    return int(mutations)


def G2DListMutatorIntegerGaussian(genome, **args):
    """ A gaussian mutator for G2DList of Integers

    Accepts the *rangemin* and *rangemax* genome parameters, both optional. Also
    accepts the parameter *gauss_mu* and the *gauss_sigma* which respectively
    represents the mean and the std. dev. of the random distribution.

    """
    from . import Consts

    if args["pmut"] <= 0.0:
        return 0
    height, width = genome.getSize()
    elements = height * width

    mutations = args["pmut"] * elements

    mu = genome.getParam("gauss_mu")
    sigma = genome.getParam("gauss_sigma")

    if mu is None:
        mu = Consts.CDefG2DListMutIntMU

    if sigma is None:
        sigma = Consts.CDefG2DListMutIntSIGMA

    if mutations < 1.0:
        mutations = 0

        for i in range(genome.getHeight()):
            for j in range(genome.getWidth()):
                if Util.randomFlipCoin(args["pmut"]):
                    final_value = genome[i][j] + int(rand_gauss(mu, sigma))

                    final_value = min(final_value, genome.getParam("rangemax", Consts.CDefRangeMax))
                    final_value = max(final_value, genome.getParam("rangemin", Consts.CDefRangeMin))

                    genome.setItem(i, j, final_value)
                    mutations += 1
    else:

        for it in range(int(round(mutations))):
            which_x = rand_randint(0, genome.getWidth() - 1)
            which_y = rand_randint(0, genome.getHeight() - 1)

            final_value = genome[which_y][which_x] + int(rand_gauss(mu, sigma))

            final_value = min(final_value, genome.getParam("rangemax", Consts.CDefRangeMax))
            final_value = max(final_value, genome.getParam("rangemin", Consts.CDefRangeMin))

            genome.setItem(which_y, which_x, final_value)

    return int(mutations)


def G2DListMutatorAllele(genome, **args):
    """ The mutator of G2DList, Allele Mutator

    To use this mutator, you must specify the *allele* genome parameter with the
    :class:`GAllele.GAlleles` instance.

    .. warning:: the :class:`GAllele.GAlleles` instance must have the homogeneous flag enabled

    """
    if args["pmut"] <= 0.0:
        return 0
    listSize = genome.getHeight() * genome.getWidth() - 1
    mutations = args["pmut"] * (listSize + 1)

    allele = genome.getParam("allele", None)
    if allele is None:
        Util.raiseException("to use the G2DListMutatorAllele, you must specify the 'allele' parameter", TypeError)

    if not allele.homogeneous:
        Util.raiseException("to use the G2DListMutatorAllele, the 'allele' must be homogeneous")

    if mutations < 1.0:
        mutations = 0

        for i in range(genome.getHeight()):
            for j in range(genome.getWidth()):
                if Util.randomFlipCoin(args["pmut"]):
                    new_val = allele[0].getRandomAllele()
                    genome.setItem(i, j, new_val)
                    mutations += 1
    else:
        for it in range(int(round(mutations))):
            which_x = rand_randint(0, genome.getHeight() - 1)
            which_y = rand_randint(0, genome.getWidth() - 1)

            new_val = allele[0].getRandomAllele()
            genome.setItem(which_x, which_y, new_val)

    return int(mutations)


def G2DListMutatorRealGaussian(genome, **args):
    """ A gaussian mutator for G2DList of Real

    Accepts the *rangemin* and *rangemax* genome parameters, both optional. Also
    accepts the parameter *gauss_mu* and the *gauss_sigma* which respectively
    represents the mean and the std. dev. of the random distribution.

    """
    from . import Consts

    if args["pmut"] <= 0.0:
        return 0
    height, width = genome.getSize()
    elements = height * width

    mutations = args["pmut"] * elements

    mu = genome.getParam("gauss_mu")
    sigma = genome.getParam("gauss_sigma")

    if mu is None:
        mu = Consts.CDefG2DListMutRealMU

    if sigma is None:
        sigma = Consts.CDefG2DListMutRealSIGMA

    if mutations < 1.0:
        mutations = 0

        for i in range(genome.getHeight()):
            for j in range(genome.getWidth()):
                if Util.randomFlipCoin(args["pmut"]):
                    final_value = genome[i][j] + rand_gauss(mu, sigma)

                    final_value = min(final_value, genome.getParam("rangemax", Consts.CDefRangeMax))
                    final_value = max(final_value, genome.getParam("rangemin", Consts.CDefRangeMin))

                    genome.setItem(i, j, final_value)
                    mutations += 1
    else:

        for it in range(int(round(mutations))):
            which_x = rand_randint(0, genome.getWidth() - 1)
            which_y = rand_randint(0, genome.getHeight() - 1)

            final_value = genome[which_y][which_x] + rand_gauss(mu, sigma)

            final_value = min(final_value, genome.getParam("rangemax", Consts.CDefRangeMax))
            final_value = max(final_value, genome.getParam("rangemin", Consts.CDefRangeMin))

            genome.setItem(which_y, which_x, final_value)

    return int(mutations)


def G2DListMutatorRealGaussianGradient(genome, **args):
    """ A gaussian gradient mutator for G2DList of Real

    Accepts the *rangemin* and *rangemax* genome parameters, both optional.

    The difference is that this multiplies the gene by gauss(1.0, 0.0333), allowing
    for a smooth gradient drift about the value.

    """
    from . import Consts

    if args["pmut"] <= 0.0:
        return 0
    height, width = genome.getSize()
    elements = height * width

    mutations = args["pmut"] * elements

    mu = Consts.CDefGaussianGradientMU
    sigma = Consts.CDefGaussianGradientSIGMA

    if mutations < 1.0:
        mutations = 0

        for i in range(genome.getHeight()):
            for j in range(genome.getWidth()):
                if Util.randomFlipCoin(args["pmut"]):
                    final_value = genome[i][j] * abs(rand_gauss(mu, sigma))

                    final_value = min(final_value, genome.getParam("rangemax", Consts.CDefRangeMax))
                    final_value = max(final_value, genome.getParam("rangemin", Consts.CDefRangeMin))

                    genome.setItem(i, j, final_value)
                    mutations += 1
    else:

        for it in range(int(round(mutations))):
            which_x = rand_randint(0, genome.getWidth() - 1)
            which_y = rand_randint(0, genome.getHeight() - 1)

            final_value = genome[which_y][which_x] * abs(rand_gauss(mu, sigma))

            final_value = min(final_value, genome.getParam("rangemax", Consts.CDefRangeMax))
            final_value = max(final_value, genome.getParam("rangemin", Consts.CDefRangeMin))

            genome.setItem(which_y, which_x, final_value)

    return int(mutations)


# 2D Binary String

def G2DBinaryStringMutatorSwap(genome, **args):
    """ The mutator of G2DBinaryString, Swap Mutator

    .. versionadded:: 0.6
       The *G2DBinaryStringMutatorSwap* function
    """

    if args["pmut"] <= 0.0:
        return 0
    height, width = genome.getSize()
    elements = height * width

    mutations = args["pmut"] * elements

    if mutations < 1.0:
        mutations = 0
        for i in range(height):
            for j in range(width):
                if Util.randomFlipCoin(args["pmut"]):
                    index_b = (rand_randint(0, height - 1), rand_randint(0, width - 1))
                    Util.list2DSwapElement(genome.genomeString, (i, j), index_b)
                    mutations += 1
    else:
        for it in range(int(round(mutations))):
            index_a = (rand_randint(0, height - 1), rand_randint(0, width - 1))
            index_b = (rand_randint(0, height - 1), rand_randint(0, width - 1))
            Util.list2DSwapElement(genome.genomeString, index_a, index_b)

    return int(mutations)


def G2DBinaryStringMutatorFlip(genome, **args):
    """ A flip mutator for G2DBinaryString

    .. versionadded:: 0.6
       The *G2DBinaryStringMutatorFlip* function
    """
    if args["pmut"] <= 0.0:
        return 0
    height, width = genome.getSize()
    elements = height * width

    mutations = args["pmut"] * elements

    if mutations < 1.0:
        mutations = 0

        for i in range(genome.getHeight()):
            for j in range(genome.getWidth()):
                if Util.randomFlipCoin(args["pmut"]):
                    if genome[i][j] == 0:
                        genome.setItem(i, j, 1)
                    else:
                        genome.setItem(i, j, 0)
                    mutations += 1
    else:  # TODO very suspicious branch

        for it in range(int(round(mutations))):
            which_x = rand_randint(0, genome.getWidth() - 1)
            which_y = rand_randint(0, genome.getHeight() - 1)

            if genome[i][j] == 0:
                genome.setItem(which_y, which_x, 1)
            else:
                genome.setItem(which_y, which_x, 0)

    return int(mutations)


# Tree

def GTreeMutatorSwap(genome, **args):
    """ The mutator of GTree, Swap Mutator

    .. versionadded:: 0.6
       The *GTreeMutatorSwap* function
    """
    if args["pmut"] <= 0.0:
        return 0
    elements = len(genome)
    mutations = args["pmut"] * elements

    if mutations < 1.0:
        mutations = 0
        for i in range(len(genome)):
            if Util.randomFlipCoin(args["pmut"]):
                mutations += 1
                nodeOne = genome.getRandomNode()
                nodeTwo = genome.getRandomNode()
                nodeOne.swapNodeData(nodeTwo)
    else:
        for it in range(int(round(mutations))):
            nodeOne = genome.getRandomNode()
            nodeTwo = genome.getRandomNode()
            nodeOne.swapNodeData(nodeTwo)

    return int(mutations)


def GTreeMutatorIntegerRange(genome, **args):
    """ The mutator of GTree, Integer Range Mutator

    Accepts the *rangemin* and *rangemax* genome parameters, both optional.

    .. versionadded:: 0.6
       The *GTreeMutatorIntegerRange* function
    """
    from . import Consts

    if args["pmut"] <= 0.0:
        return 0
    elements = len(genome)
    mutations = args["pmut"] * elements

    range_min = genome.getParam("rangemin", Consts.CDefRangeMin)
    range_max = genome.getParam("rangemax", Consts.CDefRangeMax)

    if mutations < 1.0:
        mutations = 0
        for i in range(len(genome)):
            if Util.randomFlipCoin(args["pmut"]):
                mutations += 1
                rand_node = genome.getRandomNode()
                random_int = rand_randint(range_min, range_max)
                rand_node.setData(random_int)

    else:
        for it in range(int(round(mutations))):
            rand_node = genome.getRandomNode()
            random_int = rand_randint(range_min, range_max)
            rand_node.setData(random_int)

    return int(mutations)


def GTreeMutatorRealRange(genome, **args):
    """ The mutator of GTree, Real Range Mutator

    Accepts the *rangemin* and *rangemax* genome parameters, both optional.

    .. versionadded:: 0.6
       The *GTreeMutatorRealRange* function
    """
    from . import Consts

    if args["pmut"] <= 0.0:
        return 0
    elements = len(genome)
    mutations = args["pmut"] * elements

    range_min = genome.getParam("rangemin", Consts.CDefRangeMin)
    range_max = genome.getParam("rangemax", Consts.CDefRangeMax)

    if mutations < 1.0:
        mutations = 0
        for i in range(len(genome)):
            if Util.randomFlipCoin(args["pmut"]):
                mutations += 1
                rand_node = genome.getRandomNode()
                random_real = rand_uniform(range_min, range_max)
                rand_node.setData(random_real)

    else:
        for it in range(int(round(mutations))):
            rand_node = genome.getRandomNode()
            random_real = rand_uniform(range_min, range_max)
            rand_node.setData(random_real)

    return int(mutations)


def GTreeMutatorIntegerGaussian(genome, **args):
    """ A gaussian mutator for GTree of Integers

    Accepts the *rangemin* and *rangemax* genome parameters, both optional. Also
    accepts the parameter *gauss_mu* and the *gauss_sigma* which respectively
    represents the mean and the std. dev. of the random distribution.

    """
    from . import Consts

    if args["pmut"] <= 0.0:
        return 0
    elements = len(genome)
    mutations = args["pmut"] * elements

    mu = genome.getParam("gauss_mu", Consts.CDefG1DListMutIntMU)
    sigma = genome.getParam("gauss_sigma", Consts.CDefG1DListMutIntSIGMA)

    if mutations < 1.0:
        mutations = 0
        for i in range(len(genome)):
            if Util.randomFlipCoin(args["pmut"]):
                mutations += 1
                rand_node = genome.getRandomNode()
                final_value = rand_node.getData() + int(rand_gauss(mu, sigma))
                final_value = min(final_value, genome.getParam("rangemax", Consts.CDefRangeMax))
                final_value = max(final_value, genome.getParam("rangemin", Consts.CDefRangeMin))
                rand_node.setData(final_value)
    else:
        for it in range(int(round(mutations))):
            rand_node = genome.getRandomNode()
            final_value = rand_node.getData() + int(rand_gauss(mu, sigma))
            final_value = min(final_value, genome.getParam("rangemax", Consts.CDefRangeMax))
            final_value = max(final_value, genome.getParam("rangemin", Consts.CDefRangeMin))
            rand_node.setData(final_value)

    return int(mutations)


def GTreeMutatorRealGaussian(genome, **args):
    """ A gaussian mutator for GTree of Real numbers

    Accepts the *rangemin* and *rangemax* genome parameters, both optional. Also
    accepts the parameter *gauss_mu* and the *gauss_sigma* which respectively
    represents the mean and the std. dev. of the random distribution.

    """
    from . import Consts
    if args["pmut"] <= 0.0:
        return 0
    elements = len(genome)
    mutations = args["pmut"] * elements

    mu = genome.getParam("gauss_mu", Consts.CDefG1DListMutRealMU)
    sigma = genome.getParam("gauss_sigma", Consts.CDefG1DListMutRealSIGMA)

    if mutations < 1.0:
        mutations = 0
        for i in range(len(genome)):
            if Util.randomFlipCoin(args["pmut"]):
                mutations += 1
                rand_node = genome.getRandomNode()
                final_value = rand_node.getData() + rand_gauss(mu, sigma)
                final_value = min(final_value, genome.getParam("rangemax", Consts.CDefRangeMax))
                final_value = max(final_value, genome.getParam("rangemin", Consts.CDefRangeMin))
                rand_node.setData(final_value)
    else:
        for it in range(int(round(mutations))):
            rand_node = genome.getRandomNode()
            final_value = rand_node.getData() + rand_gauss(mu, sigma)
            final_value = min(final_value, genome.getParam("rangemax", Consts.CDefRangeMax))
            final_value = max(final_value, genome.getParam("rangemin", Consts.CDefRangeMin))
            rand_node.setData(final_value)

    return int(mutations)


# Tree GP

def GTreeGPMutatorOperation(genome, **args):
    """ The mutator of GTreeGP, Operation Mutator

    .. versionadded:: 0.6
       The *GTreeGPMutatorOperation* function
    """
    from . import Consts
    if args["pmut"] <= 0.0:
        return 0
    elements = len(genome)
    mutations = args["pmut"] * elements
    ga_engine = args["ga_engine"]

    gp_terminals = ga_engine.getParam("gp_terminals")
    assert gp_terminals is not None

    gp_function_set = ga_engine.getParam("gp_function_set")
    assert gp_function_set is not None

    if mutations < 1.0:
        mutations = 0
        for i in range(len(genome)):
            if Util.randomFlipCoin(args["pmut"]):
                mutations += 1
                rand_node = genome.getRandomNode()
                assert rand_node is not None
                if rand_node.getType() == Consts.nodeType["TERMINAL"]:
                    term_operator = rand_choice(gp_terminals)
                else:
                    op_len = gp_function_set[rand_node.getData()]
                    fun_candidates = []
                    for o, length in list(gp_function_set.items()):
                        if length == op_len:
                            fun_candidates.append(o)

                    if len(fun_candidates) <= 0:
                        continue

                    term_operator = rand_choice(fun_candidates)
                rand_node.setData(term_operator)
    else:
        for _ in range(int(round(mutations))):  # TODO probably inoptimal
            rand_node = genome.getRandomNode()
            assert rand_node is not None
            if rand_node.getType() == Consts.nodeType["TERMINAL"]:
                term_operator = rand_choice(gp_terminals)
            else:
                op_len = gp_function_set[rand_node.getData()]
                fun_candidates = []
                for o, length in list(gp_function_set.items()):
                    if length == op_len:
                        fun_candidates.append(o)

                if len(fun_candidates) <= 0:
                    continue

                term_operator = rand_choice(fun_candidates)
            rand_node.setData(term_operator)

    return int(mutations)


def GTreeGPMutatorSubtree(genome, **args):
    """ The mutator of GTreeGP, Subtree Mutator

    This mutator will recreate random subtree of the tree using the grow algorithm.

    .. versionadded:: 0.6
       The *GTreeGPMutatorSubtree* function
    """

    if args["pmut"] <= 0.0:
        return 0
    ga_engine = args["ga_engine"]
    max_depth = genome.getParam("max_depth", None)
    mutations = 0

    if max_depth is None:
        Util.raiseException("You must specify the max_depth genome parameter !", ValueError)

    if max_depth < 0:
        Util.raiseException(
            "The max_depth must be >= 1, if you want to use GTreeGPMutatorSubtree crossover !", ValueError)

    branch_list = genome.nodes_branch
    elements = len(branch_list)

    for i in range(elements):

        node = branch_list[i]
        assert node is not None

        if Util.randomFlipCoin(args["pmut"]):
            depth = genome.getNodeDepth(node)
            mutations += 1

            root_subtree = GTree.buildGTreeGPGrow(ga_engine, 0, max_depth - depth)
            node_parent = node.getParent()

            if node_parent is None:
                genome.setRoot(root_subtree)
                genome.processNodes()
                return mutations
            else:
                root_subtree.setParent(node_parent)
                node_parent.replaceChild(node, root_subtree)
            genome.processNodes()

    return int(mutations)
