---
layout: blog
created: 2021-05-17
blog: true
tags:
  - haskell
---

Advent Of Code 2020 - in Haskell
================================

A few months ago, I was introduced to the [Advent Of Code](https://adventofcode.com/2020) contest series. The 2020 round has just begun, and looking at the problems from previous years, I felt it would be fun and challenging to program them in Haskell. And so I got to work and got 40 out of 50 stars at the end. This was incredibly fun, and surprisingly difficult at certain stages, and I want to share my thoughts with others.

I have put up my [solutions on GitHub](https://github.com/anurudhp/AdventOfCode2020).

Elegant Solutions
-----------------

It is really amazing how elegant Haskell solutions look, usually with very less effort.
```haskell
-- Given list of ints `xs`, find the product of some triple (x, y, z) of elements of `xs` that sum to 2020.
solve :: [Int] -> Int
solve xs = head [x * y * z | x <- xs, y <- xs, z <- xs, x + y + z == 2020]
```

Though one might dismiss this as some syntactic sugar, it is much more than that. List comprehensions in Haskell are a specific case of [Monad comprehensions](https://ghc.gitlab.haskell.org/ghc/doc/users_guide/exts/monad_comprehensions.html), which are an important aspect of Haskell's pure design.

Text Parsing
------------

Lexing and parsing text is a big pain, and providing easy-to-use libraries for this is very difficult. I have previously used [Flex](https://en.wikipedia.org/wiki/Flex_(lexical_analyser_generator)) and [GNU Bison](https://www.gnu.org/software/bison/) for implementing a compiler, and it is a nightmare to use them.

Haskell makes life simpler (in some cases) by providing parser combinators as part of the [`Text.Parsec`](https://hackage.haskell.org/package/parsec) package. This helps write very beautiful monadic parsing code, which quite closely resembles imperative code, while still being pure.

Here is a snippet from the [solution](https://github.com/anurudhp/AdventOfCode2020/blob/master/src/day21.hs) for [Day 13](https://adventofcode.com/2020/day/21). This parses input of the form `mxmxvkd kfcds sqjhc nhms (contains dairy, fish)`.

```haskell
type Ingredient = String
type Allergen = String
type Dish = ([Ingredient], [Allergen])
type Input = [Dish]

mkDish :: String -> Dish
mkDish = either undefined id . parse parseDish ""
  where
    parseDish = (,) <$> fil parseIngredients <*> fil parseAllergens
    parseIngredients = parseWord `sepBy1` space
    parseAllergens =
      string "(contains " *> (parseWord `sepBy1` string ", ") <* char ')'
    parseWord = many $ choice [char c | c <- ['a' .. 'z']]
    fil = fmap (filter (not . null))
```

More
----

There are a lot more interesting patterns one can observe in the solutions/implementation. It has been a while since I did the contest, so I may have forgotten some things. I will update this post later if I remember.
