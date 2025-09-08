import unittest

from src.syntax import fret, prop


class TestFretToString(unittest.TestCase):
    def test_requirement_immediately(self) -> None:
        p = prop.And(prop.AP("foo"), prop.Not(prop.AP("bar")))
        req = fret.Requirement(None, fret.Immediately(), p)
        self.assertEqual(str(req), "immediately (foo) ∧ (¬(bar))")

    def test_requirement_eventually(self) -> None:
        p = prop.AP("bar")
        req = fret.Requirement(None, fret.Eventually(), p)
        self.assertEqual(str(req), "eventually bar")

    def test_requirement_with_condition(self) -> None:
        cond = prop.AP("foo")
        cons = prop.AP("bar")
        req = fret.Requirement(cond, fret.Always(), cons)
        self.assertEqual(str(req), "if foo, then always bar")

    def test_requirement_within(self) -> None:
        p = prop.AP("baz")
        req = fret.Requirement(None, fret.Within(5), p)
        self.assertEqual(str(req), "within 5 baz")

    def test_requirement_for(self) -> None:
        cond = prop.AP("foo")
        cons = prop.AP("qux")
        req = fret.Requirement(cond, fret.For(3), cons)
        self.assertEqual(str(req), "if foo, then for 3 qux")


if __name__ == "__main__":
    unittest.main()
