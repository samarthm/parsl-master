import argparse
import os

import pytest

import parsl
from parsl.app.app import App
from parsl.tests.conftest import load_dfk
from parsl.tests.configs.midway_ipp_multicore import config

parsl.clear()
parsl.load(config)
parsl.set_stream_logger()


@App('bash')
def mpi_hello(ranks, inputs=[], outputs=[], stdout=None, stderr=None, mock=False):
    pass


@App('bash')
def mpi_test(ranks, inputs=[], outputs=[], stdout=None, stderr=None, mock=False):
    return """module load amber/16+cuda-8.0
    mpirun -n 6 mpi_hello
    mpirun -np 6 pmemd.MPI -O -i config_files/min.in -o min.out -c prot.rst7 -p prot.parm7 -r min.rst7 -ref prot.rst7
    """


whitelist = os.path.join(os.path.dirname(parsl.__file__), 'tests', 'configs', '*MPI.py')


@pytest.mark.whitelist(whitelist)
def test_mpi():
    x = mpi_test(4, stdout="hello.out", stderr="hello.err")
    print("Launched the mpi_hello app")
    x.result()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", default='local',
                        help="Path to configuration file to run")
    args = parser.parse_args()
    load_dfk(args.config)
    test_mpi()
