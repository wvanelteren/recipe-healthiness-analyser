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
    fvn_percentage: 0 (as a true spaghetti carbonara should be :D)
    """

    def __init__(self):
        with open("tests/recipe-info.json") as json_file:
            self.recipe_info = json.load(json_file)

    with (
        patch.object(SpoonacularNutritionAnalyser, "__init__", __init__),
        patch.object(SpoonacularNutritionAnalyser, "get_vfn", return_value=0),
    ):
        yield SpoonacularNutritionAnalyser()
