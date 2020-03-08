import pytest

from motorrefgen.experiment import Experiment
from motorrefgen.config import ExperimentConfig

from motorsim.simconfig import SimConfig
from motorsim.simulators.conn_python import Py2Mat

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

        assert len(experiment.reference_torque) == len(experiment.torque_time)
        assert len(experiment.reference_speed) == len(experiment.speed_time)

    def test__stringify(self):
        config = ExperimentConfig(integral=True, simulate=True)
        experiment = Experiment(config)

        strings = experiment._stringify()

        assert len(strings) == 5
        for string in strings:
            assert isinstance(string, str)

    def test__integral_simulation(self):
        config = ExperimentConfig(integral=True, simulate=True)
        experiment = Experiment(config)

        config = SimConfig()
        py2mat = Py2Mat(config)

        experiment.simulate(simulator=py2mat)

        assert hasattr(experiment, 'voltage_d')
        assert hasattr(experiment, 'voltage_q')
        assert hasattr(experiment, 'current_d')
        assert hasattr(experiment, 'current_q')
        assert hasattr(experiment, 'torque')
        assert hasattr(experiment, 'speed')
        assert hasattr(experiment, 'statorPuls')
        assert hasattr(experiment, 'time')
        assert hasattr(experiment, 'reference_torque_interp')
        assert hasattr(experiment, 'reference_speed_interp')

        assert len(experiment.voltage_d) == len(experiment.voltage_q)
        assert len(experiment.voltage_q) == len(experiment.current_d)
        assert len(experiment.current_d) == len(experiment.current_q)
        assert len(experiment.current_q) == len(experiment.torque)
        assert len(experiment.torque) == len(experiment.speed)
        assert len(experiment.speed) == len(experiment.statorPuls)
        assert len(experiment.statorPuls) == len(experiment.time)
        assert len(experiment.time) == len(experiment.reference_speed_interp)
        assert len(experiment.reference_speed_interp) == len(experiment.reference_torque_interp)

        
