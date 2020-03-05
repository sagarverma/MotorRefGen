import pytest

from motorrefgen.experiment import Experiment
from motorrefgen.config import ExperimentConfig

class Test_Experiment(object):
    def test__init(self):
        config = ExperimentConfig(integral=True, simulate=False)
        experiment = Experiment(config)

        assert isinstance(experiment.config, ExperimentConfig)
        assert isinstance(experiment, Experiment)

    def test__integral(self):
        config = ExperimentConfig(integral=True, simulate=False)
        experiment = Experiment(config)

        assert experiment.torque_states >= config.static_states[0] and\
               experiment.torque_states <= config.static_states[1]
        assert experiment.speed_states >= config.static_states[0] and\
                experiment.torque_states <= config.static_states[1]

        for torque in experiment.reference_torque:
            assert isinstance(torque, int)
            assert torque >= config.torque_range[0] and torque <= config.torque_range[1]

        for speed in experiment.reference_speed:
            assert isinstance(speed, int)
            assert speed >= config.speed_range[0] and speed <= config.speed_range[1]
