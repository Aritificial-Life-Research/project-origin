__author__ = 'gkour'

from universe import Universe
from statistics import Stats
import printing
from config import Config
from creatures.zombie import Zombie
from creatures.human import Human


def run(msg_queue=None):
    stats = Stats()
    races = [Zombie, Human]
    universe = Universe(races, stats)

    while universe.pass_time():
        stats.accumulate_step_stats(universe)
        printing.print_step_stats(stats)
        if msg_queue is not None:
            msg_queue.put(stats)
        stats.initialize_inter_step_stats()

        if universe.get_time() % Config.Batch_SIZE == 0:
            stats.accumulate_epoch_stats(universe)
            printing.print_epoch_stats(stats)


if __name__ == '__main__':
    run()