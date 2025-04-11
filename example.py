from layzi import lz
import random

x = lz(1.0)
y = x + 10

@lz
def foo(bar: float):
   if bar.is_integer():
      print("it's an integer!")
   return bar - 2

@lz
def ite(cond: bool, true, false):
   if cond:
      return true
   else:
      return false

z = foo(y)

print(ite(random.random() > 0.5, z, y))
