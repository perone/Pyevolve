"""

:mod:`Scaling` -- scaling schemes module
===========================================================

This module have the *scaling schemes* like Linear scaling, etc.

"""
import Consts
import math
import logging

def LinearScaling(pop):
   """ Linear Scaling scheme

   .. warning :: Linear Scaling is only for positive raw scores

   """
   logging.debug("Running linear scaling.")
   pop.statistics()
   c = Consts.CDefScaleLinearMultiplier
   a = b = delta = 0.0

   pop_rawAve = pop.stats["rawAve"]
   pop_rawMax = pop.stats["rawMax"]
   pop_rawMin = pop.stats["rawMin"]
   
   if pop_rawAve == pop.stats["rawMax"]:
      a = 1.0
      b = 0.0
   elif pop_rawMin > (c * pop_rawAve - pop_rawMax / c - 1.0):
      delta = pop_rawMax - pop_rawAve
      a = (c - 1.0) * pop_rawAve / delta
      b = pop_rawAve * (pop_rawMax - (c * pop_rawAve)) / delta
   else:
    delta = pop_rawAve - pop_rawMin
    a = pop_rawAve / delta
    b = -pop_rawMin * pop_rawAve / delta

   for i in xrange(len(pop)):
      f = pop[i].score
      if f < 0.0:
         critical_msg = "Negative score, linear scaling not supported !"
         logging.critical(critical_msg)
         raise Exception(critical_msg)
      f = f * a + b
      if f < 0:
         f = 0.0
      pop[i].fitness = f

def SigmaTruncScaling(pop):
   """ Sigma Truncation scaling scheme, allows negative scores """
   logging.debug("Running sigma truncation scaling.")
   pop.statistics()
   c = Consts.CDefScaleSigmaTruncMultiplier
   pop_rawAve = pop.stats["rawAve"]
   pop_rawDev = pop.stats["rawDev"]
   for i in xrange(len(pop)):
      f = pop[i].score - pop_rawAve
      f+= c * pop_rawDev
      if f < 0: f = 0.0
      pop[i].fitness = f

def PowerLawScaling(pop):
   """ Power Law scaling scheme

   .. warning :: Power Law Scaling is only for positive raw scores

   """
   logging.debug("Running power law scaling.")
   k = Consts.CDefScalePowerLawFactor
   for i in xrange(len(pop)):
      f = pop[i].score
      if f < 0.0:
         critical_msg = "Negative score, power law scaling not supported !"
         logging.critical(critical_msg)
         raise Exception(critical_msg)
      f = math.pow(f, k)
      pop[i].fitness = f


