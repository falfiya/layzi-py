# Layzi Python

A [friend from school](https://github.com/Ant-28) mentioned wanting to do lazy
Python and I thought that it would be interesting!

His motivations came from wanting to do some form of lazy *"if-then-else"* and
so we discussed ways to make this happen.

## An Example:

```py
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
```

## Questions:

<details>
   <summary>What does it mean to be lazy?</summary>

   When a value is needed, it is evaluated...

</details>

<details>
   <summary>How lazy can we be?</summary>

   - we can't be lazy

</details>

<details>
   <summary>Won't this mess with runtime type-checking?</summary>

   Yes.
   ```py
   x = lz(1)
   if isinstance(x, int):
      print("This will never be called :(")
   ```

   It's unfortunate but there's no way to hook into that behavior.

</details>


<details>
   <summary>When should a value be considered to be "needed"?</summary>

   A value is needed when we can't be lazy. But isn't this a kind of circular
   definition? We can be lazy when a value isn't needed, but when a value is
   needed we can't be lazy.

   In haskell

</details>

<details>
   <summary>Is it OK to simply store all item accesses via <code>__getitem__</code> and then replay them for real at execution time?</summary>

   It's a little more complicated than that. Consider the following code:

   ```py
   class SomeOtherObject:
      def __radd__(self, i: int) -> i:
         return i + 1

   @lz
   x = 1
   y = SomeOtherObject()

   z = x + y
   ```

   Here, when we do x + y, we return a lazy object that assumes `x.__add__` is valid and does not throw `NotImplemented`.
   So we store `x.__add__(y)` and wait to evaluate it later. But in doing so, we bypass the `SomeOtherObject.__radd__`, which would ordinarily have been called in the event that `int.__add__` returns `NotImplemented`.

   The correct course of action is to be less specific: we remember that `x.__add__` was called, but it probably means that the user intended to use the `+` operator, which is not necessarily the same as `x.__add__`.

</details>

## Credits

Thanks to [Peak's Proxy Types](https://github.com/PEAK-Legacy/ProxyTypes) for the idea to use `__slots__` for stuff.
