---
layout: blog
created: 2021-03-07
blog: true
tags:
  - c++
  - metaprogramming
---

A calculator in C++ - at compile time!
============

Calculator programs are usually one of the first practice programs people implement. And writing a basic one in c++ is pretty straightforward. But today, I'll demonstrate how to use your compiler (say `gcc` or `clang`) as a calculator!

Extremely strong typing
-----------------------

C++ is a statically typed language. That is, each object in it has a well defined type at compile time. This is unlike, say python, where the types of objects need not be determinable at compile time.

Now we'll define an even stricter integer type in C++:
```cpp
template<int N> struct Integer { };
```

Here, `Integer` is a templatized type with no members. For example, an object of type `Integer<0>` is just an empty object. This is unlike the usual `int` type, where objects of the type could take any `int` value (in the appropriate range).

First operation: Addition
--------

Now we define how to add two `Integer<N>` objects.

```cpp
template<int N, int M>
Integer<N + M> add(Integer<N> n, Integer<M> m) {
  return Integer<N + M>();
}
```

Here, the add function takes two `Integer<>` objects, and returns another. But notice how it deduces the type of the result!

For example:
```cpp
Integer<2> two;
Integer<3> three;
Integer<5> five = add(two, three); // OK
Integer<6> six = add(two, three); // compile error!
```

By making our types extremely strict (one type for each integer value), we can force the compiler to do _arithmetic_ at compile time!

We can overload the `+` operator for better expressivity.
```cpp
template<int N, int M>
Integer<N + M> operator+(Integer<N> n, Integer<M> m) {
  return Integer<N + M>();
}

auto six = three + three; // typeof(six) == Integer<6>
```

More operations
---------------
Extending this is pretty simple, just define more operators just like we did above.

```cpp
template<int N, int M>
Integer<N * M> operator*(Integer<N> n, Integer<M> m) {
  return Integer<N * M>();
}
```

Takeaways
---------
We are used to drawing a clear distinction between _compilation_ and _execution_. The above exercise just demonstrates that they are not so different, and in fact the exact same thing! We just artificially split the total process into two phases, for improved efficiency or ease of use etc.

For instance, c++ does more type checking at compile time than python, while python defers it to runtime. Different languages choose different boundaries for the two, based on the trade-offs.

Challenge 
---------
We saw how to pull arithmetic from runtime to compile time in c++. 

Now try to push some process from compile time to runtime: **Can you create python-like objects in C++?** (i.e. no type checking at compile time)
