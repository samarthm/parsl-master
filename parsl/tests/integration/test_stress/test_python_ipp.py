''' Testing bash apps
'''
from parsl import *
import pytest
from utils import *
import itertools
import time
times = []
from ssh import *
from libsubmit.providers.slurm.slurm import *
from config import *
from ipp import *
    

for init_block_var in range(1,1000):
    config = Config(
        executors=[
            IPyParallelExecutor(
                provider=Slurm(
                    'westmere',
                    init_blocks=init_blocks_var,
                    min_blocks=1,
                    max_blocks=init_blocks_var,
                    nodes_per_block=1,
                    tasks_per_node=4,
                    parallelism=0.5,
                    overrides='module load Anaconda3/5.1.0; export PARSL_TESTING=True'
                ),
                label='midway_ipp'
            )
        ]
    )
    dfk = DataFlowKernel(config=config)


    @App('python', dfk)
    def increment(x):
        return x + 1


    def test_stress(count=1000):
        """IPP app launch stress test"""
        start = time.time()
        x = {}
        for i in range(count):
            x[i] = increment(i)
        end = time.time()
        print("Launched {0} tasks in {1} s".format(count, end - start))
        dfk.cleanup()
        return((end-start)/1000)

    if __name__ == '__main__':

        parser = argparse.ArgumentParser()
        parser.add_argument("-c", "--count", default="100",
                            help="width of the pipeline")
        parser.add_argument("-d", "--debug", action='store_true',
                            help="Count of apps to launch")
        args = parser.parse_args()

        if args.debug:
            parsl.set_stream_logger()

        test_stress(count=int(args.count))
        times.append(test_stress(count=int(args.count)))

    if (init_block_var % 50) and (init_block_var is not 0):
        thefile = open('initBlocks' + init_block_var + '.txt', 'w')
        for item in times:
            thefile.write("%s\n" % item)

import matplotlib.pyplot as plt
myList = range(999)
myList = [x+1 for x in mylist]
plt.plot(myList, times)
plt.xlabel("initBlocks")
plt.ylabel("Time (seconds)")
plt.title("Number of initBlocks on Time")
plt.show()
