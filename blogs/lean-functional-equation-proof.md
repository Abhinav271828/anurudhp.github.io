---
layout: blog
created: 2021-02-22
---

Solving a functional equation using Lean
========================================

Here is a problem from the [2019 Brazil Undergrad MO]():  
> Find all functions $$f: \mathbb{R} \rightarrow \mathbb{R}$$ satisfying $$ f(x f(y) + f(x)) + f(y^2) = f(x) + y f(x + y)$$

I was curious to see if I could formalize and prove/verify this in [Lean](https://leanprover.github.io/), so here goes.

Preparation
-----------

First I encode the given constraint in lean, as a predicate:

```lean
def prop (f : ℝ → ℝ) : Prop := 
  ∀ x y : ℝ, f (x * f (y) + f (x)) + f (y * y) = f (x) + y * f (x + y)
```

So if we prove `prop f` for some `f`, then we have verified that `f` is one solution to the above problem.

First Steps
-----------

Before diving straight into it, I decided to verify two specific trivial solutions: the identity function and the zero function.

```lean
def idf : ℝ → ℝ := λ x, x

example : prop idf :=
begin
  unfold prop idf,
  intros x y,
  ring,
end
```

```lean
def zerof : ℝ -> ℝ := λ x, 0
example : prop zerof :=
begin
  unfold prop zerof,
  intros x y,
  simp,
end
```

These two really turned out to be trivial, and could directly be simplified.

Approach
--------

I am not too familiar with Lean, so I do not know the full power of its tactic and simplification library. I am rather just using this to verify an existing proof, which I found by hand. 

I first prove a bunch of lemmas, and finally show that the above two solutions are the only valid ones.

A few easy lemmas
-----------------

I will skip the proofs here, as they are not very important. In case you are interested, the full proofs can be found [here](https://gist.github.com/anurudhp/9c60e89a5609fa935a5e890c3b9c0aa4).

Plugging in $x = y = 0$ in the given equation, we get: $f(f(0)) = f(0)$
```lean
lemma f_0_0__eq__0 : ∀ f, prop f → 
  f(f(0)) = 0
```

Using the above lemma, and plugging $x = 0, y = 1$, we get $f(0) = 0$
```lean
lemma f_0__eq__0 : ∀ f, prop f → 
  f(0) = 0
```

TODO: FINISH ARTICLE
