from world import World, WorldState
import DNA
import logging
import animal

# Configure logging
logging.basicConfig(filename='world.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(name)-15s %(message)s', filemode='w')


class WorldTester(World):
    def start_world(self):
        logging.debug('World Started')
        self.create_test_animal((self.world_length / 2, self.world_length / 2), DNA(10, 'red'))
        self.create_test_animal((4.5, 50.5), DNA(9, 'green'))
        self.world_state = WorldState.GO

    def create_test_animal(self, coordinates, DNA):
        new_animal = animal.Animal(*coordinates, DNA)
        self.all_animals.append(new_animal)
        self.used_positions.add(coordinates)

    def run(self):
        logging.debug('Run called')
        if self.world_state == WorldState.GO:
            logging.debug('Running')
            self.test_step()

    def test_step(self):
        for animal in self.all_animals:
            animal.move()
            logging.debug('Animal moved')

