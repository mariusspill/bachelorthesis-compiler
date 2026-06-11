# Exercise 9

Your task is to extend the compiler to support peephole optimizations.

As always we already modified the interpreter, type checker, and syntax trees for you, so that you only have to extend the compiler passes.

The following is a description of the non-trivial changes that have to be done to extend the compiler. Any change marked with a `TODO` will be your task to complete.

## Optimize

We introduce a new pass `pass_10_10_optimize` which implements the peephole optimizations.

- `TODO`: Any instruction `Instr2 op dst x y` where `x` and `y` are constants should be replaced by an equivalent move instruction. You may use the helper functions `simulate_over_and_underflow` and `to_int_64` when necessary.

- `TODO`: Any instruction `Instr2 op dst x y` where `y` is a constant and the operation being executed is
    - `x + 0`
    - `x - 0`
    - `x * 1`
    - `x // 1`
    - `x * 0`

    should be replaced by an equivalent move instruction.

- `TODO`: Any instruction `Branch cc x y target` where `x` and `y` are constants should be replaced by a jump instruction or removed, depending on which is equivalent. Make sure that jump instructions only appear at the end of blocks so that no unreachable instructions remain.

- `TODO`: Removing branch instructions might make some of the basic blocks unreachable, so filter out all unreachable blocks from the set of basic blocks for each function after applying the peephole optimizations.

- `TODO`: Any instruction `Move x x` should be removed.

- `TODO`: Any instruction `Move y x` directly preceded by `Move x y` should be removed. Make sure that removing a move instruction does not leave behind another possibilty for removal.

##

If stuff is unclear, don't hesitate to use the chat!

*Happy Coding! <3*
