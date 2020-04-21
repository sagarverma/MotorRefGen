
class ExperimentConfig(object):
    """Random trajecotry generator configuration.

    Parameters
    ----------
    integral : bool
        All values of the trajecotries are integers.
    simulate : bool
        Simulate this trajectory using simulink model.

    Attributes
    ----------
    torque_range : list
        Minumum and maximum torque range.
    speed_range : list
        Minimum and maximum speed range.
    static_states : list
        Minimum and maximum number of static states.
    static_duration : list
        Minimum and maximum duration of a static state.
    ramp_range : list
        Minimum and maximum ramp slope.
    step : int
        Generating integral values at step size of the given ranges.
    torque_steps : list
        Torque steps generated from torque range and step when integral=true.
    speed_steps : list
        Speed steps generated from speed range and step when integral=true.
    ramps : list
        List of floats as possible ramps.
    simulate
    integral

    """
    def __init__(self, integral=False, simulate=False):
        self.torque_range = [-120, 120]
        self.speed_range = [-70, 70]
        self.static_states = [5, 15]
        self.static_duration = [1, 5]
        self.ramp_range = [0.00025, 1]
        self.simulate = False
        self.integral = integral

        if self.integral:
            self.step = 1
            self.torque_steps = [x for x in range(self.torque_range[0],
                                 self.torque_range[1], self.step)]
            self.speed_steps = [x for x in range(self.speed_range[0],
                                self.speed_range[1], self.step)]
            self.ramps = [0.00025, 0.0005, 0.001, 0.0025,
                          0.005, 0.1, 0.2, 0.025, 0.05,
                          0.2, 0.1, 0.5, 1]

    def get_config_json(self):
        return {key: value for key, value in self.__dict__.items()
                if not key.startswith('__') and not callable(key)}

    def _validate_config(self, config):
        if 'integral' in config and not config['integral'] and \
                len(config.keys()) == 7:
            return True

        if 'integral' in config and config['integral'] and\
                len(config.keys()) == 11:
            return True

        return False

    def set_config_from_json(self, config):
        # assert self._validate_config(config)

        for k in config.keys():
            self.__dict__[k] = config[k]
