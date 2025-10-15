import random
from os import getenv
from unittest import TestCase

if getenv("TESTING") != "1":
    error_msg = "Environment is not ready for testing."
    raise OSError(error_msg)


def total(a: int, b: int) -> int:
    return a + b


class TotalTestCase(TestCase):
    def test_total(self) -> None:
        num_a = random.randint(1, 5)
        num_b = random.randint(1, 5)
        result = total(num_a, num_b)
        expected = num_a + num_b
        self.assertEqual(result, expected)
