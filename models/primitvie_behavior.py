from primitive_animal import PrimitiveAnimal


class PrimitiveBehavior(object):
    def step(self, animal: PrimitiveAnimal):
        pass

    @classmethod
    def set_limits(cls, world_width, world_height):
        cls.world_width = world_width
        cls.world_height = world_height
