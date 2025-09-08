import random
import unittest

from src.logic import fret, prop


class TestFretToString(unittest.TestCase):
    def test_requirement_immediately(self) -> None:
        p = prop.And(prop.AP("foo"), prop.Not(prop.AP("bar")))
        req = fret.Requirement(None, fret.Immediately(), p)
        self.assertEqual(str(req), "immediately, (foo) ∧ (¬(bar))")

    def test_requirement_eventually(self) -> None:
        p = prop.AP("bar")
        req = fret.Requirement(None, fret.Eventually(), p)
        self.assertEqual(str(req), "eventually, bar")

    def test_requirement_with_condition(self) -> None:
        cond = prop.AP("foo")
        cons = prop.AP("bar")
        req = fret.Requirement(cond, fret.Always(), cons)
        self.assertEqual(str(req), "if foo, then always, bar")

    def test_requirement_within(self) -> None:
        p = prop.AP("baz")
        req = fret.Requirement(None, fret.Within(5), p)
        self.assertEqual(str(req), "within 5 timesteps, baz")

    def test_requirement_for(self) -> None:
        cond = prop.AP("foo")
        cons = prop.AP("qux")
        req = fret.Requirement(cond, fret.For(3), cons)
        self.assertEqual(str(req), "if foo, then for 3 timesteps, qux")


class TestTimingMutation(unittest.TestCase):
    def test_mutate_timing(self) -> None:
        timing = fret.Immediately()
        seed_result_pairs = [
            (0, "after 7 timesteps"),
            (1, "eventually"),
            (2, "after 1 timesteps"),
            (5, "within 5 timesteps"),
            (6, "after 10 timesteps"),
            (7, "always"),
            (9, "never"),
            (10, "within 1 timesteps"),
            (14, "at next timepoint"),
            (17, "within 7 timesteps"),
            (19, "for 1 timesteps"),
        ]
        for seed, expected in seed_result_pairs:
            rand = random.Random(seed)
            mutated_timing = fret.mutate_timing(timing, rand)
            self.assertEqual(fret.str_of_timing(mutated_timing), expected)


if __name__ == "__main__":
    unittest.main()
