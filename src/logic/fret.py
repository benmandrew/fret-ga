from __future__ import annotations

from dataclasses import dataclass

from src.logic import prop


@dataclass(frozen=True, order=True)
class Timing:
    pass


@dataclass(frozen=True)
class Immediately(Timing):
    pass


@dataclass(frozen=True)
class AtNextTimepoint(Timing):
    pass


@dataclass(frozen=True)
class Eventually(Timing):
    pass


@dataclass(frozen=True)
class Always(Timing):
    pass


@dataclass(frozen=True)
class Never(Timing):
    pass


@dataclass(frozen=True)
class Within(Timing):
    t: int


@dataclass(frozen=True)
class For(Timing):
    t: int


@dataclass(frozen=True)
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
        return f"within {timing.t}"
    if isinstance(timing, For):
        return f"for {timing.t}"
    if isinstance(timing, After):
        return f"after {timing.t}"
    msg = f"Unknown timing type: {type(timing)}"
    raise TypeError(msg)


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
            return f"{str_of_timing(self.timing)} {prop.str_of_prop(self.consequent)}"
        return (
            f"if {prop.str_of_prop(self.condition)},"
            f" then {str_of_timing(self.timing)}"
            f" {prop.str_of_prop(self.consequent)}"
        )
