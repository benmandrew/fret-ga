import random
import unittest

from src import prop


class TestPropToString(unittest.TestCase):
    def test_nested_not_and(self) -> None:
        p = prop.And(prop.Not(prop.AP("foo")), prop.AP("bar"))
        self.assertEqual(prop.str_of_prop(p), "(¬(foo)) ∧ (bar)")

    def test_nested_or_not(self) -> None:
        p = prop.Not(prop.Or(prop.AP("foo"), prop.AP("bar")))
        self.assertEqual(prop.str_of_prop(p), "¬((foo) ∨ (bar))")

    def test_deeply_nested_and_or(self) -> None:
        p = prop.And(
            prop.Or(prop.AP("a"), prop.Not(prop.AP("b"))),
            prop.And(prop.AP("c"), prop.Or(prop.AP("d"), prop.AP("e"))),
        )
        self.assertEqual(
            prop.str_of_prop(p),
            "((a) ∨ (¬(b))) ∧ ((c) ∧ ((d) ∨ (e)))",
        )

    def test_combined_all_types(self) -> None:
        p = prop.Or(
            prop.And(prop.TrueBool(), prop.Not(prop.AP("x"))),
            prop.And(prop.FalseBool(), prop.AP("y")),
        )
        self.assertEqual(
            prop.str_of_prop(p),
            "((True) ∧ (¬(x))) ∨ ((False) ∧ (y))",
        )


def mutate_deterministic(p: prop.Prop, all_ap: list[prop.AP], seed: int) -> str:
    rand = random.Random(seed)
    return prop.str_of_prop(prop.mutate(p, all_ap, rand))


class TestPropMutation(unittest.TestCase):

    def test_unary(self) -> None:
        all_ap = [prop.AP("x"), prop.AP("y"), prop.AP("z")]
        p = prop.Not(prop.AP("x"))

        seed_result_pairs = [
            (0, "¬(¬(x))"),
            (1, "z"),
            (2, "y"),
            (4, "¬(x)"),
            (5, "(y) ∧ (¬(x))"),
            (6, "(x) ∨ (¬(x))"),
            (20, "(z) ∧ (z)"),
        ]
        for seed, expected in seed_result_pairs:
            self.assertEqual(mutate_deterministic(p, all_ap, seed), expected)

    def test_binary(self) -> None:
        all_ap = [prop.AP("x"), prop.AP("y"), prop.AP("z")]
        p = prop.And(prop.AP("x"), prop.AP("y"))

        seed_result_pairs = [
            (0, "¬((¬(x)) ∨ (z))"),
            (1, "z"),
            (2, "y"),
            (3, "z"),
            (4, "¬(y)"),
            (5, "(¬(x)) ∧ (z)"),
            (6, "¬(x)"),
            (7, "(z) ∧ (x)"),
            (8, "¬(y)"),
            (9, "¬((¬(x)) ∧ (¬(y)))"),
        ]
        for seed, expected in seed_result_pairs:
            self.assertEqual(mutate_deterministic(p, all_ap, seed), expected)


if __name__ == "__main__":
    unittest.main()
