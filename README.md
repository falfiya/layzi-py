# Layzi Python

A [friend from school](https://github.com/Ant-28) mentioned wanting to do lazy
Python and I thought that it would be interesting!

His motivations came from wanting to do some form of lazy *"if-then-else"* and
so we discussed ways to make this happen.

## An Example:

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

## Questions:

<details>
   <summary>What does it mean to be lazy?</summary>

   When a value is needed, it is evaluated. 

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

   A value is needed when we can't be lazy. But isn't this a kind of circular
   definition? We can be lazy when a value isn't needed, but when a value is
   needed we can't be lazy.

   

</details>

<details>
   <summary>Is it OK to simply store all item accesses via <code>__getitem__</code></summary>

   No. The answer is no.

</details>

## Credits

Thanks to [Peak's Proxy Types](https://github.com/PEAK-Legacy/ProxyTypes) for the idea to use `__slots__` for stuff.
