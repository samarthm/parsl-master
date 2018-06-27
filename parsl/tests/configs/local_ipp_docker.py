import pytest
import shutil

from parsl.config import Config
from parsl.executors.ipp import IPyParallelExecutor

if shutil.which('docker') is None:
    pytest.skip('docker not installed', allow_module_level=True)

config = Config(
    executors=[
        IPyParallelExecutor(
            label='local_ipp_docker',
            container_image='parslbase_v0.1'
        )
    ],
    lazy_errors=True
)
