'''
Libsubmit
=========

Uniform interface to diverse and multi-lingual set of computational resources.

'''
import logging
logger = logging.getLogger(__name__)

from libsubmit.version import VERSION
from libsubmit.providers.slurm.slurm import Slurm
from libsubmit.providers.aws.aws import EC2Provider
from libsubmit.providers.googlecloud.googlecloud import GoogleCloud
from libsubmit.providers.grid_engine.grid_engine import GridEngine
from libsubmit.providers.azure.azure import AzureProvider
from libsubmit.providers.jetstream.jetstream import Jetstream
from libsubmit.providers.condor.condor import Condor
from libsubmit.providers.torque.torque import Torque
from libsubmit.providers.local.local import Local
from libsubmit.providers.cobalt.cobalt import Cobalt
from libsubmit.channels.ssh.ssh import SSHChannel
from libsubmit.channels.ssh_il.ssh_il import SSHInteractiveLoginChannel
from libsubmit.channels.local.local import LocalChannel

__author__ = 'Yadu Nand Babuji'
__version__ = VERSION

__all__ = ['Slurm', 'EC2Provider', 'AzureProvider', 'GoogleCloud', 'Jetstream',
           'Local', 'Cobalt', 'Condor', 'Torque', 'GridEngine',
           'LocalChannel', 'SSHChannel', 'SSHInteractiveLoginChannel']


def set_stream_logger(name='libsubmit', level=logging.DEBUG, format_string=None):
    '''
    Add a stream log handler

    Args:
         - name (string) : Set the logger name.
         - level (logging.LEVEL) : Set to logging.DEBUG by default.
         - format_string (sting) : Set to None by default.

    Returns:
         - None
    '''

    if format_string is None:
        format_string = "%(asctime)s %(name)s [%(levelname)s]  %(message)s"

    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = logging.StreamHandler()
    handler.setLevel(level)
    formatter = logging.Formatter(format_string)
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def set_file_logger(filename, name='libsubmit', level=logging.DEBUG, format_string=None):
    ''' Add a stream log handler

    Args:
        - filename (string): Name of the file to write logs to
        - name (string): Logger name
        - level (logging.LEVEL): Set the logging level.
        - format_string (string): Set the format string

    Returns:
       -  None
    '''

    if format_string is None:
        format_string = "%(asctime)s %(name)s [%(levelname)s] %(message)s"

    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = logging.FileHandler(filename)
    handler.setLevel(level)
    formatter = logging.Formatter(format_string)
    handler.setFormatter(formatter)
    logger.addHandler(handler)


class NullHandler(logging.Handler):
    ''' Setup default logging to /dev/null since this is library.

    '''

    def emit(self, record):
        pass


logging.getLogger('libsubmit').addHandler(NullHandler())
