from __future__ import annotations

import typing
from dataclasses import dataclass

from src.logic import prop

if typing.TYPE_CHECKING:
    import random


@dataclass(frozen=True, order=True)
class Timing:
    pass


@dataclass(frozen=True, order=True)
class Immediately(Timing):
    pass


@dataclass(frozen=True, order=True)
class AtNextTimepoint(Timing):
    pass


@dataclass(frozen=True, order=True)
class Eventually(Timing):
    pass


@dataclass(frozen=True, order=True)
class Always(Timing):
    pass


@dataclass(frozen=True, order=True)
class Never(Timing):
    pass


@dataclass(frozen=True, order=True)
class Within(Timing):
    t: int


@dataclass(frozen=True, order=True)
class For(Timing):
    t: int


@dataclass(frozen=True, order=True)
class After(Timing):
    t: int


def str_of_timing(timing: Timing) -> str:
    if isinstance(timing, Immediately):
        return "immediately"
    if isinstance(timing, AtNextTimepoint):
        return "at next timepoint"
    if isinstance(timing, Eventually):
        return "eventually"
    if isinstance(timing, Always):
        return "always"
    if isinstance(timing, Never):
        return "never"
    if isinstance(timing, Within):
        return f"within {timing.t} timesteps"
    if isinstance(timing, For):
        return f"for {timing.t} timesteps"
    if isinstance(timing, After):
        return f"after {timing.t} timesteps"
    msg = f"Unknown timing type: {type(timing)}"
    raise TypeError(msg)


def mutate_timing(timing: Timing, rand: random.Random) -> Timing:
    choices: list[type] = [
        Immediately,
        AtNextTimepoint,
        Eventually,
        Always,
        Never,
        Within,
        For,
        After,
    ]
    choices.remove(type(timing))
    choice = rand.choice(choices)
    if choice in {Immediately, AtNextTimepoint, Eventually, Always, Never}:
        result = choice()
        assert isinstance(result, Timing)
        return result
    if choice in {Within, For, After}:
        result = choice(rand.randint(1, 10))
        assert isinstance(result, Timing)
        return result
    msg = "Unreachable"
    raise RuntimeError(msg)


class Requirement:
    def __init__(
        self,
        condition: prop.Prop | None,
        timing: Timing,
        consequent: prop.Prop,
    ) -> None:
        self.condition = condition
        self.timing = timing
        self.consequent = consequent

    def __str__(self) -> str:
        if self.condition is None:
            return f"{str_of_timing(self.timing)}, {prop.str_of_prop(self.consequent)}"
        return (
            f"if {prop.str_of_prop(self.condition)},"
            f" then {str_of_timing(self.timing)},"
            f" {prop.str_of_prop(self.consequent)}"
        )

    def mutate_condition(
        self,
        all_ap: list[prop.AP],
        rand: random.Random,
    ) -> prop.Prop | None:
        # How might we generate a new condition if there is none?
        if self.condition is None or rand.randint(0, 1) == 0:
            return None
        return prop.mutate(self.condition, all_ap, rand)

    def mutate(self, all_ap: list[prop.AP], rand: random.Random) -> Requirement:
        choice = rand.randint(0, 2)
        if choice == 0:
            new_condition = self.mutate_condition(all_ap, rand)
            return Requirement(new_condition, self.timing, self.consequent)
        if choice == 1:
            new_timing = mutate_timing(self.timing, rand)
            return Requirement(self.condition, new_timing, self.consequent)
        if choice == 2:
            new_consequent = prop.mutate(self.consequent, all_ap, rand)
            return Requirement(self.condition, self.timing, new_consequent)
        msg = f"Invalid choice: {choice}"
        raise ValueError(msg)
