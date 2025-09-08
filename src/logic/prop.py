from __future__ import annotations

import typing
from dataclasses import dataclass

if typing.TYPE_CHECKING:
    import random


@dataclass(frozen=True, order=True)
class Prop:
    pass


@dataclass(frozen=True, order=True)
class TrueBool(Prop):
    pass


@dataclass(frozen=True, order=True)
class FalseBool(Prop):
    pass


@dataclass(frozen=True, order=True)
class AP(Prop):
    name: str


@dataclass(frozen=True, order=True)
class Not(Prop):
    operand: Prop


@dataclass(frozen=True, order=True)
class And(Prop):
    left: Prop
    right: Prop


@dataclass(frozen=True, order=True)
class Or(Prop):
    left: Prop
    right: Prop


Unary = Not
Binary = And | Or


def str_of_prop(p: Prop) -> str:
    if isinstance(p, TrueBool):
        return "True"
    if isinstance(p, FalseBool):
        return "False"
    if isinstance(p, AP):
        return p.name
    if isinstance(p, Not):
        return f"¬({str_of_prop(p.operand)})"
    if isinstance(p, And):
        return f"({str_of_prop(p.left)}) ∧ ({str_of_prop(p.right)})"
    if isinstance(p, Or):
        return f"({str_of_prop(p.left)}) ∨ ({str_of_prop(p.right)})"
    msg = f"Unknown Prop type: {type(p)}"
    raise TypeError(msg)


def random_ap(all_ap: list[AP], without: AP | None, rand: random.Random) -> AP:
    if without is None:
        return rand.choice(all_ap)
    copied = all_ap.copy()
    copied.remove(without)
    return rand.choice(copied)


def random_binary(left: Prop, right: Prop, rand: random.Random) -> Prop:
    choice = rand.randint(0, 1)
    if choice == 0:
        return And(left, right)
    if choice == 1:
        return Or(left, right)
    msg = f"Invalid choice: {choice}"
    raise ValueError(msg)


def mutate_ap(p: AP, all_ap: list[AP], rand: random.Random) -> Prop:
    choice = rand.randint(0, 1)
    if choice == 0:
        return random_ap(all_ap, p, rand=rand)
    if choice == 1:
        return Not(p)
    msg = f"Invalid choice: {choice}"
    raise ValueError(msg)


def mutate_unary(p: Unary, all_ap: list[AP], rand: random.Random) -> Prop:
    choice = rand.randint(0, 2)
    if choice == 0:
        return mutate(p.operand, all_ap, rand)
    if choice == 1:
        return Not(mutate(p.operand, all_ap, rand))
    if choice == 2:
        return random_binary(
            random_ap(all_ap, None, rand),
            mutate(p.operand, all_ap, rand),
            rand,
        )
    msg = f"Unknown unary Prop type: {type(p)}"
    raise TypeError(msg)


def mutate_binary(_p: Binary, _all_ap: list[AP], _rand: random.Random) -> Prop:
    msg = "Not implemented yet"
    raise NotImplementedError(msg)


def mutate(p: Prop, all_ap: list[AP], rand: random.Random) -> Prop:
    if isinstance(p, TrueBool):
        return FalseBool()
    if isinstance(p, FalseBool):
        return TrueBool()
    if isinstance(p, AP):
        return mutate_ap(p, all_ap, rand)
    if isinstance(p, Unary):
        return mutate_unary(p, all_ap, rand)
    if isinstance(p, Binary):
        return mutate_binary(p, all_ap, rand)
    msg = f"Unknown Prop type: {type(p)}"
    raise TypeError(msg)
