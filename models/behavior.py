from abc import ABC, abstractmethod


class Behavior(ABC):
    @abstractmethod
    def apply(self, world):
        pass


