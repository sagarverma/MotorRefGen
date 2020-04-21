import pytest

from motorrefgen.config import ExperimentConfig

class Test_ExperimentConfig(object):
    def test__init_nointegral(self):
        config = ExperimentConfig(integral=False)

        assert config.integral == False
        with pytest.raises(AttributeError):
            assert config.step == 1

        assert isinstance(config.torque_range, list)
        assert len(config.torque_range) == 2

        assert isinstance(config.speed_range, list)
        assert len(config.speed_range) == 2

        assert isinstance(config.static_states, list)
        assert len(config.static_states) == 2

        assert isinstance(config.static_duration, list)
        assert len(config.static_duration) == 2

        assert isinstance(config.ramp_range, list)
        assert len(config.ramp_range) == 2

    def test__init_integral(self):
        config = ExperimentConfig(integral=True)

        assert config.integral == True
        assert config.step == 1

        assert isinstance(config.torque_steps, list)
        assert isinstance(config.speed_steps, list)
        assert isinstance(config.ramps, list)

    def test__get_config_json_nointegral(self):
        config = ExperimentConfig(integral=False)
        params = config.get_config_json()
        assert isinstance(params, dict)
        assert len(params.keys()) == 7

    def test__get_config_json_integral(self):
        config = ExperimentConfig(integral=True)
        params = config.get_config_json()
        assert isinstance(params, dict)
        assert len(params.keys()) == 11

    def test__set_config_from_json_nointegral(self):
        config = ExperimentConfig(integral=False)
        params = config.get_config_json()
        params['torque_range'] = [0, 10]
        config.set_config_from_json(params)

        assert config.torque_range == [0, 10]

    # def test__set_config_from_json_integral_incomplete(self):
    #     config = ExperimentConfig(integral=False)
    #     params = config.get_config_json()
    #     params['integral'] = True
    #
    #     with pytest.raises(AssertionError):
    #         config.set_config_from_json(params)

    def test__set_config_from_json_nointegral_complete(self):
        config = ExperimentConfig(integral=False)
        params = config.get_config_json()
        params['integral'] = True
        params['step'] = 2
        params['torque_steps'] = [-5, -2, 0, 2, 5]
        params['speed_steps'] = [-3, -1, 0, 1, 3]
        params['ramps'] = [0.1, 0.15, 0.2]
        config.set_config_from_json(params)

        assert config.integral
        assert config.step == 2
        assert config.torque_steps == [-5, -2, 0, 2, 5]
        assert config.speed_steps == [-3, -1, 0, 1, 3]
        assert config.ramps == [0.1, 0.15, 0.2]
