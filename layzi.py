from typing import *

T = TypeVar("T")
U = TypeVar("U")
Ts = TypeVarTuple("Ts")

# see https://docs.python.org/3/reference/datamodel.html#special-method-names
# to learn more about special methods
GA = object.__getattribute__
SA = object.__setattr__

class LzValue(Generic[T]):
   """
   Not very threadsafe
   """

   __slots__ = "__subject__", "__computed__"

   def __init__(self, subject: T):
      SA(self, "__subject__", subject)
      SA(self, "__computed__", False)

   def imm(self):
      """
      Caching imm with preparation of subject
      """
      subject = GA(self, "__subject__")

      if not GA(self, "__computed__"):
         # this does not re
         subject = imm(subject)

         subject = GA(self, "__imm__")(subject)

         SA(self, "__subject__", subject)
         SA(self, "__computed__", True)

      return subject

   def __imm__(self, subject):
      return subject

   def __call__(self, *args, **kwargs):
      return LzCall(self, args, kwargs)

   # technically we can do better...
   # def __iter__(self):
   #    ...

   # def __reversed__(self):
   #    ...

   def __divmod__(self, other):
      return (self / other, self % other)

   def __rdivmod__(self, other):
      return (GA(self, "__rdiv__")(other), GA(self, "__rmod__")(other))

   #############################################################################
   # Codegen Below :(                                                          #
   #############################################################################
      # if you call any of these methods, it evaluates the lazy value immediately
   __immediate_methods__ = (
      "__repr__", "__str__", "__bytes__", "__format__", "__hash__", "__bool__",
      "__dir__", "__isinstance__", "__len__", "__length_hint__", "__contains__",
      "__enter__", "__exit__", "__buffer__", "__release_buffer__", "__await__",
      "__iter__", "__reversed__", # too lazy to do these two
   )
   for name in __immediate_methods__:
      exec(""
         + f"def {name}(self, *args, **kwargs):\n"
         + f'   return GA(self, "imm")().{name}(*args, **kwargs)\n'
      )

   __no_proxy__ = __immediate_methods__ + (
      "__call__", "__iter__", "__reversed__", "__divmod__"
   )

   __operators__ = (
      "Add,+,l", "RAdd,+,r", "Sub,-,l", "RSub,-,r", "Mul,*,l", "RMul,*,r",
      "Matmul,@,l", "RMatmul,@,r", "Truediv,/,l", "RTruediv,/,r",
      "Floordiv,//,l", "RFloordiv,//,r", "Mod,%,l", "RMod,%,r", "Pow,**,l",
      "RPow,**,r", "LShift,<<,l", "RLShift,<<,r", "RShift,<<,l",
      "RRShift,<<,r", "And,&,l", "RAnd,&,r", "Xor,^,l", "RXor,^,r", "Or,|,l",
      "ROr,|,r",
   )
   for pair in __operators__:
      name, op, lr = pair.split(",")
      realname = f"__{name.lower()}__"
      exec(""
         + f"def {realname}(self, other):\n"
         + f"   return Lz{name}(self, other)"
      )
      __no_proxy__ += (realname, )

   # immediate fields require the computation of the underlaying
   __immediate_fields__ = ("__mro_entries__")
   def __getattribute__(self, name):
      """
      This doesn't stop stuff like type()
      """
      if name in LzValue.__no_proxy__:
         return GA(self, name)

      if name in LzValue.__immediate_fields__:
         return GA(GA(self, "imm")(), name)
      else:
         return LzAttrib(self, name)

def imm(val):
   if issubclass(type(val), LzValue):
      return GA(val, "imm")()
   else:
      return val

class LzAttrib(LzValue):
   __slots__ = "__name__"

   def __init__(self, subject, name: str):
      super().__init__(subject)
      SA(self, "__name__", name)

   def __imm__(self, subject):
      return GA(subject, GA(self, "__name__"))

class LzCall(LzValue):
   __slots__ = "__args__", "__kwargs__"

   def __init__(self, subject, args, kwargs):
      super().__init__(subject)
      SA(self, "__args__", args)
      SA(self, "__kwargs__", kwargs)

   def __imm__(self, subject):
      return subject(*GA(self, "__args__"), **GA(self, "__kwargs__"))

for pair in LzValue.__operators__:
   name, op, lr = pair.split(",")
   code = (""
      + f"class Lz{name}(LzValue):\n"
      + f"   __slots__ = '__other__'\n"
      + f"   def __init__(self, subject, other):\n"
      + f"      super().__init__(subject)\n"
      + f"      SA(self, '__other__', other)\n"
      + f"   def __imm__(self, subject):\n"
      + f""
   )
   if lr == "r":
      code += f"      return subject + GA(self, '__other__')\n"
   else:
      code += f"      return GA(self, '__other__') + subject\n"
   exec(code)

def lz(v: T) -> T:
   """
   Create a lazy value or function.
   """
   return LzValue(v)

def un(fn: Callable[[*Ts], U]) -> Callable[[*Ts], U]:
   def wrapper(*args, **kwargs):
      imm(fn(*args, **kwargs))
   return wrapper

def app(fn: Callable[[*Ts], U], *args: *Ts) -> U:
   """
   Applies a function to a value (lazy or non lazy) lazily
   """
   return LzCall(fn, *args)

lz.un = un
lz.app = app
