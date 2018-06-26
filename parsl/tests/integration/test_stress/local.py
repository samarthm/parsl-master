from parsl import *
times = []
import time
import argparse
import matplotlib.pyplot as pltp
for hello in range(1,4):
    config = {
        "sites": [
            {
                "site": "local_ipp",
                "auth": {
                    "channel": None
                },
                "execution": {
                    "executor": "ipp",
                    "provider": "local",
                    "block": {
                        "initBlocks": hello,
                    }
                }
            }
        ],
        "globals": {
            "lazyErrors": True,
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
        parser.add_argument("-c", "--count", default="1000",
                            help="width of the pipeline")
        parser.add_argument("-d", "--debug", action='store_true',
                            help="Count of apps to launch")
        args = parser.parse_args()

        if args.debug:
            parsl.set_stream_logger()

        times.append(test_stress(count=int(args.count)))
import matplotlib.pyplot as plt
plt.plot([1,2,3], times)
plt.xlabel("initBlocks")
plt.ylabel("Time (seconds)")
plt.title("Number of initBlocks on Time")
plt.show()