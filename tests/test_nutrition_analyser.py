import pytest


@pytest.mark.parametrize(
    ("index", "name"),
    [
        (0, "Calories"),
        (5, "Sugar"),
        (2, "Saturated Fat"),
        (7, "Sodium"),
        (8, "Protein"),
        (17, "Fiber"),
    ],
)
def test_retrieved_correct_nutrients(MockNutritionAnalyser, index, name):
    assert (
        MockNutritionAnalyser.recipe_info["nutrition"]["nutrients"][index]["name"]
        == name
    )


def test_get_weigth(MockNutritionAnalyser):
    assert MockNutritionAnalyser.get_weight() == 337
