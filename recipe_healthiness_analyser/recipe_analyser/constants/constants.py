from recipe_healthiness_analyser.recipe_analyser.constants.api_keys import (
    SPOONACULAR_API_KEY,
)

HEADER_NUTRITION: dict[str, str] = {
    "content-type": "application/json",
    "X-RapidAPI-Key": SPOONACULAR_API_KEY,
    "X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
}

HEADER: dict[str, str] = {
    "X-RapidAPI-Key": SPOONACULAR_API_KEY,
    "X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
}

NUTRITION_API_URL: str = (
    "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/analyze"
)
CONVERSION_API_URL: str = (
    "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/convert"
)
