import pytest
from cnegng.ACME import LootTable
import random


@pytest.fixture
def setup_seed():
    """
    Set up a seed for randomness to ensure test repeatability.
    """
    random.seed(42)


def test_percentage_chances_bisect(setup_seed):
    loot = LootTable()

    # Adding entries with known chances
    loot.add_entry(0.5, lambda: "Action A")
    loot.add_entry(0.3, lambda: "Action B")
    loot.add_entry(0.2, lambda: "Action C")

    outcomes = {"Action A": 0, "Action B": 0, "Action C": 0, "None": 0}
    iterations = 100000

    # Perform rolls and track results
    for _ in range(iterations):
        result = loot.roll()
        if result is None:
            outcomes["None"] += 1

        else:
            outcomes[result] += 1

    # Calculate actual percentages

    actual_a = outcomes["Action A"] / iterations

    actual_b = outcomes["Action B"] / iterations

    actual_c = outcomes["Action C"] / iterations

    actual_none = outcomes["None"] / iterations

    # Assert that the actual percentages are close to the expected ones
    assert pytest.approx(actual_a, 0.01) == 0.5
    assert pytest.approx(actual_b, 0.01) == 0.3
    assert pytest.approx(actual_c, 0.01) == 0.2
    assert pytest.approx(actual_none, 0.01) == 0.0  # None should not be triggered
