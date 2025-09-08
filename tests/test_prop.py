import random
import unittest

from src.logic import prop


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


class TestPropMutation(unittest.TestCase):
    def test_unary(self) -> None:
        all_ap = [prop.AP("x"), prop.AP("y"), prop.AP("z")]
        p = prop.Not(prop.AP("x"))

        def test_with_seed(seed: int, expected: str) -> None:
            rand = random.Random(seed)
            mutated_p = prop.mutate(p, all_ap, rand)
            self.assertEqual(prop.str_of_prop(mutated_p), expected)

        test_with_seed(0, "¬(¬(x))")
        test_with_seed(1, "z")
        test_with_seed(2, "y")
        test_with_seed(4, "¬(x)")
        test_with_seed(5, "(y) ∧ (¬(x))")
        test_with_seed(6, "(x) ∨ (¬(x))")
        test_with_seed(20, "(z) ∧ (z)")


if __name__ == "__main__":
    unittest.main()
