# FRET Genetic Algorithm

Modifying FRETish requirements using a genetic algorithm inspired by [1]. Two genetic operators are defined: *mutation* and *crossover*.

## Mutation

Mutation takes a single part of a FRETish requirement, either the condition, timing, or consequent, and randomly mutates it. The condition and consequent can be mutated according to the propositional mutations described in [1], and the timing can be mutated by choosing any timing, with a random time parameter if needed.

For example, `if x, then always, (¬(y)) ∧ (x)` could be mutated to any of the following:

```
if x, then after 7 timesteps, (¬(y)) ∧ (x)
if x, then always, ((y) ∧ (z)) ∧ (y)
if z, then always, (¬(y)) ∧ (x)
if x, then never, (¬(y)) ∧ (x)
always, (¬(y)) ∧ (x)
```

## Crossover

Crossover takes two FRETish requirements, and produces a third that takes subformulae of the conditions and consequents, as well as one of the timings. This is yet to be implemented.

---

[1]: Brizzio, M., et al. (2023). *Automated Repair of Unrealisable LTL Specifications Guided by Model Counting*. Proceedings of the Genetic and Evolutionary Computation Conference, 1499–1507. https://doi.org/10.1145/3583131.3590454
