
class ExperimentConfig(object):
    def __init__(self, integral=False):
        self.torque_range = [-120, 120]
        self.speed_range = [-70, 70]
        self.static_states = [5, 15]
        self.static_duration = [1, 5]
        self.ramp_range = [0.00025, 1]
        self.integral = integral

        if self.integral:
            self.step = 1
            self.torque_steps = [x for x in range(self.torque_range[0], self.torque_range[1], self.step)]
            self.speed_steps =[x for x in range(self.speed_range[0], self.speed_range[1], self.step)]
            self.ramps = [0.00025, 0.0005, 0.001, 0.0025, 0.005, 0.1, 0.2, 0.025, 0.05, 0.2, 0.1, 0.5, 1]

    def get_config_json(self):
        return {key:value for key, value in self.__dict__.items() if not key.startswith('__') and not callable(key)}
