"""

:mod:`Util` -- utility module
============================================================================

This is the utility module, with some utility functions of general
use, like list item swap, random utilities and etc.

"""

from random import random as rand_random
from sys import platform as sys_platform
import logging
import Consts

if sys_platform[:5] == "linux":
   import sys, termios
   from select import select

   fd = sys.stdin.fileno()
   new_term = termios.tcgetattr(fd)
   old_term = termios.tcgetattr(fd)
   new_term[3] = (new_term[3] & ~termios.ICANON & ~termios.ECHO)

def set_normal_term():
   """ This is a linux platform function to set the term back to normal """
   termios.tcsetattr(fd, termios.TCSAFLUSH, old_term)

def set_curses_term():
   """ This is a linux platform function to set the term to curses """
   termios.tcsetattr(fd, termios.TCSAFLUSH, new_term)

def getch():
   """ Linux platform function to get a pressed key """
   return sys.stdin.read(1)

def kbhit():
   """ The linux implementation of the kbhit() function """
   dr,dw,de = select([sys.stdin], [], [], 0)
   return dr <> []

def randomFlipCoin(p):
   """ Returns True with the *p* probability. If the *p* is 1.0,
   the function will always return True, or if is 0.0, the
   function will return always False.
   
   Example:
      >>> Util.randomFlipCoin(1.0)
      True

   :param p: probability, between 0.0 and 1.0
   :rtype: True or False

   """
   if p == 1.0: return True
   if p == 0.0: return False
   if rand_random() <= p: return True
   else: return False
   
def listSwapElement(lst, indexa, indexb):
   """ Swaps elements A and B in a list.

   Example:
      >>> l = [1, 2, 3]
      >>> Util.listSwapElement(l, 1, 2)
      >>> l
      [1, 3, 2]

   :param lst: the list
   :param indexa: the swap element A
   :param indexb: the swap element B
   :rtype: None

   """
   temp = lst[indexa]
   lst[indexa] = lst[indexb]
   lst[indexb] = temp

def list2DSwapElement(lst, indexa, indexb):
   """ Swaps elements A and B in a 2D list (matrix).

   Example:
      >>> l = [ [1,2,3], [4,5,6] ] 
      >>> Util.list2DSwapElement(l, (0,1), (1,1) )
      >>> l
      [[1, 5, 3], [4, 2, 6]]

   :param lst: the list
   :param indexa: the swap element A
   :param indexb: the swap element B
   :rtype: None

   """
   temp = lst[indexa[0]][indexa[1]]
   lst[indexa[0]][indexa[1]] = lst[indexb[0]][indexb[1]]
   lst[indexb[0]][indexb[1]] = temp

def raiseException(message, expt=None):
   """ Raise an exception and logs the message.

   Example:
      >>> Util.raiseException('The value is not an integer', ValueError)

   :param message: the message of exception
   :param expt: the exception class
   :rtype: None

   """
   logging.critical(message)
   if expt is None:
      raise Exception(message)
   else:
      raise expt, message

