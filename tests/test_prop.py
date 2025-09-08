import unittest

from src.syntax import prop


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


if __name__ == "__main__":
    unittest.main()
