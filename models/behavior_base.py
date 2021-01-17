from abc import ABC, abstractmethod


class BehaviorBase(ABC):
    @classmethod
    @abstractmethod
    def initialize(cls, world):
        pass

    @classmethod
    @abstractmethod
    def get_data_collector(cls, world):
        pass

    @classmethod
    @abstractmethod
    def apply(cls, world, speed):
        pass

    @classmethod
    @abstractmethod
    def is_dead(cls, world):
        pass

    @classmethod
    def get_config(cls):
        return {}
