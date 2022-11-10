import pytest
from mock import patch

from recipe_healthiness_analyser.recipe_analyser.nutriscore.nutriscore_analyser import (
    NutriScoreAnalyser,
)
from recipe_healthiness_analyser.recipe_analyser.recipe_analyser import RecipeAnalyser


@pytest.fixture
def MockRecipeAnalyser(MockNutritionAnalyser):
    """
    Mocked Recipe: (recipe-info.json)
    Title: Spaghetti Carbonara
    Servings: 2
    Ingredients: Spaghetti, Pancetta, Olive oil, Egg, Parmesan
    """

    def __init__(self):
        self.nutrition_analyser = MockNutritionAnalyser
        self.nutriscore_analyser = NutriScoreAnalyser()

    with (patch.object(RecipeAnalyser, "__init__", __init__),):
        yield RecipeAnalyser()


def test_calories(MockRecipeAnalyser):
    # Value that is asserted to be equal is calculated by hand
    assert round(MockRecipeAnalyser.get_calories(), 2) == 1615.88


def test_sugar(MockRecipeAnalyser):
    # Value that is asserted to be equal is calculated by hand
    assert round(MockRecipeAnalyser.get_sugar(), 2) == 1.88


def test_saturated_fat(MockRecipeAnalyser):
    # Value that is asserted to be equal is calculated by hand
    assert round(MockRecipeAnalyser.get_saturated_fat(), 2) == 4.14


def test_sodium(MockRecipeAnalyser):
    # Value that is asserted to be equal is calculated by hand
    assert round(MockRecipeAnalyser.get_sodium(), 2) == 229.69


def test_protein(MockRecipeAnalyser):
    # Value that is asserted to be equal is calculated by hand
    assert round(MockRecipeAnalyser.get_protein(), 2) == 14.11


def test_fiber(MockRecipeAnalyser):
    # Value that is asserted to be equal is calculated by hand
    assert round(MockRecipeAnalyser.get_fiber(), 2) == 2.15


def test_vfn(MockRecipeAnalyser):
    assert MockRecipeAnalyser.get_vfn() == 0


def test_healthiness_score(MockRecipeAnalyser):
    # Value that is asserted to be equal is calculated by hand
    assert MockRecipeAnalyser.get_healthiness_score() == 3


def test_nutriscore(MockRecipeAnalyser):
    # Value that is asserted to be equal is calculated by hand
    assert MockRecipeAnalyser.get_nutriscore() == "C"
