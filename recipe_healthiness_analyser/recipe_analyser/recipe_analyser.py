import json

import requests

from recipe_healthiness_analyser.recipe_analyser.constants.constants import (  # HEADER_NUTRITION,; NUTRITION_API_URL,
    CONVERSION_API_URL,
    HEADER,
)
from recipe_healthiness_analyser.recipe_analyser.nutriscore.nutriscore_analyser import (
    NutriScoreAnalyser,
)
from recipe_healthiness_analyser.recipe_analyser.recipe import Recipe
from recipe_healthiness_analyser.recipe_analyser.recipe_analyser_interface import (
    RecipeAnalyserInterface,
)


class RecipeAnalyser(RecipeAnalyserInterface):
    recipe_info: dict[str, any]

    def __init__(self, recipe: Recipe):
        self.recipe_info = self.__fetch_recipe_info_from_api(recipe=recipe)

    def __fetch_recipe_info_from_api(self, recipe: Recipe) -> dict[str, any]:
        """
        Fetches all recipe info from Spoonacular's "Analyze Recipe" endpoint

        Arguments:
            recipe {Recipe} -- recipe

        Returns:
            dict[str, any] -- recipe's information stored in a dictionary of flattened json
        """
        # querystring: dict[str, str] = {
        #     "language": "en",
        #     "includeNutrition": "true",
        #     "includeTaste": "false",
        # }

        # payload: dict[str, str] = {
        #     "title": str(recipe["id"]),
        #     "servings": str(recipe["servings"]),
        #     "ingredients": str(recipe["ingredient_list"]),
        # }

        # response: requests.Response = requests.request(
        #     "Post",
        #     NUTRITION_API_URL,
        #     json=payload,
        #     headers=HEADER_NUTRITION,
        #     params=querystring,
        # )
        # recipe_info: dict[str, any] = json.loads(response.text)
        with open("tests/recipe-info.json") as json_file:
            recipe_info: dict[str, any] = json.load(json_file)
        return recipe_info

    def get_nutriscore(self) -> int:
        nutri_score_analyser: NutriScoreAnalyser = NutriScoreAnalyser()
        score: int = nutri_score_analyser.calculate_calories_score(self.get_calories())
        return score

    def get_calories(self) -> float:
        """Returns recipe's calorie content per 100 gram"""
        total_calories: float = self.__convert_to_kj(
            calories=self.recipe_info["nutrition"]["nutrients"][0]["amount"]
        )  # type: ignore
        calories_per_100g: float = total_calories / self.get_weight() * 100
        return calories_per_100g

    def get_sugar(self) -> float:
        """Returns recipe's sugar content per 100 gram"""
        total_sugar: float = self.recipe_info["nutrition"]["nutrients"][5]["amount"]
        sugar_per_100g: float = total_sugar / self.get_weight() * 100
        return sugar_per_100g

    def get_saturated_fat(self) -> float:
        """Returns recipe's saturated fat content per 100 gram"""
        total_saturated_fat: float = self.recipe_info["nutrition"]["nutrients"][2][
            "amount"
        ]
        saturated_fat_per_100g: float = total_saturated_fat / self.get_weight() * 100
        return saturated_fat_per_100g

    def get_sodium(self) -> float:
        """Returns recipe's sodium content per 100 gram"""
        total_sodium: float = self.recipe_info["nutrition"]["nutrients"][7]["amount"]
        sodium_per_100g: float = total_sodium / self.get_weight() * 100
        return sodium_per_100g

    def get_protein(self) -> float:
        """Returns recipe's protein content per 100 gram"""
        total_protein: float = self.recipe_info["nutrition"]["nutrients"][8]["amount"]
        protein_per_100g: float = total_protein / self.get_weight() * 100
        return protein_per_100g

    def get_fiber(self) -> float:
        """Returns recipe's fiber content per 100 gram"""
        total_fiber: float = self.recipe_info["nutrition"]["nutrients"][12]["amount"]
        fiber_per_100g: float = total_fiber / self.get_weight() * 100
        return fiber_per_100g

    def get_vfn(self) -> float:
        """Returns the percentage that a recipe consists of either fruit, nuts or vegatables"""
        vfn_amount: float = 0

        for ingredient in self.recipe_info["extendedIngredients"]:
            if self.__is_vfn(ingredient["id"]):
                if ingredient["unit"] != "gr" or ingredient["unit"] != "g":
                    vfn_amount += self.__convert_to_grams(
                        ingredient["name"], ingredient["unit"], ingredient["amount"]
                    )
                else:
                    vfn_amount += ingredient["amount"]
        return vfn_amount

    def __is_vfn(self, ingredient_id: int) -> bool:
        """Checks whether ingredient is either a vegetable. fruit or nut"""
        URL = f"https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/food/ingredients/{ingredient_id}/information"
        response: requests.Response = requests.request("GET", URL, headers=HEADER)
        ingredient_info: dict[str, any] = json.loads(response.text)

        vfn: list[str] = ["fruit", "vegetable", "nut"]
        if any(category in vfn for category in ingredient_info["categoryPath"]):
            return True
        return False

    def get_weight(self) -> int:
        """Returns recipe's total weight"""
        weight: int = self.recipe_info["nutrition"]["weightPerServing"]["amount"]
        if weight == 0:
            raise ValueError("Meal cannot weight 0 grams")
        return weight

    @staticmethod
    def __convert_to_grams(ingredient: str, unit: str, amount: int) -> float:
        """
        Converts an ingredient's amount to grams via spoonacular's "Convert Amounts"
        endpoint. This is needed for ingredients of which the amount needed
        is not specified in grams.
            Example: a pinch of salt -> 0.35 grams salt

        Arguments:
            ingredient {str} -- ingredient name
            unit {str} -- type of unit (e.g. handful, gram, pinch, slice)
            amount {int} -- amount of unit

        Returns:
            float -- ingredient's weight in grams
        """
        querystring: dict[str, str] = {
            "ingredientName": ingredient,
            "targetUnit": "grams",
            "sourceUnit": unit,
            "sourceAmount": str(amount),
        }
        response: requests.Response = requests.request(
            "GET", CONVERSION_API_URL, headers=HEADER, params=querystring
        )
        ingredient_info: dict[str, any] = json.loads(response.text)
        weight: float = ingredient_info["targetAmount"]
        if weight == 0.0:
            raise ValueError("ingredient cannot weight 0")
        return weight

    @staticmethod
    def __convert_to_kj(calories: float) -> float:
        return calories * 4.184
