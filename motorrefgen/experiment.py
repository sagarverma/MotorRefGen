import random

import numpy as np

class Experiment(object):
    def __init__(self, config):
        """
        This class is used to generate reference speed and reference load
        trajectories, can also be used to simulate those trajectories using
        simulink model.
        """
        self.config = config

        self.torque_states = random.randint(*config.static_states)
        self.speed_states = random.randint(*config.static_states)

        if self.config.integral:
            self.torque_time, self.reference_torque = self._gen_integral_torque_trajectory()
            self.speed_time, self.reference_speed = self._gen_integral_speed_trajectory()
        else:
            self.torque_time, self.reference_torque = self._gen_continuous_torque_trajectory()
            self.speed_time, self.reference_speed = self._gen_continuous_speed_trajectory()

        if self.torque_time[-1] > self.speed_time[-1]:
            self.speed_time[-1] = self.torque_time[-1]
        elif self.speed_time[-1] > self.torque_time[-1]:
            self.torque_time[-1] = self.speed_time[-1]

    def _get_ramp(self):
        """
        Get a ramp with random slope.
        """
        if self.config.integral:
            ramp = random.choice(self.config.ramps)
        else:
            ramp = np.random.uniform(self.config.ramp_range[0], self.config.ramp_range[1], 1)[0]

        return ramp

    def _integral_trajectory(self, points):
        """
        Generate a simple trajectory with integral values.
        """
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

        time = time[:-1]

        return time, reference

    def _continuous_trajectory(self, points):
        """
        Generate a random trajectory from a continuous distribution.
        """
        time = [0]
        reference = []

        for point in points:
            ramp = np.random.uniform(self.config.ramp_range[0],
                                      self.config.ramp_range[1], 1)[0]
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
        """
        Generate a simple torque trajectory with integral values.
        """
        torque_points = [0] + random.sample(self.config.torque_steps, k=self.torque_states)
        return self._integral_trajectory(torque_points)

    def _gen_integral_speed_trajectory(self):
        """
        Generate a simple speed trajectory with integral values.
        """
        speed_points = [0] + random.sample(self.config.speed_steps, k=self.speed_states)
        return self._integral_trajectory(speed_points)

    def _gen_continuous_torque_trajectory(self):
        """
        Generate a torque trajectory with continuous values.
        """
        torque_points = [0] + np.random.uniform(self.config.torque_range[0],
                                                self.config.torque_range[1],
                                                self.torque_states)
        return self._continuous_trajectory(torque_points)

    def _gen_continuous_speed_trajectory(self):
        """
        Generate a speed trajectory with continuous values.
        """
        speed_points = [0] + np.random.uniform(self.config.speed_range[0],
                                               self.config.speed_range[1],
                                               self.speed_states)
        return self._continuous_trajectory(speed_points)

    def _get_true_values(self):
        """
        Convert reference torque in % of nominal to Nm and
        reference speed in Hz to rad/s
        """
        return np.asarray(self.reference_torque) * 25 / 100., \
                np.asarray(self.reference_speed) * 2 * np.pi

    def _set_simulation_output(self, data):
        """
        Get all simulated quantities from simulator returned data and
        set them as data member of this class. Also interpolate reference values
        to match simulated data.
        """
        data = np.asarray(data)
        self.voltage_d = data[:, 0]
        self.voltage_q = data[:, 1]
        self.current_d = data[:, 2]
        self.current_q = data[:, 3]
        self.torque = data[:, 4]
        self.speed = data[:, 6]
        self.statorPuls = data[:, 6]
        self.time = data[:, 7]

        reference_torque, reference_speed = self._get_true_values()
        self.reference_torque_interp = np.interp(self.time, self.torque_time, reference_torque)
        self.reference_speed_interp = np.interp(self.time, self.speed_time, reference_speed)

    def _stringify(self):
        """
        Convert simulation input to strings to pass it to simulator.
        """
        reference_torque, reference_speed = self._get_true_values()

        reference_torque = str(list(reference_torque)).replace(',', '')
        reference_speed = str(list(reference_speed)).replace(',', '')
        torque_time = str(list(self.torque_time)).replace(',', '')
        speed_time = str(list(self.speed_time)).replace(',', '')
        sim_time = str(self.speed_time[-1])

        print (reference_torque, reference_speed, torque_time, speed_time, sim_time)
        return reference_speed, reference_torque, \
                speed_time, torque_time, sim_time

    def simulate(self, simulator):
        """
        Simulate using passed model.
        """
        data = simulator.sim(*self._stringify())
        self._set_simulation_output(data)
