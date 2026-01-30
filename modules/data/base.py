from abc import ABC, abstractmethod


class AIModel(ABC):
    @abstractmethod
    def run(self, image):
        pass


class IDGenerator:
    _id = 0

    @classmethod
    def get(cls):
        cls._id += 1
        return cls._id
