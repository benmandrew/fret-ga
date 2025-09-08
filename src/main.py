from src.logic import fret, prop


def main() -> None:
    condition = prop.And(prop.AP("a"), prop.AP("b"))
    timing = fret.Always()
    consequent = prop.Not(prop.AP("c"))
    requirement = fret.Requirement(condition, timing, consequent)
    print(requirement)  # noqa: T201


if __name__ == "__main__":
    main()
