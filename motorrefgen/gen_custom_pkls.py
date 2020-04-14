import os
import argparse
import random

import numpy as np
import pickle as pkl

from motorrefgen.experiment import Experiment
from motorrefgen.config import ExperimentConfig

from motorsim.simconfig import SimConfig
from motorsim.simulators.conn_python import Py2Mat

def get_arg_parse():
    parser = argparse.ArgumentParser(description='Generate custom benchmark.')
    parser.add_argument('--save_dir', required=True, type=str)
    parser.add_argument('--reference_speed', type=str, required=True, help='comma seperated floats')
    parser.add_argument('--speed_time', type=str, required=True, help='comma seperated floats')
    parser.add_argument('--reference_torque', type=str, required=True, help='comma seperated floats')
    parser.add_argument('--torque_time', type=str, required=True, help='comma seperated floats')
    parser.add_argument('--benchmark_name', type=str, required=True, help='name for saving the data')

    args = parser.parse_args()
    return args

def generate(opt):
    config = ExperimentConfig(integral=False, simulate=True)
    experiment = Experiment(config)

    reference = {'reference_speed': list(map(float, opt.reference_speed.split(','))),
                'speed_time':  list(map(float, opt.speed_time.split(','))),
                'reference_torque':  list(map(float, opt.reference_torque.split(','))),
                'torque_time':  list(map(float, opt.torque_time.split(',')))}
    experiment.set_manual_reference(reference)

    config = SimConfig()
    py2mat = Py2Mat(config)

    experiment.simulate(simulator=py2mat)
    simulation_data = experiment.get_simulation_data()

    fout = open(os.path.join(opt.save_dir, opt.benchmark_name + '.pkl'), 'wb')
    pkl.dump(simulation_data, fout)
    fout.close()

opt = get_arg_parse()
generate(opt)
