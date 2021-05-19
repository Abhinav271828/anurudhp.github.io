---
layout: blog
created: 2021-02-23
tags:
  - game-theory
  - algebra
---

Sprague-Grundy: Why is it XOR?
============

I have always wondered why the _correct_ way to combine [nim games](https://en.wikipedia.org/wiki/Sprague%E2%80%93Grundy_theorem) is taking the XOR of their grundy numbers. But never got around to learning the theory behind it.

Recently, I had a very enlightening conversation with [Siddharth Bhat](https://bollu.github.io). He showed me a very simple and elegant proof for this.

Definitions
-----------

### [Nim Game](https://en.wikipedia.org/wiki/Nim)
There are a set of piles. Each pile could be a stack of coins or a [tree](https://en.wikipedia.org/wiki/Tree_(graph_theory)) etc.  
Two players play a game - in a move a player chooses a particular pile and removes some number of coins or nodes. The exact game will define which moves are allowed. The player who cannot play a move loses.

Assuming both players play optimally, we want to find who wins a game.

### Solving a single pile
We assign each state of a pile a non-negative integer value - called its _grundy number_. A losing state will have a grundy number of 0, and winning states will have a non-zero value.

To compute the _grundy number_ of a state, we take the minimum excluded value among the grundy numbers of all states you can reach by playing _one move_.
> $$MEX(S) = min_x(x \not \in S)$$

Notice that the trivial losing state - one where there are no moves left - gets a grundy number of 0.

P.s. Now, I still don't know the proof for why the grundy number of a state is the [MEX](https://en.wikipedia.org/wiki/Mex_(mathematics)) of all the child states. But I'll take that fact for granted for now. I do hope to learn it someday, and will write about it then.

Group Structure in Nim
----------------------

Now let us consider the set of all nim games. Each game is a collection of a certain number of (possibly-zero) piles. We can think of a game as an _unordered multiset of piles_

Now I define a _binary operation_ $\oplus$ on the games: take the union (keeping duplicates). Notice that this operation has the following properties:

- **Closed**: Combining two games just gives us a larger set of piles. Which is also a game.
- **Identity Game**: The empty set of piles is a valid game. And when combined with any other game $G$, you get back $G$.
- **Commutativity**: As we are taking unordered unions, the order of combining does not matter. I.e. $G \oplus G' = G' \oplus G$
- **Associativity**: Again as the order does not matter, we get this for free as well.

So we see that $(G, \oplus)$ forms an abelian [monoid](https://en.wikipedia.org/wiki/Monoid)!

We can think of each element in $G$ as a _grundy number_ for that game. And the binary operation combines two numbers giving another grundy number.

### Inverse
Now this is where the magic happens: Each element is its own inverse!

**Why?**  
Consider a game $G$. Now when we take the game $G' = G \oplus G$, the second player can always mirror the first player in the opposite pile. This gives a winning strategy for the second player no matter what $G$ is!  
As there is only one losing element - $0$ - we get that $G' = 0$.

So this means that $(G, \oplus)$ is an abelian group where each element is its own inverse. Why is this special? Because there is only one group (up to isomorphism) satisfying this property: the XOR group!  

This gives us an isomorphism between the game group and the XOR group. And turns out that mapping is just the _grundy numbers_. More on that later!
