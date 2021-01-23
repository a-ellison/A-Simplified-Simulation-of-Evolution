import logging
import time

from helpers import Speed, State
from models.primer.behavior import PrimerBehavior
from models.simulation import Simulation

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)-8s %(name)-15s %(message)s"
)

n_runs = 1
n_days = 500
config = {
    "start_population": 100,
    "food_count": 100,
    "species": 50,
}


if __name__ == "__main__":
    for i in range(n_runs):
        sim = Simulation(
            1200 * 0.7,
            800 * 0.7,
            PrimerBehavior,
            int(time.time() * 1000),
            config,
            data_folder="../script_data",
            auto_save=False,
        )
        while len(sim.data_collector.days) != n_days:
            days = len(sim.data_collector.days)
            if days and days % 100 == 0 and PrimerBehavior.is_asleep(sim.world):
                logging.info(f"{int(days / n_days * 100)}% complete")
            if sim.step(Speed.FAST) == State.FINISHED:
                logging.info("world died")
                break
        sim.data_collector.save()
        logging.info("sim saved")
