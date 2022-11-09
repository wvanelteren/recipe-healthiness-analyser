from recipe_healthiness_analyser.recipe_analyser.nutriscore.nutriscore_analyser import (
    NutriScoreAnalyser,
)
from recipe_healthiness_analyser.recipe_analyser.nutrition.spoonacular_nutrition_analyser import (
    SpoonacularNutritionAnalyser,
)
from recipe_healthiness_analyser.recipe_analyser.recipe import Recipe


class RecipeAnalyser:
    def __init__(self, recipe: Recipe):
        self.nutrition_analyser: SpoonacularNutritionAnalyser = (
            SpoonacularNutritionAnalyser(
                title=str(recipe.get("id")),
                servings=recipe.get("servings"),
                ingredients=recipe.get("ingredient_list"),
            )
        )
        self.nutriscore_analyser: NutriScoreAnalyser = NutriScoreAnalyser()

    def get_healthiness_score(self) -> int:
        return self.nutri_score_analyser.calculate_healthiness_score(
            calories=self.get_calories(),
            sugar=self.get_sugar(),
            saturated_fat=self.get_saturated_fat(),
            sodium=self.get_sodium(),
            protein=self.get_protein(),
            fiber=self.get_fiber(),
            vfn_percentage=self.get_vfn(),
        )

    def get_nutriscore(self) -> str:
        return self.nutri_score_analyser.calculate_nutriscore(
            calories=self.get_calories(),
            sugar=self.get_sugar(),
            saturated_fat=self.get_saturated_fat(),
            sodium=self.get_sodium(),
            protein=self.get_protein(),
            fiber=self.get_fiber(),
            vfn_percentage=self.get_vfn(),
        )

    def get_calories(self) -> float:
        """Returns recipe's calorie content per 100 gram"""
        return self.nutrition_analyser.get_calories()

    def get_sugar(self) -> float:
        """Returns recipe's sugar content per 100 gram"""
        return self.nutrition_analyser.get_sugar()

    def get_saturated_fat(self) -> float:
        """Returns recipe's saturated fat content per 100 gram"""
        return self.nutrition_analyser.get_saturated_fat()

    def get_sodium(self) -> float:
        """Returns recipe's sodium content per 100 gram"""
        return self.nutrition_analyser.get_sodium()

    def get_protein(self) -> float:
        """Returns recipe's protein content per 100 gram"""
        return self.nutrition_analyser.get_protein()

    def get_fiber(self) -> float:
        """Returns recipe's fiber content per 100 gram"""
        return self.nutrition_analyser.get_fiber()

    def get_vfn(self) -> float:
        """Returns the percentage that a recipe consists of either fruit, nuts or vegatables"""
        return self.nutrition_analyser.get_vfn()

    def get_weight(self) -> int:
        """Returns recipe's total weight"""
        return self.nutrition_analyser.get_weight()
