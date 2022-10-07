import pandas as pd
from recipe_analyser.recipe import Recipe
from recipe_analyser.recipe_analyser import RecipeAnalyser


def main() -> None:
    """
    loads and parses the included recipes.csv file. Consider this an example.
    """
    recipes: list[Recipe] = load_recipes()
    analysed_recipes: list[Recipe] = analyse_recipes(recipes)
    print(analysed_recipes)


def load_recipes() -> list[Recipe]:
    """
    Loads all recipes from the included recipes.csv file into a pandas
    dataframe. Each row is transformed into a Recipe of type TypedDict.

    Returns:
        list[Recipe]: List of all recipes in the recipes.csv file
    """
    df: pd.DataFrame = pd.read_csv("../recipes-nutriscore/recipes_test.csv")

    recipe_list: list[Recipe] = []

    # TODO: df.iterrows() should be avoided in favour of vectorization for
    #       traversing a dataframe due to performance issues. However,
    #       since the included recipes.csv file only has 248 rows, this
    #       doesn't matter. Switch to vectorization for bigger datasets.
    for index, row in df.iterrows():
        try:
            # Assigning key:value pairs while typechecking
            id: int = int(row[0])
            author: str = row[1]
            followers: int = int(row[2])
            date: str = row[3]
            media: str = row[4]
            likes: int = int(row[5])
            comments: int = int(row[6])
            ingredient_list: list[str] = __convert_tolist(row[7])
            servings: int = int(row[8])

            recipe: Recipe = Recipe(
                id=id,
                author=author,
                followers=followers,
                date=date,
                media=media,
                likes=likes,
                comments=comments,
                ingredient_list=ingredient_list,
                servings=servings,
            )
            recipe_list.append(recipe)
        except TypeError:
            print(f"TypeError occured at {row}: {index}")
            raise
    return recipe_list


def analyse_recipes(recipes: list[Recipe]) -> list[Recipe]:
    """
    Analyses nutrients of all recipes in a list

    Arguments:
        recipes {list[Recipe]} -- list of Recipes

    Returns:
        list[Recipe] -- List of analysed Recipes
    """
    analysed_recipes: list[Recipe] = []
    recipe_analyser: RecipeAnalyser = RecipeAnalyser()
    for recipe in recipes:
        analysed_recipe: Recipe = recipe_analyser.analyse_nutrients(recipe=recipe)
        analysed_recipes.append(analysed_recipe)
    return analysed_recipes


def __convert_tolist(string):
    """
    Helpter function that converts a string to a list of strings by splitting the
    string when a comma is encountered
    """
    li: list[str] = list(string.split(","))
    return li


if __name__ == "__main__":
    main()
