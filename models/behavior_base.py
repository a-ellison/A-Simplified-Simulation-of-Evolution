from abc import ABC, abstractmethod


class BehaviorBase(ABC):
    @classmethod
    @abstractmethod
    def get_data_collector(cls, world, **kwargs):
        pass

    @classmethod
    def get_config(cls):
        return {}

    @classmethod
    @abstractmethod
    def is_dead(cls, world):
        pass

    @classmethod
    @abstractmethod
    def initialize(cls, world):
        pass

    @classmethod
    @abstractmethod
    def apply(cls, world, speed):
        pass
