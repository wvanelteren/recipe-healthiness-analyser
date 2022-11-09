import json


class NutriScoreAnalyser:
    score_table: dict[str, any]

    def __init__(self):
        with open("nutriscore_table.json") as json_file:
            self.score_table = json.load(json_file)

    def calculate():
        raise NotImplementedError

    @staticmethod
    def in_range(value: float, lower_bound: float, upper_bound: float) -> bool:
        return min(lower_bound, upper_bound) < value < max(lower_bound, upper_bound)
