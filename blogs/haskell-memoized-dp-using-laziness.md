---
layout: blog_lhs
created: 2021-05-12
blog: true
tags:
  - haskell
  - competitive programming
---

# \[Haskell for CP\] Exploiting laziness for memoized DPs

## Problem

[Partition
Problem](https://en.wikipedia.org/wiki/Partition_(number_theory)) -
Compute the number of partitions for a given integer $n$ - ways of
writing n as a sum of positive integers. Two sums that differ only in
the order of their summands are considered the same partition.

## Solution

This is a fairly standard problem, solved using a recurrence.

Let $P(n, x)$ be the number of partitions of $n$, such that the smallest
element in it is $x$. We define this recurrence for $n \geq 1$ and
$x \geq 1$.

$$
P(n, x) \equiv
\begin{cases}
\sum_{y = x}^{n - x} P(n - x, y) & x < n \\
1 & x = n \\
0 & x > n \\
\end{cases}
$$

Note: An empty summation is $0$.

## Counting

We define a list of lists $dp$, to store the computed values.

``` haskell
-- a "two dimensional" memory/array; realized as a list of lists.
type Mem2D a = [[a]]

-- the memoized values of the recurrence $P$
-- P(n, x) = dp !! n !! x
dp :: Mem2D Integer

-- compute P(n, x)
getP :: Int -> Int -> Integer
getP n x = dp !! n !! x -- extract the corresponding element

-- #partitions of n
partitions :: Int -> Integer
partitions n = sum $ dp !! n
```

Notice that $dp$ here is not a function, just a global constant list!
But unlike usual programming languages, we can give Haskell a recipe to
compute the elements of the list, which in turn can use previous
elements. This works because Haskell is lazily evaluated.

Implementation trick: We only store non-trival values. The zeros (for
the $x > n$ case) are not stored.\
To compute `dp[n][x]`, we implement the above recurrence:

``` haskell
sum -- Add all the values, i.e. dp[n - x][x ..]
  $ drop x -- drop the first x values. i.e. dp[n - x][0 .. x - 1]
    $ dp !! (n - x) -- Take dp[n - x]
```

Now let us put this together and build the entire $dp$ list.

``` haskell
dp =
  [] : -- dp[0]
  [ 0 : -- dp[n][0] (padding, unused)
    [sum $ drop x $ dp !! (n - x) -- dp[n][1..n - 1]
    | x <- [1 .. n - 1]
    ]
    ++ [1] -- dp[n][n]
  | n <- [1 ..]
  ]
```

That is it! Just a few lines to compute all the dp values! In Haskell,
when a list is forced, it either evaluates to `[]` or to `x : xs`, where
`xs` is not forced yet. So the computation forces one element at a time,
which nicely preserves the order of computation. This ensures that the
`dp` results for smaller $n$ values are computed first.

``` haskell
ghci> take 5 dp
[[],[0,1],[0,1,1],[0,2,0,1],[0,3,1,0,1]]
ghci> dp !! 6
[0,7,2,1,0,0,1]
ghci> dp !! 5 !! 1 -- same as `getP 5 1`
5 -- the sequences are: (1, 1, 1, 1, 1); (1, 1, 1, 2); (1, 1, 3); (1, 2, 2); (1, 4)
ghci> partitions 5
6
```

## Bonus: Compute all partitions

We can extend the above code to not just count the partitions, but to
actually compute all of them. Instead of adding up the subproblem
counts, we take the subproblem partition lists, and prepend the current
element $x$ to it.

First, let us declare some types and the `sequences` array.

``` haskell
type Partition = [Int] -- A single partition, just a list.
type Partitions = [Partition] -- A collection of partitions.

-- sequences !! n !! x - list of all partitions of n with smallest value x
sequences :: Mem2D Partitions

-- collect all partitions of n
allPartitions :: Int -> Partitions
allPartitions n = concat $ sequences !! n
```

To compute all partitions of $n$ with smallest value $x$, we write
something similar:

``` haskell
map (x :) -- prepend `x` to each of those partitions
  -- now we have a big list of all partitions of `n - x`, starting with any y >= x
  $ concat -- concatenate all the lists corresponding to different starting values
    -- now we have multiple lists, each list contains a set of partitions
    $ drop x -- drop the ones starting with values < x
      $ sequences !! (n - x) -- partitions of n starting with x
```

Putting it together:

``` haskell
sequences =
  [] : -- partitions of 0 (empty, just for padding)
  [ [] : -- partitions of n starting with 0 (empty, just for padding)
    [ map (x :) $ concat $ drop x $ sequences !! (n - x) -- partitions of n starting with x
    | x <- [1 .. n - 1]
    ]
    ++ [[[n]]] -- partitions of n starting with n - only one partition: (n)
  | n <- [1 ..]
  ]
```

A few example values evaluated in the interpreter:

``` haskell
ghci> take 5 sequences
[[],
 [[],[[1]]],
 [[],[[1,1]],[[2]]],
 [[],[[1,1,1],[1,2]],[],[[3]]],
 [[],[[1,1,1,1],[1,1,2],[1,3]],[[2,2]],[],[[4]]]
]
ghci> sequences !! 5
[[],
 [[1,1,1,1,1],[1,1,1,2],[1,1,3],[1,2,2],[1,4]],
 [[2,3]],
 [],
 [],
 [[5]]
]
ghci> allPartitions 5
[[1,1,1,1,1],
 [1,1,1,2],
 [1,1,3],
 [1,2,2],
 [1,4],
 [2,3],
 [5]
]
```
