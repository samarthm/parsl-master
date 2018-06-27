''' Testing bash apps
'''
from parsl import *
import pytest
from utils import get_rundir
from user_opts import user_opts
import itertools
import time
times = []

if 'midway' in user_opts:
    info = user_opts['midway']
else:
    pytest.skip('midway user_opts not configured {}'.format(str(user_opts)), allow_module_level=True)

for hello in range(1,1000):
    config = {
        "sites": [
            {
                "site": "midway_ipp",
                "auth": {
                    "channel": "ssh",
                    "hostname": "swift.rcc.uchicago.edu",
                    "username": info['username'],
                    "scriptDir": info['script_dir']
                },
                "execution": {
                    "executor": "ipp",
                    "provider": "slurm",
                    "block": {
                        "nodes": 1,
                        "minBlocks": 1,
                        "maxBlocks": 2,
                        "initBlocks": hello,
                        "taskBlocks": 4,
                        "parallelism": 0.5,
                        "options": info['options']
                    }
                }
            }
        ],
        "globals": {
            "lazyErrors": True,
            "runDir": 'runinfo_{}'.format(get_tag(n))
        }
    }
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

import matplotlib.pyplot as plt
myList = range(999)
myList = [x+1 for x in mylist]
plt.plot(myList, times)
plt.xlabel("initBlocks")
plt.ylabel("Time (seconds)")
plt.title("Number of initBlocks on Time")
plt.show()
