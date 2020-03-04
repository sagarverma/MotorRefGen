
class ExperimentConfig(object):
    def __init__(self):
        self.torque_range = [-120, 120]
        self.speed_range = [-70, 70]
        self.static_states = [5, 15]
        self.static_duration = ]1, 5]
        self.ramp_range = [0.00025, 1]

        self.integral = False
