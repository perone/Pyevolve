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

import Util
from random import choice as rand_choice

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


   :param name: the slot name
   :param rand_apply: if True, just one of the functions in the slot will be applied, this function is randomly picked.

   """

   def __init__(self, name="Anonymous Function", rand_apply=False):
      """ The creator of the FunctionSlot Class """
      self.funcList = []
      self.slotName = name
      self.rand_apply = rand_apply

   def __getitem__(self, index):
      """ Used to retrieve some slot function index """
      return self.funcList[index]

   def __setitem__(self, index, value):
      """ Used to set the index slot function """
      self.funcList[index] = value      

   def __iter__(self):
      """ Return the function list iterator """
      return iter(self.funcList)

   def setRandomApply(self, flag=True):
      """ Sets the random function application, in this mode, the
      function will randomly choose one slot to apply

      :param flag: True or False

      """
      self.rand_apply = flag
   
   def getFunction(self, index=0):
      """ Return the function handle at index

      :param index: the index of the function

      """
      return self.funcList[index]

   def clear(self):
      """ Used to clear the functions in the slot """
      if len(self.funcList) > 0:
         del self.funcList[:]

   def add(self, func):
      """ Used to add a function to the slot

      :param func: the function to be added in the slot

      """
      self.funcList.append(func)

   def isEmpty(self):
      """ Return true if the function slot is empy """
      return (len(self.funcList) == 0)

   def set(self, func):
      """ Used to clear all functions in the slot and add one

      :param func: the function to be added in the slot

      .. note:: the method *set* of the function slot remove all previous
                functions added to the slot.
      """
      self.clear()
      self.add(func)

   def apply(self, index, obj, **args):
      """ Apply the index function

      :param index: the index of the function
      :param obj: this object is passes as parameter to the function
      :param args: this args dictionary is passed to the function   

      """
      if len(self.funcList) <= 0:
         raise Exception("No function defined: " + self.slotName)
      return funcList[index](obj, **args)
      
   def applyFunctions(self, obj, **args):
      """ Generator to apply all function slots in obj

      :param obj: this object is passes as parameter to the function
      :param args: this args dictionary is passed to the function   

      """
      if len(self.funcList) <= 0:
         raise Exception("No function defined: " + self.slotName)
      if not self.rand_apply:
         for f in self.funcList:
            yield f(obj, **args)
      else:
         yield rand_choice(self.funcList)(obj, **args)

   def __repr__(self):
      """ String representation of FunctionSlot """
      strRet = "Slot [%s] (Count: %d)\n" % (self.slotName, len(self.funcList))

      if len(self.funcList) <= 0:
         strRet += "\t\tNo function\n"
         return strRet

      for f in self.funcList:
         strRet += "\t\tName: " + f.func_name + "\n"
         if f.func_doc:
            strRet += "\t\tDoc: " + f.func_doc + "\n"

      return strRet
