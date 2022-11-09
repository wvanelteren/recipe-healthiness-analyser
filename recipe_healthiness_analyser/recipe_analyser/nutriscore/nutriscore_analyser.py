import json


class NutriScoreAnalyser:
    score_table: dict[str, any]

    def __init__(self):
        with open("nutriscore_table.json") as json_file:
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

    def calculate_calories_score(calories: float) -> int:
        raise NotImplementedError

    def calculate_sugar_score(sugar: float) -> int:
        raise NotImplementedError

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

    @staticmethod
    def in_range(value: float, lower_bound: float, upper_bound: float) -> bool:
        return min(lower_bound, upper_bound) < value < max(lower_bound, upper_bound)
