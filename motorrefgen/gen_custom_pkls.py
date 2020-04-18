import os
import argparse

import pickle as pkl

from motorrefgen.experiment import Experiment
from motorrefgen.config import ExperimentConfig

from motorsim.simconfig import SimConfig
from motorsim.simulators.conn_python import Py2Mat


def csv2lst(csv_str):
    """Parse comma seperated string to list.

    Parameters
    ----------
    csv_str : str
        Comma seperated real values.

    Returns
    -------
    list
        List of floats.

    """
    return list(map(float, csv_str.split(',')))


def get_arg_parse():
    """Prase command line arguments.

    Returns
    -------
    Namespace
        ArgumentParser parsed.

    """
    parser = argparse.ArgumentParser(description='Generate custom benchmark.')
    parser.add_argument('--save_dir', required=True, type=str)
    parser.add_argument('--reference_speed', type=csv2lst,
                        required=True, help='comma seperated floats')
    parser.add_argument('--speed_time', type=csv2lst,
                        required=True, help='comma seperated floats')
    parser.add_argument('--reference_torque', type=csv2lst,
                        required=True, help='comma seperated floats')
    parser.add_argument('--torque_time', type=csv2lst,
                        required=True, help='comma seperated floats')
    parser.add_argument('--benchmark_name', type=str,
                        required=True, help='name for saving the data')
    parser.add_argument('--sim_rate', type=float,
                        required=True, help='Simulation rate')
    args = parser.parse_args()
    return args


def generate(opt):
    """Generate trajectory from the passed argument.

    Parameters
    ----------
    opt : args
        Parsed arguments.

    Returns
    -------
    None

    """
    config = ExperimentConfig(integral=False, simulate=True)
    experiment = Experiment(config)

    reference = {'reference_speed': opt.reference_speed,
                 'speed_time':  opt.speed_time,
                 'reference_torque':  opt.reference_torque,
                 'torque_time':  opt.torque_time}
    experiment.set_manual_reference(reference)

    simconfig = SimConfig()
    simconfig.set_config_from_json({'Data_Ts': opt.sim_rate})
    py2mat = Py2Mat(simconfig)

    experiment.simulate(simulator=py2mat)
    simulation_data = experiment.get_simulation_data()

    fout = open(os.path.join(opt.save_dir, opt.benchmark_name + '.pkl'), 'wb')
    pkl.dump(simulation_data, fout)
    fout.close()


opt = get_arg_parse()
generate(opt)
