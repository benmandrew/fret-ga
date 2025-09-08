from __future__ import annotations

import random
from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class Prop:
    pass


@dataclass(frozen=True)
class TrueBool(Prop):
    pass


@dataclass(frozen=True)
class FalseBool(Prop):
    pass


@dataclass(frozen=True)
class AP(Prop):
    name: str


@dataclass(frozen=True)
class Not(Prop):
    operand: Prop


@dataclass(frozen=True)
class And(Prop):
    left: Prop
    right: Prop


@dataclass(frozen=True)
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


def random_ap(ap_set: set[AP], without: AP | None = None) -> AP:
    if without is None:
        return random.choice(list(ap_set))
    return random.choice(list(ap_set - {without}))


def random_binary(left: Prop, right: Prop) -> Prop:
    choice = random.randint(0, 1)
    if choice == 0:
        return And(left, right)
    if choice == 1:
        return Or(left, right)
    msg = f"Invalid choice: {choice}"
    raise ValueError(msg)


def mutate_ap(p: AP, ap_set: set[AP]) -> Prop:
    choice = random.randint(0, 1)
    if choice == 0:
        return random_ap(ap_set, without=p)
    if choice == 1:
        return Not(p)
    msg = f"Invalid choice: {choice}"
    raise ValueError(msg)


def mutate_unary(p: Unary, ap_set: set[AP]) -> Prop:
    choice = random.randint(0, 2)
    if choice == 0:
        return mutate(p.operand, ap_set)
    if choice == 1:
        return Not(mutate(p.operand, ap_set))
    if choice == 2:
        return random_binary(random_ap(ap_set), mutate(p.operand, ap_set))
    msg = f"Unknown unary Prop type: {type(p)}"
    raise TypeError(msg)


def mutate_binary(_p: Binary, _ap_set: set[AP]) -> Prop:
    msg = "Not implemented yet"
    raise NotImplementedError(msg)


def mutate(p: Prop, ap_set: set[AP]) -> Prop:
    if isinstance(p, TrueBool):
        return FalseBool()
    if isinstance(p, FalseBool):
        return TrueBool()
    if isinstance(p, AP):
        return mutate_ap(p, ap_set)
    if isinstance(p, Unary):
        return mutate_unary(p, ap_set)
    if isinstance(p, Binary):
        return mutate_binary(p, ap_set)
    msg = f"Unknown Prop type: {type(p)}"
    raise TypeError(msg)
