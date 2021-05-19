---
layout: blog
tags:
 - theorem-proving
 - lean
title: "Solving a functional equation using Lean"
---

Here is a problem from the [2019 Brazil Undergrad MO](https://artofproblemsolving.com/community/c1018411_2019_brazil_undergrad_mo):  
> Find all functions $$f: \mathbb{R} \rightarrow \mathbb{R}$$ satisfying $$ f(x f(y) + f(x)) + f(y^2) = f(x) + y f(x + y)$$

I was curious to see if I could formalize and prove/verify this in [Lean](https://leanprover.github.io/), so here goes.
<!--more-->

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

Similarly - but just simple substitutions - we can show more results:
> $f(x^2) = x f(x)$  
> $f(f(x)) = f(x)$

Division is hard
----------------

The first roadblock was when trying to prove $f(-x) = -f(x)$.
By plugging in $x$ and $-x$ in $f(x^2) = x f(x)$, we get
> $x f(x) = -x f(-x)$

One would trivially cancel out the $x$ here - implicitly using the fact that $f(0) = 0$ - and prove the lemma required.
But in Lean, we need to formalize each step precisely.

First, the lemma itself:
```lean
lemma f_neg_x__eq__neg_f_x  : ∀ f, prop f → 
  ∀ x, f (- x) = - f (x)
```

Now, some basic unfolding and introductions of previous lemmas:
```lean
unfold prop,
intros f H x,
have fxx1 := f_x_sq__eq__x_f_x f H x,
have fxx2 := f_x_sq__eq__x_f_x f H (-x),

-- simplify all equations
simp at *,
rewrite fxx1 at fxx2,
```

We now have `fxx2: x * f x = -(x * f (-x))`. To divide, we must split into two cases - whether $x$ is $0$ or not. The `x = 0` case simplifies directly.

```lean
cases classical.em (x = 0)
{ -- x = 0
  rewrite h,
  simp,
  rewrite f_0__eq__0 f H,
  simp,
},
```

I ended up invoking `euclidean_domain` for the rule `b ≠ 0 → a * b = c → a = c / b`
```lean
{ -- x ≠ 0
  ring at fxx2,
  have H3 : f (x) * x = -f (-x) * x, { rewrite fxx2, ring },
  have H4 := euclidean_domain.eq_div_of_mul_eq_left h H3,
  rewrite euclidean_domain.mul_div_cancel (-f (-x)) h at H4,
  rewrite H4,
  ring,
},
```

Using the same strategy, we can also prove $f(x + y) = f(x) + f(y)$. This means that the function has to be additive.

Final Steps
-----------

Using additivity and the other lemmas, we can rewrite the initial equation as:
> $f(x f(y) + f(x)) + f(y^2) = f(x) + y f(x + y)$  
> $= f(x f(y)) + f(f(x)) + f(y^2) = f(x) + y (f(x) + f(y))$  
> $= f(x f(y)) + f(x) + y f(y) = f(x) + y f(x) + y f(y)$  
> $= f(x f(y)) = y f(x)$  

And now plugging $x = 1$, we get
> $f(f(y)) = y f(1)$  
> $\implies f(y) = y f(1)$

So we know the function is a line through origin. To find $f(1)$, we can use idempotency.
> $f(f(x)) = f(x)$  
> $\implies f(x) f(1) = f(x)$  

This gives that either $f(x) = 0$ forall $x$, or $f(1) = 1$.
We can do case analysis on $f(1) = 0$, to see if there is a non-zero value in the range.
```lean
lemma f1__eq__0_or_1 : ∀ f, prop f →
  (f(1) = 0) ∨ (f(1)  = 1)
:= begin
  intros f H,
  have Hlinear := fx__eq__x_f1 f H (f(1)), -- f(f(1)) = f(1) f(1)
  have Hidemp := f_x__eq_f_f_x f H 1, -- f(f(1)) = f(1)
  rewrite Hlinear at Hidemp, -- f(1)^2 = f(1)
  cases classical.em (f(1) = 0), {
    tauto,
  }, {
    right,
    have H' := @euclidean_domain.eq_div_of_mul_eq_left _ _ (f(1)) (f(1)) (f(1)) h Hidemp,
    field_simp at H',
    exact H',
  }
end
```

That's it! We finally showed that $f(1)$ is either 0 or 1, which gives us the exhaustive solution set.
