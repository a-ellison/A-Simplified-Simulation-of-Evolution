import logging
import time

from helpers import Speed, State
from models.microbe.behavior import MicrobeBehavior, FoodPattern
from models.simulation import Simulation

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)-8s %(name)-15s %(message)s"
)
logger = logging.getLogger("simulation")

n_runs = 1
n_steps = 10 ** 4
# n_steps = 100
seed = None
config = {
    "start_population": 10,
    "start_food": 5000,
    "food_per_step": 10,
    "food_pattern": FoodPattern.SQUARE.name,
}


def get_seed():
    if seed is None:
        return int(time.time() * 1000)
    return seed


def run_sim(i):
    sim = Simulation(
        1200 * 0.7,
        800 * 0.7,
        MicrobeBehavior,
        get_seed(),
        config,
        data_folder="../script-runs/",
        auto_save=False,
    )
    percentages = [k * 10 for k in range(1, 10)]
    logger.info(f"starting sim {i}")
    while sim.world.time != n_steps:
        percent = sim.world.time / n_steps * 100
        if percentages and percent >= percentages[0]:
            percentages.pop(0)
            logger.info(f"microbe sim {i} {int(percent)}% complete")
        if sim.step(Speed.FAST) == State.FINISHED:
            logger.info(f"world microbe sim {i} died")
            break
    sim.save()
    logger.info(f"saving microbe sim {i}")


if __name__ == "__main__":
    for i in range(n_runs):
        run_sim(i)
