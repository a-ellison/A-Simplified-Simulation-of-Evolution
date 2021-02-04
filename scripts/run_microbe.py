import logging
import time

from helpers import Speed, State
from models.microbe.behavior import MicrobeBehavior, FoodPattern
from models.simulation import Simulation

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)-8s %(name)-15s %(message)s"
)
logger = logging.getLogger("simulation")

N_RUNS = 1
N_STEPS = 10 ** 5
SEED = None
SWITCH_PATTERN = None

config = {
    "start_population": 10,
    "start_food": 5000,
    "food_per_step": 10,
    "food_pattern": FoodPattern.EVEN.name,
}


def get_seed():
    if SEED is None:
        return int(time.time() * 1000)
    return SEED


def run_sim(i):
    sim = Simulation(
        1200 * 0.7,
        800 * 0.7,
        MicrobeBehavior,
        get_seed(),
        config,
        data_folder="../script-data/",
        auto_save=False,
    )
    percentages = [k * 10 for k in range(1, 10)]
    logger.info(f"starting sim {i}")
    while sim.world.time != N_STEPS:
        if SWITCH_PATTERN is not None and sim.world.time == N_STEPS / 2:
            logger.info("Switching to %s" % SWITCH_PATTERN)
            sim.world.config["food_pattern"] = SWITCH_PATTERN
        percent = sim.world.time / N_STEPS * 100
        if percentages and percent >= percentages[0]:
            percentages.pop(0)
            logger.info(f"microbe sim {i} {int(percent)}% complete")
        if sim.step(Speed.FAST) == State.FINISHED:
            logger.info(f"world microbe sim {i} died")
            return False
    sim.save()
    logger.info(f"saving microbe sim {i}")
    return True


if __name__ == "__main__":
    for i in range(N_RUNS):
        success = run_sim(i)
        while not success:
            success = run_sim(i)
