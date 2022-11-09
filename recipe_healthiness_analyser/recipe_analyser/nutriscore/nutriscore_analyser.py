import json


class NutriScoreAnalyser:
    score_table: dict[str, any]

    def __init__(self):
        with open(
            "recipe_healthiness_analyser/recipe_analyser/nutriscore/nutriscore_table.json"  # noqa: E501
        ) as json_file:
            self.score_table = json.load(json_file)

    def calculate_healthiness_score(
        calories: float,
        sugar: float,
        saturated_fat: float,
        sodium: float,
        protein: float,
        fiber: float,
        percentage_fvn: float,
    ) -> int:
        raise NotImplementedError

    def calculate_nutriscore(
        calories: float,
        sugar: float,
        saturated_fat: float,
        sodium: float,
        protein: float,
        fiber: float,
        percentage_fvn: float,
    ) -> str:
        raise NotImplementedError

    def calculate_calories_score(self, calories: float) -> int:
        return self.__calculate_nutrient_score(nutrient_key="calories", value=calories)

    def calculate_sugar_score(sugar: float) -> int:
        return 3

    def calculate_saturated_fat_score(saturated_fat: float) -> int:
        raise NotImplementedError

    def calculate_sodium_score(sodium: float) -> int:
        raise NotImplementedError

    def calculate_protein_score(protein: float) -> int:
        raise NotImplementedError

    def calculate_fiber_score(fiber: float) -> int:
        raise NotImplementedError

    def calculate_fvn_score(percentage_fvn: float) -> int:
        raise NotImplementedError

    def __calculate_nutrient_score(self, nutrient_key: str, value: float) -> int:
        score_list: list[list[float, float, int]] = self.score_table.get(nutrient_key)
        for score in score_list:
            if self.in_range(
                value=value,
                lower_bound=score[0],
                upper_bound=score[1],
            ):
                return score[2]
        raise ValueError("Nutrient {nutrient_key} has an extreme, illogical value")

    @staticmethod
    def in_range(value: float, lower_bound: float, upper_bound: float) -> bool:
        return min(lower_bound, upper_bound) < value < max(lower_bound, upper_bound)
