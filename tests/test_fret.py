import random
import unittest

from src import fret, prop


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


class TestRequirementMutation(unittest.TestCase):
    def test_mutate_requirement(self) -> None:
        all_ap = [prop.AP("x"), prop.AP("y"), prop.AP("z")]
        cond = prop.AP("x")
        cons = prop.And(prop.Not(prop.AP("y")), prop.AP("x"))
        req = fret.Requirement(cond, fret.Always(), cons)

        seed_result_pairs = [
            (0, "if x, then after 7 timesteps, (¬(y)) ∧ (x)"),
            (4, "if z, then always, (¬(y)) ∧ (x)"),
            (5, "if x, then always, ((y) ∧ (z)) ∧ (y)"),
            (6, "if x, then always, ¬(¬(y))"),
            (7, "if x, then at next timepoint, (¬(y)) ∧ (x)"),
            (14, "always, (¬(y)) ∧ (x)"),
            (15, "always, (¬(y)) ∧ (x)"),
            (16, "if x, then never, (¬(y)) ∧ (x)"),
            (17, "if x, then always, ¬((¬(¬(y))) ∧ (¬(x)))"),
            (18, "always, (¬(y)) ∧ (x)"),
            (19, "if x, then always, (x) ∨ (z)"),
            (20, "if x, then always, ¬(x)"),
            (21, "if ¬(x), then always, (¬(y)) ∧ (x)"),
            (22, "always, (¬(y)) ∧ (x)"),
            (27, "if x, then always, ¬(((y) ∧ (¬(y))) ∨ (y))"),
        ]
        for seed, expected in seed_result_pairs:
            rand = random.Random(seed)
            mutated_req = req.mutate(all_ap, rand)
            self.assertEqual(str(mutated_req), expected)


if __name__ == "__main__":
    unittest.main()
