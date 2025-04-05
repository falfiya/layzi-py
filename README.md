# Layzi Python

A [friend from school](https://github.com/Ant-28) mentioned wanting to do lazy
Python and I thought that it would be interesting!

```py
from layzi import lz

def if_then_else(cond, true, false):
   if lz.eval(cond):
      return lz.eval(true)
   else:
      return lz.eval(false)

@lz
a = 1

b = lz(2) # same thing as above

def foo(x):
   print(x)
   return x + 3

@lz.fn
def bar(y):
   print(f"{y}!")
   return foo(y - 3)

c = lz.fn(foo, a) # have to explicitly use lz.fn since foo is not a lazy function
d = bar(b + 9)

if_then_else(True, c, d)
```

## Pseudo-Discussion

<details>
   <summary>What does it mean to be lazy?</summary>

   ...

</details>

<details>
   <summary>How lazy can we be?</summary>

   - we can't be lazy

</details>

<details>
   <summary>Won't this mess with runtime type-checking?</summary>

   Yes, and that's kind of a problem. But there might be a way around it.

</details>


<details>
   <summary>When should a value be considered to be "needed"?</summary>

   ...

</details>

<details>
   <summary>Is it OK to simply store all item accesses via <code>__getitem__</code></summary>

   No. The answer is no.

</details>

## Credits

Thanks to [Peak's Proxy Types](https://github.com/PEAK-Legacy/ProxyTypes) for the idea to use `__slots__` for stuff.
