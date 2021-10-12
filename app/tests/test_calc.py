import pytest
from app import calc

def test_example():
  assert calc.add(10,20) == 30
  # assert 1 == 1

# @pytest.mark.slow
# def test_example_another():
#   # assert calc.add(10,20) == 30
#   assert 1 == 1