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
    parser = argparse.ArgumentParser(description='Generate training and validation data.')
    parser.add_argument('--save_dir', required=True, type=str)
    parser.add_argument('--set', type=str, required=True, help='train/val')
    parser.add_argument('--samples', type=int, required=True, help='Number of samples.')

    args = parser.parse_args()
    return args

def generate(sim_no, opt):
    config = ExperimentConfig(integral=False, simulate=True)
    experiment = Experiment(config)

    config = SimConfig()
    py2mat = Py2Mat(config)

    experiment.simulate(simulator=py2mat)
    simulation_data = experiment.get_simulation_data()

    fout = open(os.path.join(opt.save_dir, opt.set, str(sim_no).zfill(5) + '.pkl'), 'wb')
    pkl.dump(simulation_data, fout)
    fout.close()

def generate_set(opt):
    if not os.path.exists(os.path.join(opt.save_dir, opt.set)):
        os.makedirs(os.path.join(opt.save_dir, opt.set))

    for i in range(opt.samples):
        generate(i, opt)

opt = get_arg_parse()
generate_set(opt)
