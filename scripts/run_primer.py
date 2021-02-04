import logging
import time

from helpers import Speed, State
from models.primer.behavior import PrimerBehavior
from models.simulation import Simulation

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)-8s %(name)-15s %(message)s"
)
logger = logging.getLogger("simulation")

N_RUNS = 1
N_DAYS = 1000
SEED = None

config = {
    "start_population": 40,
    "food_count": 40,
    "species": 20,
}


def get_seed():
    if SEED is None:
        return int(time.time() * 1000)
    return SEED


def run_sim(i):
    sim = Simulation(
        1200 * 0.7,
        800 * 0.7,
        PrimerBehavior,
        get_seed(),
        config,
        data_folder="../script-data/",
        auto_save=False,
    )
    percentages = [k * 10 for k in range(1, 10)]
    logger.info(f"starting sim {i}")
    while len(sim.data_collector.days) != N_DAYS:
        days = len(sim.data_collector.days)
        percent = days / N_DAYS * 100
        if (
            percentages
            and percent >= percentages[0]
            and PrimerBehavior.is_asleep(sim.world)
        ):
            percentages.pop(0)
            logger.info(f"sim {i} {int(percent)}% complete")
        if sim.step(Speed.FAST) == State.FINISHED:
            logger.info(f"world sim {i} died")
            break
    sim.save()
    logger.info(f"sim {i} saved")


if __name__ == "__main__":
    for i in range(N_RUNS):
        run_sim(i)
