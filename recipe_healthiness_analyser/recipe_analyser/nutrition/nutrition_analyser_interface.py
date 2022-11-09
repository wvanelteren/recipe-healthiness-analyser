import abc


class NutritionAnalyserInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "load_data_source")
            and callable(subclass.load_data_source)
            and hasattr(subclass, "extract_text")
            and callable(subclass.extract_text)
            or NotImplemented
        )

    @abc.abstractmethod
    def get_calories(self) -> float:
        raise NotImplementedError

    @abc.abstractmethod
    def get_sugar(self) -> float:
        raise NotImplementedError

    @abc.abstractmethod
    def get_saturated_fat(self) -> float:
        raise NotImplementedError

    @abc.abstractmethod
    def get_sodium(self) -> float:
        raise NotImplementedError

    @abc.abstractmethod
    def get_protein(self) -> float:
        raise NotImplementedError

    @abc.abstractmethod
    def get_fiber(self) -> float:
        raise NotImplementedError

    @abc.abstractmethod
    def get_vfn(self) -> float:
        raise NotImplementedError
