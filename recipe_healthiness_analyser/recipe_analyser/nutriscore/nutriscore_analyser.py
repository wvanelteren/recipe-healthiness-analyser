import json


class NutriScoreAnalyser:
    score_table: dict[str, any]

    def __init__(self):
        with open(
            "recipe_healthiness_analyser/recipe_analyser/nutriscore/nutriscore_table.json"  # noqa: E501
        ) as json_file:
            self.score_table = json.load(json_file)

    def calculate_healthiness_score(
        self,
        calories: float,
        sugar: float,
        saturated_fat: float,
        sodium: float,
        protein: float,
        fiber: float,
        vfn_percentage: float,
    ) -> int:
        calories_score: int = self.calculate_calories_score(calories=calories)
        sugar_score: int = self.calculate_sugar_score(sugar=sugar)
        saturated_fat_score: int = self.calculate_saturated_fat_score(
            saturated_fat=saturated_fat
        )
        sodium_score: int = self.calculate_sodium_score(sodium=sodium)
        protein_score: int = self.calculate_protein_score(protein=protein)
        fiber_score: int = self.calculate_fiber_score(fiber=fiber)
        vfn_score: int = self.calculate_vfn_score(vfn_percentage=vfn_percentage)

        bad_nutrients_score: int = (
            calories_score + sugar_score + saturated_fat_score + sodium_score
        )  # noqa: E501
        good_nutrients_score: int = protein_score + fiber_score + vfn_score
        if bad_nutrients_score >= 11 and vfn_score < 5:
            return bad_nutrients_score - fiber_score - vfn_score
        else:
            return bad_nutrients_score - good_nutrients_score

    def calculate_nutriscore(
        self,
        calories: float,
        sugar: float,
        saturated_fat: float,
        sodium: float,
        protein: float,
        fiber: float,
        vfn_percentage: float,
    ) -> str:
        healthiness_score: int = self.calculate_healthiness_score(
            calories=calories,
            sugar=sugar,
            saturated_fat=saturated_fat,
            sodium=sodium,
            protein=protein,
            fiber=fiber,
            vfn_percentage=vfn_percentage,
        )
        return self.__calculate_score(
            nutriscore_table_key="nutriscore",
            value=healthiness_score,
        )

    def calculate_calories_score(self, calories: float) -> int:
        return self.__calculate_score(nutriscore_table_key="calories", value=calories)

    def calculate_sugar_score(self, sugar: float) -> int:
        return self.__calculate_score(nutriscore_table_key="sugar", value=sugar)

    def calculate_saturated_fat_score(self, saturated_fat: float) -> int:
        return self.__calculate_score(
            nutriscore_table_key="saturated_fat",
            value=saturated_fat,
        )

    def calculate_sodium_score(self, sodium: float) -> int:
        return self.__calculate_score(nutriscore_table_key="sodium", value=sodium)

    def calculate_protein_score(self, protein: float) -> int:
        return self.__calculate_score(nutriscore_table_key="protein", value=protein)

    def calculate_fiber_score(self, fiber: float) -> int:
        return self.__calculate_score(nutriscore_table_key="fiber", value=fiber)

    def calculate_vfn_score(self, vfn_percentage: float) -> int:
        return self.__calculate_score(
            nutriscore_table_key="vfn_percentage",
            value=vfn_percentage,
        )

    def __calculate_score(self, nutriscore_table_key: str, value: float) -> int | str:
        score_list: list[list[float, float, int]] = self.score_table.get(
            nutriscore_table_key
        )
        for score in score_list:
            if self.in_range(
                value=value,
                lower_bound=score[0],
                upper_bound=score[1],
            ):
                return score[2]
        raise ValueError("Nutrient {nutriscore_table_key} has an improbable value")

    @staticmethod
    def in_range(value: float, lower_bound: float, upper_bound: float) -> bool:
        return min(lower_bound, upper_bound) < value < max(lower_bound, upper_bound)
