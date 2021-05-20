---
layout: blog
title: "Haskell in C++: Implementing pure functional constructs in c++ using templates"
tags:
  - haskell
  - c++
  - metaprogramming
---

When I first learnt Haskell a while back, I found it difficult to adjust my thinking to the pure-functional style. Especially because I have been coding in imperative languages for more than 7 years before that. It took me a while to fully grasp and appreciate the elegance of these constructs in Haskell, like functors and monads. At some point, I attempted to implement the same constructs in C++, to help my understanding, and get a feel of the expressive power Haskell has.

<!--more-->

Prerequisites
-------------

I am assuming basic knowledge of both c++ (with templates) and Haskell. I will be using `clang++ 11.0.0; c++17` and `ghc 8.10.4`, but I believe most of these should work on any compiler/version.

First blood: Basic Types
------------------------

Before we dive deep, it is good to rewrite some simple concepts - such as standard types - to ensure we are on the right track.

<div class="row"><div class="col-xs-12 col-sm-6">
```haskell
type Int
```
</div><div class="col-xs-12 col-sm-6">
```c++
struct Int { int value; }
```
</div></div>
