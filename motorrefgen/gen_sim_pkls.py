import os
import argparse

import pickle as pkl

from motorrefgen.experiment import Experiment
from motorrefgen.config import ExperimentConfig

from motorsim.simconfig import SimConfig
from motorsim.simulators.conn_python import Py2Mat


def get_arg_parse():
    """Prase command line arguments.

    Returns
    -------
    Namespace
        ArgumentParser parsed.

    """
    parser = argparse.ArgumentParser(
                    description="""Generate training and validation data.""")
    parser.add_argument('--save_dir', required=True, type=str)
    parser.add_argument('--set', type=str, required=True, help='train/val')
    parser.add_argument('--sim_rate', type=float, required=True,
                        help='Simulation rate')
    parser.add_argument('--samples', type=int, required=True,
                        help='Number of samples.')

    args = parser.parse_args()
    return args


def generate(sim_no, opt):
    """Generate one sample or random trajectory and simulate.

    Parameters
    ----------
    sim_no : int
        Simulation number in the set.
    opt : args
        Parsed arguments.

    Returns
    -------
    None

    """
    config = ExperimentConfig(integral=False, simulate=True)
    experiment = Experiment(config)

    simconfig = SimConfig()
    simconfig.set_config_from_json({'Data_Ts': opt.sim_rate})
    py2mat = Py2Mat(simconfig)

    experiment.simulate(simulator=py2mat)
    simulation_data = experiment.get_simulation_data()

    fout = open(os.path.join(opt.save_dir,
                opt.set, str(sim_no).zfill(5) + '.pkl'), 'wb')
    pkl.dump(simulation_data, fout)
    fout.close()


def generate_set(opt):
    """Generate set of randomly generated trajectories.

    Parameters
    ----------
    opt : args
        Passed arguments.

    Returns
    -------
    None
    """
    if not os.path.exists(os.path.join(opt.save_dir, opt.set)):
        os.makedirs(os.path.join(opt.save_dir, opt.set))

    for i in range(opt.samples):
        generate(i, opt)


opt = get_arg_parse()
generate_set(opt)
