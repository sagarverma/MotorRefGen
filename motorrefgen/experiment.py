import random

class Experiment(object):
    def __init__(self, config):
        self.config = config

        self.torque_states = random.randint(*config.static_states)
        self.speed_states = random.randint(*config.static_states)

        if self.config.integral:
            self.torque_time, self.reference_torque = self._gen_integral_torque_trajectory()
            self.speed_time, self.reference_speed = self._gen_integral_speed_trajectory()
        else:
            self.torque_time, self.reference_torque = self._gen_continuous_torque_trajectory()
            self.speed_time, self.refernce_speed = self._gen_continuous_speed_trajectory()

        if self.torque_time[-1] > self.speed_time[-1]:
            self.speed_time[-1] = self.torque_time[-1]
        elif speed_time[-1] > self.torque_time[-1]:
            self.torque_time[-1] = self.speed_time[-1]
            
    def _get_ramp(self):
        if self.config.integral:
            ramp = random.choice(self.config.ramps)
        else:
            ramp = np.random.uniform(self.config.ramp_range[0], self.config.ramp_range[1], 1)[0]

        return ramp

    def _integral_trajectory(self, points):
        time = [0]
        reference = []

        for point in points:
            ramp = random.choice(self.config.ramps)
            duration = random.randint(*self.config.static_duration)
            time.append(time[-1] + ramp + duration)
            reference.append(point)
            reference.append(point)
            duration = random.randint(*self.config.static_duration)
            time.append(time[-1] + duration + ramp)

        return time, reference

    def _continuous_trajectory(self, points):
        time = [0]
        reference = []

        for point in points:
            ramp = np.random.uniform(self.config.ramp_range[0],
                                      self.config.ramp.range[1], 1)[0]
            duration = np.random.uniform(self.config.static_duration[0],
                                         self.config.static_duration[1], 1)[0]
            time.append(time[-1] + ramp + duration)
            reference.append(point)
            reference.append(point)
            duration = np.random.uniform(self.config.static_duration[0],
                                         self.config.static_duration[1], 1)[0]
            time.append(time[-1] + duration + ramp)

        time = time[:-1]

        return time, reference

    def _gen_integral_torque_trajectory(self):
        torque_points = [0] + random.sample(self.config.torque_steps, k=self.torque_states)
        return self._integral_trajectory(torque_points)

    def _gen_integral_speed_trajectory(self):
        speed_points = [0] + random.sample(self.config.speed_steps, k=self.speed_states)
        return self._integral_trajectory(speed_points)

    def _gen_continuous_torque_trajectory(self):
        torque_points = [0] + np.random.uniform(self.config.torque_range[0],
                                                self.config.torque_range[1],
                                                self.torque_states)
        return self._continuous_trajectory(torque_points)

    def _gen_continuous_speed_trajectory(self):
        speed_points = [0] + np.random.uniform(self.config.speed_range[0],
                                               self.config.speed_range[1],
                                               self.speed_states)
        return self._continuous_trajectory(speed_points)
