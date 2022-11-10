import json

import pytest
from mock import patch

from recipe_healthiness_analyser.recipe_analyser.nutrition.spoonacular_nutrition_analyser import (
    SpoonacularNutritionAnalyser,
)


@pytest.fixture
def MockNutritionAnalyser():
    """
    Mocks SpoonacularNutritionAnalyser __init__ constructor by instead of fetching recipe info
    from spoonacular API reading recipe-info.json

    Mock Recipe:
    Title: Spaghetti Carbonara
    Servings: 2
    Ingredients: Spaghetti, Pancetta, Olive oil, Egg, Parmesan
    Weigth per serving: 337 g
    """

    def __init__(self):
        with open("tests/recipe-info.json") as json_file:
            self.recipe_info = json.load(json_file)

    with (
        patch.object(SpoonacularNutritionAnalyser, "__init__", __init__),
        patch.object(SpoonacularNutritionAnalyser, "get_vfn", return_value=0),
    ):
        yield SpoonacularNutritionAnalyser()


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
