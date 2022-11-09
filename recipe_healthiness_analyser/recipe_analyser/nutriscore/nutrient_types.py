from enum import Enum


class NutrientTypes(Enum):
    CALORIES = "calories"
    SUGAR = "sugar"
    SATURATED_FAT = "saturated_fat"
    SODIUM = "sodium"
    FVN = "fvn_percentage"
    FIBERS = "fibers"
    PROTEINS = "proteins"


bad_nutrients = [
    NutrientTypes.CALORIES,
    NutrientTypes.SUGAR,
    NutrientTypes.SATURATED_FAT,
    NutrientTypes.SODIUM,
]

good_nutrients = [NutrientTypes.PROTEINS, NutrientTypes.FIBERS, NutrientTypes.FVN]
