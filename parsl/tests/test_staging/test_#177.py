import pytest

import parsl
from parsl.data_provider.files import File
from parsl.tests.configs.local_threads_globus import config

parsl.clear()
parsl.load(config)


@pytest.mark.local
def test_explicit_staging():
    unsorted_file = File(
        "globus://037f054a-15cf-11e8-b611-0ac6873fc732/unsorted.txt")

    print("File plain ", unsorted_file)
    print("Filepath before stage_in ", unsorted_file.filepath)

    dfu = unsorted_file.stage_in()
    dfu.result()

    print("DFU result: ", dfu.result())
    print(unsorted_file.filepath)


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", action='store_true',
                        help="Count of apps to launch")
    args = parser.parse_args()

    if args.debug:
        parsl.set_stream_logger()

    test_explicit_staging()
