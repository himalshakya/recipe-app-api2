import pytest
from app import calc

def test_add_numbers():
  assert calc.add(10,20) == 30


def test_subtract_numbers():
  assert calc.subtract(20, 10) == 10