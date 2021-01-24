import logging
import time
from concurrent.futures.thread import ThreadPoolExecutor

from helpers import Speed, State
from models.primer.behavior import PrimerBehavior
from models.simulation import Simulation

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)-8s %(name)-15s %(message)s"
)
logger = logging.getLogger("simulation")

n_runs = 5
n_days = 200
config = {
    "start_population": 40,
    "food_count": 40,
    "species": 20,
}
seed = None


def get_seed():
    if seed is None:
        return int(time.time() * 1000)
    return seed


def run_sim(i):
    sim = Simulation(
        1200 * 0.7,
        800 * 0.7,
        PrimerBehavior,
        get_seed(),
        config,
        data_folder="../script_data/limit_energy",
        auto_save=False,
    )
    percentages = [i * 10 for i in range(1, 10)]
    logger.info(f"starting sim {i}")
    while len(sim.data_collector.days) != n_days:
        days = len(sim.data_collector.days)
        percent = days / n_days * 100
        if (
            percentages
            and percent >= percentages[0]
            and PrimerBehavior.is_asleep(sim.world)
        ):
            percentages.pop(0)
            logger.info(f"sim {i} {int(percent)}% complete")
            sim.save()
        if sim.step(Speed.FAST) == State.FINISHED:
            logger.info(f"world sim {i} died")
            break
    sim.save()
    logger.info(f"sim {i} saved")


pool = ThreadPoolExecutor()

if __name__ == "__main__":
    for i in range(n_runs):
        pool.submit(run_sim, i)
