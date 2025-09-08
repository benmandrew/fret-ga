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


@dataclass(frozen=True)
class Implies(Prop):
    left: Prop
    right: Prop


def str_of_prop(prop: Prop) -> str:
    if isinstance(prop, TrueBool):
        return "True"
    if isinstance(prop, FalseBool):
        return "False"
    if isinstance(prop, AP):
        return prop.name
    if isinstance(prop, Not):
        return f"¬({str_of_prop(prop.operand)})"
    if isinstance(prop, And):
        return f"({str_of_prop(prop.left)}) ∧ ({str_of_prop(prop.right)})"
    if isinstance(prop, Or):
        return f"({str_of_prop(prop.left)}) ∨ ({str_of_prop(prop.right)})"  # noqa: RUF001
    if isinstance(prop, Implies):
        return f"({str_of_prop(prop.left)}) → ({str_of_prop(prop.right)})"
    msg = f"Unknown Prop type: {type(prop)}"
    raise TypeError(msg)
