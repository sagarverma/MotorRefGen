import pytest

from motorrefgen.experiment import Experiment
from motorrefgen.config import ExperimentConfig

class Test_Experiment(object):
    def test__init(self):
        config = ExperimentConfig(integral=True, simulate=False)
        experiment = Experiment(config)

        assert isinstance(experiment.config, ExperimentConfig)
        assert isinstance(experiment, Experiment)
        
