import pytest

from recipe_healthiness_analyser.recipe_analyser.nutriscore.nutriscore_analyser import (
    NutriScoreAnalyser,
)

nutriscore_analyser: NutriScoreAnalyser = NutriScoreAnalyser()


@pytest.mark.parametrize(
    ("name", "value", "score"),
    [
        ("calories", 500, 1),
        ("sugar", 99.64564, 10),
        ("fiber", 0.99, 1),
        ("protein", 9, 5),
        ("sodium", 44, 0),
        ("vfn_percentage", 0, 0),
        ("saturated_fat", 4, 4),
        ("nutriscore", 14, "D"),
    ],
)
def test_calculate_score(name, value, score):
    assert (
        nutriscore_analyser.calculate_score(nutriscore_table_key=name, value=value)
        == score
    )


@pytest.mark.parametrize(
    ("value", "lower_bound", "upper_bound"), [(0, 0, 0.01), (4, -4, 5), (14, 12, 15)]
)
def test_in_range(value, lower_bound, upper_bound):
    assert nutriscore_analyser.in_range(
        value=value, lower_bound=lower_bound, upper_bound=upper_bound
    )
