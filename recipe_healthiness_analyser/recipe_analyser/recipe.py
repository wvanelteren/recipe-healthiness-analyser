from typing import TypedDict


class Recipe(TypedDict, total=False):
    """
    A TypedDict that functions as a model for a recipe.

    Keys:
        id {int}                    --  recipe's id
        author {str}                --  recipe's creator
        followers {int}             --  author's amount of followers on instagram
        date {str}                  --  recipe's post date
        media {str}                 --  type of media recipe is potrayed in
        like {int}                  --  amount of likes recipe post received
        comments {int}              --  amount of comments on recipe post received
        ingredient_list {list[str]} --  list of ingredients including quantity needed
                                        for recipe creation
        servings {int}              --  amount of intended servings
        calories {float}            --  amount of calories in kJ per 100g
        sugar {float}               --  amount of sugar in g per 100g
        saturatedfat {float}        --  amount of saturated fat in g per 100g
        sodium {float}              --  amount of sodium in mg per 100g
        protein {float}             --  amount of protein in g per 100g
        fiber {float}               --  amount of fiber in g per 100g
        percentage_fvn {float}      --  the percentage of the recipe that is either
                                        fruit, vegetable or nuts (needed for NutriScore
                                        calculation)
        nutri_score {str}           --  recipe's NutriScore
        healthiness_score {int}     --  recipe's healthiness score (determines
                                        NutriScore)
    """

    id: int
    author: str
    followers: int
    date: str
    media: str
    likes: int
    comments: int
    ingredient_list: list[str]
    servings: int
    calories: float
    sugar: float
    saturated_fat: float
    sodium: float
    protein: float
    fiber: float
    percentage_fvn: float
    nutri_score: str
    healthiness_score: int
