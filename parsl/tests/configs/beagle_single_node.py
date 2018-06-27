"""
================== Block
| ++++++++++++++ | Node
| |            | |
| |    Task    | |             . . .
| |            | |
| ++++++++++++++ |
==================
"""
from libsubmit.channels.ssh.ssh import SSHChannel
from libsubmit.providers.torque.torque import Torque
from parsl.config import Config
from parsl.executors.ipp import IPyParallelExecutor
from parsl.tests.user_opts import user_opts
from parsl.tests.utils import get_rundir

config = Config(
    executors=[
        IPyParallelExecutor(
            label='beagle_multinode_mpi',
            provider=Torque(
                'debug',
                channel=SSHChannel(
                    hostname='login4.beagle.ci.uchicago.edu',
                    username=user_opts['beagle']['username'],
                    script_dir="/lustre/beagle2/{}/parsl_scripts".format(user_opts['beagle']['username'])
                ),
                nodes_per_block=1,
                tasks_per_node=1,
                init_blocks=1,
                max_blocks=1,
                launcher='aprun',
                overrides=user_opts['beagle']['overrides'],
            )
        )

    ],
    run_dir=get_rundir()
)
