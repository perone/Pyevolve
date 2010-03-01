"""
:mod:`FunctionSlot` -- function slots module
==================================================================

The *function slot* concept is large used by Pyevolve, the idea
is simple, each genetic operator or any operator, can be assigned
to a slot, by this way, we can add more than simple one operator,
we can have for example, two or more mutator operators at same time,
two or more evaluation functions, etc. In this :mod:`FunctionSlot` module,
you'll find the class :class:`FunctionSlot.FunctionSlot`, which is the slot class.

"""

from random import uniform as rand_uniform
import inspect
from types import BooleanType

import Util

class FunctionSlot:
   """ FunctionSlot Class - The function slot

   Example:
      >>> genome.evaluator.set(eval_func)
      >>> genome.evaluator[0]
      <function eval_func at 0x018C8930>
      >>> genome.evaluator
      Slot [Evaluation Function] (Count: 1)
                Name: eval_func
      >>> genome.evaluator.clear()
      >>> genome.evaluator
      Slot [Evaluation Function] (Count: 0)
                No function

   You can add weight to functions when using the `rand_apply` paramter:
      >>> genome.evaluator.set(eval_main, 0.9)
      >>> genome.evaluator.add(eval_sec,  0.3)
      >>> genome.evaluator.setRandomApply()

   In the above example, the function *eval_main* will be called with 90% of
   probability and the *eval_sec* will be called with 30% of probability.

   There are another way to add functions too:
      >>> genome.evaluator += eval_func

   :param name: the slot name
   :param rand_apply: if True, just one of the functions in the slot
                      will be applied, this function is randomly picked based
                      on the weight of the function added.

   """

   def __init__(self, name="Anonymous Function", rand_apply=False):
      """ The creator of the FunctionSlot Class """
      self.funcList = []
      self.funcWeights = []
      self.slotName = name
      self.rand_apply = rand_apply

   def __typeCheck(self, func):
      """ Used internally to check if a function passed to the
      function slot is callable. Otherwise raises a TypeError exception.
  
      :param func: the function object
      """
      if not callable(func):
         Util.raiseException("The function must be a method or function", TypeError)

   def __iadd__(self, func):
      """ To add more functions using the += operator
      
         .. versionadded:: 0.6
            The __iadd__ method.
      """
      self.__typeCheck(func)
      self.funcList.append(func)
      return self

   def __getitem__(self, index):
      """ Used to retrieve some slot function index """
      return self.funcList[index]

   def __setitem__(self, index, value):
      """ Used to set the index slot function """
      self.__typeCheck(value)
      self.funcList[index] = value      

   def __iter__(self):
      """ Return the function list iterator """
      return iter(self.funcList)

   def __len__(self):
      """ Return the number of functions on the slot

      .. versionadded:: 0.6
         The *__len__* method
      """
      return len(self.funcList)

   def setRandomApply(self, flag=True):
      """ Sets the random function application, in this mode, the
      function will randomly choose one slot to apply

      :param flag: True or False

      """
      if type(flag) != BooleanType:
         Util.raiseException("Random option must be True or False", TypeError)

      self.rand_apply = flag
   
   def clear(self):
      """ Used to clear the functions in the slot """
      if len(self.funcList) > 0:
         del self.funcList[:]

   def add(self, func, weight=0.5):
      """ Used to add a function to the slot

      :param func: the function to be added in the slot
      :param weight: used when you enable the *random apply*, it's the weight
                     of the function for the random selection

      .. versionadded:: 0.6
         The `weight` parameter.

      """
      self.__typeCheck(func)
      self.funcList.append(func)
      self.funcWeights.append(weight)

   def isEmpty(self):
      """ Return true if the function slot is empy """
      return (len(self.funcList) == 0)

   #def __call__(self, *args):
   #   """ The callable method """

   def set(self, func, weight=0.5):
      """ Used to clear all functions in the slot and add one

      :param func: the function to be added in the slot
      :param weight: used when you enable the *random apply*, it's the weight
                     of the function for the random selection

      .. versionadded:: 0.6
         The `weight` parameter.

      .. note:: the method *set* of the function slot remove all previous
                functions added to the slot.
      """
      self.clear()
      self.__typeCheck(func)
      self.add(func, weight)

   def apply(self, index, obj, **args):
      """ Apply the index function

      :param index: the index of the function
      :param obj: this object is passes as parameter to the function
      :param args: this args dictionary is passed to the function   

      """
      if len(self.funcList) <= 0:
         raise Exception("No function defined: " + self.slotName)
      return self.funcList[index](obj, **args)
      
   def applyFunctions(self, obj=None, **args):
      """ Generator to apply all function slots in obj

      :param obj: this object is passes as parameter to the function
      :param args: this args dictionary is passed to the function   

      """
      if len(self.funcList) <= 0:
         Util.raiseException("No function defined: " + self.slotName)
      
      if not self.rand_apply:
         for f in self.funcList:
            yield f(obj, **args)
      else:
         v = rand_uniform(0, 1)
         fobj = None
         for func, weight in zip(self.funcList, self.funcWeights):
            fobj = func
            if v < weight:
               break
            v = v - weight

         yield fobj(obj, **args)

   def __repr__(self):
      """ String representation of FunctionSlot """
      strRet = "Slot [%s] (Count: %d)\n" % (self.slotName, len(self.funcList))

      if len(self.funcList) <= 0:
         strRet += "\t\tNo function\n"
         return strRet

      for f, w in zip(self.funcList, self.funcWeights):
         strRet += "\t\tName: %s - Weight: %.2f\n" % (f.func_name, w)
         if f.func_doc:
            strRet += "\t\tDoc: " + f.func_doc + "\n"

      return strRet
