import json

import requests

from recipe_healthiness_analyser.recipe_analyser.constants.constants import (
    CONVERSION_API_URL,
    HEADER,
    HEADER_NUTRITION,
    NUTRITION_API_URL,
)
from recipe_healthiness_analyser.recipe_analyser.recipe import Recipe


class RecipeAnalyser:
    def analyse_nutrients(self, recipe: Recipe) -> Recipe:
        """
        Creates a new Recipe TypedDict with additional nutrients as attribute:
        - calories {float}
        - sugar {float}
        - saturatedfat {float}
        - sodium {float}
        - protein {float}
        - fiber {float}
        - percentage_fvn {float}



        Arguments:
            recipe {Recipe} -- Recipe TypedDict without nutrition attributes

        Returns:
            Recipe -- Recipe TypedDict with added nutrition attributes
        """
        recipe_info: object = self.__fetch_recipe_info_from_api(recipe=recipe)
        parsed_recipe: Recipe = Recipe(
            id=recipe["id"],
            author=recipe["author"],
            followers=recipe["followers"],
            date=recipe["date"],
            media=recipe["media"],
            likes=recipe["likes"],
            comments=recipe["comments"],
            ingredient_list=recipe["ingredient_list"],
            servings=recipe["servings"],
            calories=self.__get_calories(recipe_info),
            sugar=self.__get_sugar(recipe_info),
            saturated_fat=self.__get_saturated_fat(recipe_info),
            sodium=self.__get_sodium(recipe_info),
            protein=self.__get_protein(recipe_info),
            fiber=self.__get_fiber(recipe_info),
            percentage_fvn=self.__get_vfn(recipe_info),
        )
        return parsed_recipe

    def __fetch_recipe_info_from_api(self, recipe: Recipe) -> object:
        querystring: dict[str, str] = {
            "language": "en",
            "includeNutrition": "true",
            "includeTaste": "false",
        }

        payload: dict[str, str] = {
            "title": str(recipe["id"]),
            "servings": str(recipe["servings"]),
            "ingredients": recipe["ingredient_list"],  # type: ignore
        }

        response: requests.Response = requests.request(
            "Post",
            NUTRITION_API_URL,
            json=payload,
            headers=HEADER_NUTRITION,
            params=querystring,
        )
        json_data: object = json.loads(response.text)
        recipe_info: object = json_data
        return recipe_info

    def __get_weight(self, recipe_info: object) -> float:
        return recipe_info["nutrition"]["weightPerServing"]["amount"]  # type: ignore

    def __get_calories(self, recipe_info: object) -> float:
        total_calories: float = self.__convert_to_kj(
            calories=recipe_info["nutrition"]["nutrients"][0]["amount"]  # type: ignore
        )  # type: ignore
        calories_per_100g: float = total_calories / self.__get_weight(recipe_info) * 100
        return calories_per_100g

    def __get_sugar(self, recipe_info: object) -> float:
        total_sugar: float = recipe_info["nutrition"]["nutrients"][5]["amount"]  # type: ignore
        sugar_per_100g: float = total_sugar / self.__get_weight(recipe_info) * 100
        return sugar_per_100g

    def __get_saturated_fat(self, recipe_info: object) -> float:
        total_saturated_fat: float = recipe_info["nutrition"]["nutrients"][2]["amount"]  # type: ignore
        saturated_fat_per_100g: float = (
            total_saturated_fat / self.__get_weight(recipe_info) * 100
        )
        return saturated_fat_per_100g

    def __get_sodium(self, recipe_info: object) -> float:
        total_sodium: float = recipe_info["nutrition"]["nutrients"][7]["amount"]  # type: ignore
        sodium_per_100g: float = total_sodium / self.__get_weight(recipe_info) * 100
        return sodium_per_100g

    def __get_protein(self, recipe_info: object) -> float:
        total_protein: float = recipe_info["nutrition"]["nutrients"][8]["amount"]  # type: ignore
        protein_per_100g: float = total_protein / self.__get_weight(recipe_info) * 100
        return protein_per_100g

    def __get_fiber(self, recipe_info: object) -> float:
        total_fiber: float = recipe_info["nutrition"]["nutrients"][12]["amount"]  # type: ignore
        fiber_per_100g: float = total_fiber / self.__get_weight(recipe_info) * 100
        return fiber_per_100g

    def __get_vfn(self, recipe_info: object) -> float:
        vfn_amount: float = 0

        for ingredient in recipe_info["extendedIngredients"]:  # type: ignore
            if self.__is_vfn(ingredient["id"]):
                if ingredient["unit"] != "gr" or ingredient["unit"] != "g":
                    vfn_amount += self.__convert_to_grams(
                        ingredient["name"], ingredient["unit"], ingredient["amount"]
                    )
                else:
                    vfn_amount += ingredient["amount"]
        return vfn_amount

    def __is_vfn(self, ingredient_id: int) -> bool:
        URL = f"https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/food/ingredients/{ingredient_id}/information"
        response: requests.Response = requests.request("GET", URL, headers=HEADER)
        ingredient_info: object = json.loads(response.text)

        vfn: list[str] = ["fruit", "vegetable", "nut"]
        if any(category in vfn for category in ingredient_info["categoryPath"]):  # type: ignore
            return True
        return False

    @staticmethod
    def __convert_to_grams(ingredient: str, unit: str, amount: int) -> float:
        querystring: dict[str, str] = {
            "ingredientName": ingredient,
            "targetUnit": "grams",
            "sourceUnit": unit,
            "sourceAmount": str(amount),
        }
        response: requests.Response = requests.request(
            "GET", CONVERSION_API_URL, headers=HEADER, params=querystring
        )
        ingredient_info: object = json.loads(response.text)
        return ingredient_info["targetAmount"]  # type: ignore

    @staticmethod
    def __convert_to_kj(calories: float) -> float:
        return calories * 4.184
