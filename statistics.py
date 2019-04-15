__author__ = 'gkour'

import numpy as np
from collections import OrderedDict
from aiq import AIQ
import pandas as pd
import utils
from creature_actions import Actions
from config import ConfigBrain, ConfigBiology


class Stats:

    def __init__(self):
        self.action_dist = np.zeros(Actions.num_actions())  # [Left Right Eat Mate Fight]
        self.death_cause = [0, 0, 0, 0]  # [Fatigue Fight Elderly Fall]
        self.step_stats_df = pd.DataFrame()
        self.epoch_stats_df = pd.DataFrame()

    def accumulate_step_stats(self, universe):
        step_stats_dict = self.collect_last_step_stats(universe)
        temp_df = pd.DataFrame([step_stats_dict], columns=step_stats_dict.keys())
        self.step_stats_df = pd.concat([self.step_stats_df, temp_df], axis=0).reset_index(drop=True)

    def collect_last_step_stats(self, universe):
        return OrderedDict([
            ('Time', universe.get_time()),
            ('Population', universe.num_creatures()),
            ('IDs', universe.get_creatures_counter()),
            ('Age', np.round(utils.emptynanmean([creature.age() for creature in universe.get_all_creatures()]), 2)),
            ('MaxAge',
             np.round(utils.emptynanmean([creature.life_expectancy() for creature in universe.get_all_creatures()]), 2)),
            ('BrainParam',
             np.round(utils.emptynanmean([creature.brain_structure_param() for creature in universe.get_all_creatures()]),
                      2)),
            ('LFreq',
             np.round(utils.emptynanmean([creature.learning_frequency() for creature in universe.get_all_creatures()]),
                      2)),
            ('LRate',
             np.round(utils.emptynanmean([creature.learning_rate() for creature in universe.get_all_creatures()]) *
                      (1 / ConfigBrain.BASE_LEARNING_RATE), 2)),
            ('RDiscount', np.round(utils.emptynanmean([creature.reward_discount() for creature in universe.get_all_creatures()]), 2)),
            ('VRange',
             np.round(utils.emptynanmean([creature.vision_range() for creature in universe.get_all_creatures()]), 2)),
            ('AIQ', AIQ.get_population_aiq(universe)),
            ('RacesDist', universe.races_dist()),
            ('ActionDist', self.action_dist),
            ('DeathCause', self.death_cause),
            ('CreaturesDist', universe.get_creatures_distribution()),
            ('FoodDist', universe.get_food_distribution()),
            ('Fitrah', np.round(np.nanmean([creature.fitrah() for creature in universe.get_all_creatures()], axis=0),
                      2)),
        ])

    def accumulate_epoch_stats(self, universe):
        epoch_stats_dict = self.collect_last_epoch_states(universe)
        temp_df = pd.DataFrame([epoch_stats_dict], columns=epoch_stats_dict.keys())
        self.epoch_stats_df = pd.concat([self.epoch_stats_df, temp_df], axis=0).reset_index(drop=True)

    def collect_last_epoch_states(self, universe):
        return OrderedDict([
            ('Time', universe.get_time()),
            ('PopulationAgeDist', np.histogram([creature.age() for creature in universe.get_all_creatures()],
                                               bins=[0, ConfigBiology.MATURITY_AGE,
                                                     2 * ConfigBiology.MATURITY_AGE,
                                                     ConfigBiology.BASE_LIFE_EXPECTANCY * 2])[0]),
        ])

    def initialize_inter_step_stats(self):
        self.action_dist = np.zeros_like(self.action_dist)
        self.death_cause = np.zeros_like(self.death_cause)
