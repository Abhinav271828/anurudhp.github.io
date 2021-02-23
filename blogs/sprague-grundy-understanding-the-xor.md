---
layout: blog
created: 2021-02-23
---

Sprague-Grundy: Why is it XOR?
============

I have always wondered why the _correct_ way to combine [nim games](https://en.wikipedia.org/wiki/Sprague%E2%80%93Grundy_theorem) is taking the XOR of their grundy numbers. But never got around to learning the theory behind it.

Recently, I had a very enlightening conversation with [Siddharth Bhat](https://bollu.github.io). He showed me a very simple and elegant proof for this.

Group Structure in Nim
----------------------

The first observation is that the set of games/game states form a group, under the _combine_ action. In the simple case - where each game is a set of piles - combining is just taking all the piles from both games together. And the generating elements for this group are the single pile games - whose grundy number we know how to compute. 

Now, I still don't know the proof for why the grundy number of a state is the [MEX](https://en.wikipedia.org/wiki/Mex_(mathematics)) of all the child states. But I'll take that fact for granted for now.

**Identity Element** This will be the trivial losing state - the one with no moves. Notice that combining this any number of times with an other state doesn't change the other state.
**Group Action** Concatenating the list of piles/games.
**Associativity + Commutativity** As the order of piles doesn't matter, we get these two properties for free.

### Inverse
Now this is where the magic happens: Each element is its own inverse!

Why? Consider a game $G$. Now when we take the game $G + G$, the second player can always mirror the first player in the opposite pile. This gives a winning strategy for the second player no matter what $G$ is! So we know $G + G$ is losing, which means it has to be $0$, or the identity.

And it turns out, the only group where every element is it's own inverse is the XOR group! Which gives a natural bijection between the game structure and the XOR group.

