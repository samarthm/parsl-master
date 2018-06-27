"""The following config uses two IPP executors designed for python apps which may
not show any performance improvements on local threads. This also allows you to
send work to two separate remote executors, or to two separate partitions.
"""
from parsl.config import Config
from libsubmit.providers.local.local import Local
from parsl.executors.ipp import IPyParallelExecutor
from parsl.tests.utils import get_rundir

config = Config(
    executors=[
        IPyParallelExecutor(
            label='local_ipp_1',
            provider=Local(
                nodes_per_block=1,
                tasks_per_node=1,
                walltime="00:15:00",
                init_blocks=4,
            )
        ),
        IPyParallelExecutor(
            label='local_ipp_2',
            provider=Local(
                nodes_per_block=1,
                tasks_per_node=1,
                walltime="00:15:00",
                init_blocks=2,
            )
        )

    ],
    run_dir=get_rundir(),
)
