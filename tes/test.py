"""Simple math operations for testing."""


def add(a: int, b: int) -> int:
    """Return sum of a and b."""
    return a + b


def subtract(a: int, b: int) -> int:
    """Return difference of a and b."""
    return a - b


def multiply(a: int, b: int) -> int:
    """Return product of a and b."""
    return a * b


def divide(a: int, b: int) -> float:
    """Return division of a by b."""
    if not b:
        msg = "Cannot divide by zero"
        raise ValueError(msg)
    return a / b


if __name__ == "__main__":
    print(add(5, 3))
    print(subtract(5, 3))
    print(multiply(5, 3))
    print(divide(5, 3))
