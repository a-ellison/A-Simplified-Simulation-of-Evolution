from models.beeplant.bee import Bee
from models.beeplant.plant import Plant
from models.behavior_base import BehaviorBase

BEES = 'Bees'
PLANTS = 'Plants'


class BeePlantBehavior(BehaviorBase):
    CELL_SIZE = 5

    @classmethod
    def initialize(cls, world):
        cls.set_store(world)
        Bee.CELL_SIZE = cls.CELL_SIZE
        Plant.CELL_SIZE = cls.CELL_SIZE
        world[BEES] = []
        cls.generate_bees(world.config['start_bees'], world)
        world[PLANTS] = []
        cls.generate_plants(world.config['start_bees'], world)

    @classmethod
    def set_store(cls, world):
        min_cell, max_cell = cls.to_cell_corners(*world.corners)
        bee_matrix = [[[] for i in range(min_cell.x, max_cell.x + 1)] for k in range(min_cell.y, max_cell.y + 1)]
        plant_matrix = [[[] for i in range(min_cell.x, max_cell.x + 1)] for k in range(min_cell.y, max_cell.y + 1)]
        world.store[BEES] = bee_matrix
        world.store[PLANTS] = plant_matrix

    @classmethod
    def generate_bees(cls, n, world):
        for i in range(n):
            b = Bee.random(*cls.to_cell_corners(*world.corners))
            world.store[BEES][b.y][b.x].append(b)
            world[BEES].append(b)

    @classmethod
    def generate_plants(cls, n, world):
        for i in range(n):
            p = Plant.random(*cls.to_cell_corners(*world.corners))
            world.store[PLANTS][p.y][p.x].append(p)
            world[PLANTS].append(p)

    @classmethod
    def to_cell_corners(cls, min_coordinate, max_coordinate):
        return cls.to_cell_position(min_coordinate), cls.to_cell_position(max_coordinate.move_by(-1))

    @classmethod
    def to_cell_position(cls, position):
        return position.translate(1 / cls.CELL_SIZE).to_int()

    @classmethod
    def get_data_collector(cls, world):
        pass

    @classmethod
    def apply(cls, world, speed):
        min_cell, max_cell = cls.to_cell_corners(*world.corners)
        for p in world[PLANTS]:
            p.create_pollen()
        for b in world[BEES].copy():
            world.store[BEES][b.y][b.x].remove(b)
            b.move(min_cell, max_cell)
            if b.is_alive:
                world.store[BEES][b.y][b.x].append(b)
            else:
                world[BEES].remove(b)
                del b
        for b in world[BEES].copy():
            cls.try_land(b, world)
            cls.try_reproduce(b, world)
        for p in world[PLANTS].copy():
            cls.try_reproduce(p, world)

    @classmethod
    def try_land(cls, b, world):
        p = cls.try_get_plant(b, world)
        if p is not None:
            b.land(p)

    @classmethod
    def try_get_plant(cls, b, world):
        cell = world.store[PLANTS][b.y][b.x]
        p_choice = None
        for p in cell:
            if p_choice is None or p.pollen > p_choice.pollen:
                p_choice = p
        return None

    @classmethod
    def move_bee(cls, b, world):
        # plants = cls.find_plants(b, world)
        # b.move(*cls.to_cell_corners(*world.corners))
        pass

    @classmethod
    def find_plants(cls, b, world):
        cells = cls.get_neighbours(b.position, world.store[PLANTS], world)
        plants = []
        for c in cells:
            if len(c):
                plants.extend(c)
        return plants

    @classmethod
    def get_neighbours(cls, cell, grid, world):
        min_cell, max_cell = cls.to_cell_corners(*world.corners)
        cells = []
        for y in range(max(min_cell.y, cell.y - 1), min(max_cell.y), cell.y + 2):
            for x in range(max(min_cell.x, cell.x - 1), min(max_cell.x), cell.x + 2):
                cells.append(grid[y][x])
        return cells

    @classmethod
    def try_reproduce(cls, agent, world):
        min_cell, max_cell = cls.to_cell_corners(*world.corners)
        if type(agent) is Bee:
            key = BEES
        elif type(agent) is Plant:
            key = PLANTS
        if agent.can_reproduce:
            child = agent.mutate(min_cell, max_cell)
            world[key].append(child)
            world.store[key][child.y][child.x].append(child)

    @classmethod
    def is_dead(cls, world):
        return len(world[BEES]) == 0 and len(world[PLANTS]) == 0

    @classmethod
    def get_config(cls):
        return {
            'start_bees': {
                'default': 50,
                'label': 'Start Bees'
            },
            'start_plants': {
                'default': 50,
                'label': 'Start Plants'
            }
        }

