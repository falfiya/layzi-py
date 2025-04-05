from typing import *

T = TypeVar("T")
Ts = TypeVarTuple("Ts")
U = TypeVar("U")

# see https://docs.python.org/3/reference/datamodel.html#special-method-names
# to learn more about special methods

class LzMethod(Generic[T]):
   ...

class LzAction:
   __slots__ = ()
   def eval(self, imm):
      """
      Applies the action to the immediate (non-lazy) value.
      """

class LzAdd1(LzAction):
   """
   lz + val
   """
   __slots__ = "__right__"
   def __init__(self, right):
      self.__right__ = right

   def eval(self, imm):
      return imm + self.__right__

class LzAdd2:
   """
   val + lz

   This is only triggered when val doesn't know what to do with a lazy object.
   We hope that val.__add__ returns NotImplemented all the time so that we can
   take control over the addition.
   """
   __slots__ = "__left__"
   def __init__(self, left):
      self.__left__ = left

   def eval(self, imm):
      return imm + self.__left__

class LzValue(Generic[T]):
   __slots__ = "__subject__", "__chain__"

   def __init__(self, val: T, chain: tuple[LzAction] = ()):
      self.__subject__: T = val
      self.__chain__: tuple[LzAction] = chain

   def __call__(self, *args, **kwargs):
      return self.__subject__(*args, **kwargs)

def lz():
   """
   Create a lazy value or function.

   If you want to control the behavior, use `lz.val` and `lz.fn`.
   """

def app():
   """
   Applies a function to a value (lazy or non lazy) lazily
   """

def imm(fn: Callable[[*Ts], U]) -> Callable[[*Ts], U]:
   """
   Decorator for a function to force the evaluation of lazy arguments.
   """
   ...
