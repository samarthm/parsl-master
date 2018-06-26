import logging

from parsl.app.futures import DataFuture
from parsl.app.app import AppBase
from parsl.dataflow.dflow import DataFlowKernelLoader

logger = logging.getLogger(__name__)


def remote_side_bash_executor(func, *args, **kwargs):
    """Execute the bash app type function and return the command line string.

    This string is reformatted with the *args, and **kwargs
    from call time.
    """
    import os
    import time
    import subprocess
    import logging
    import parsl.app.errors as pe

    logging.basicConfig(filename='/tmp/bashexec.{0}.log'.format(time.time()), level=logging.DEBUG)

    # start_t = time.time()

    func_name = func.__name__

    # Try to run the func to compose the commandline
    try:
        # Execute the func to get the commandline
        partial_cmdline = func(*args, **kwargs)
        # Reformat the commandline with current args and kwargs
        executable = partial_cmdline.format(*args, **kwargs)

    except AttributeError as e:
        if partial_cmdline:
            raise pe.AppBadFormatting("[{}] App formatting failed during cmd_line resolution: {}".format(func_name, e), None)
        else:
            raise pe.BashAppNoReturn("[{}] Bash App returned NoneType, must return str object".format(func_name), None)

    except IndexError as e:
        raise pe.AppBadFormatting("[{}] App formatting failed during cmd_line resolution: {}".format(func_name, e), None)
    except Exception as e:
        logging.error("[{}] Caught exception during cmd_line resolution: {}".format(func_name, e))
        raise e

    logging.debug("Executable: %s", executable)

    # Updating stdout, stderr if values passed at call time.
    stdout = kwargs.get('stdout')
    stderr = kwargs.get('stderr')
    timeout = kwargs.get('walltime')
    logging.debug("Stdout: %s", stdout)
    logging.debug("Stderr: %s", stderr)

    try:
        std_out = open(stdout, 'w') if stdout else None
    except Exception as e:
        raise pe.BadStdStreamFile(stdout, e)

    try:
        std_err = open(stderr, 'w') if stderr else None
    except Exception as e:
        raise pe.BadStdStreamFile(stderr, e)

    returncode = None
    try:
        proc = subprocess.Popen(executable, stdout=std_out, stderr=std_err, shell=True, executable='/bin/bash')
        proc.wait(timeout=timeout)
        returncode = proc.returncode

    except subprocess.TimeoutExpired as e:
        print("Timeout")
        raise pe.AppTimeout("[{}] App exceeded walltime: {}".format(func_name, timeout), e)

    except Exception as e:
        print("Caught exception: ", e)
        raise pe.AppException("[{}] App caught exception: {}".format(func_name, proc.returncode), e)

    if returncode != 0:
        raise pe.AppFailure("[{}] App failed with exit code: {}".format(func_name, proc.returncode), proc.returncode)

    # TODO : Add support for globs here

    missing = []
    for outputfile in kwargs.get('outputs', []):
        fpath = outputfile
        if type(outputfile) != str:
            fpath = outputfile.filepath

        if not os.path.exists(fpath):
            missing.extend([outputfile])

    if missing:
        raise pe.MissingOutputs("[{}] Missing outputs".format(func_name), missing)

    # exec_duration = time.time() - start_t
    return returncode


class BashApp(AppBase):

    def __init__(self, func, executor=None, walltime=60, cache=False,
                 sites='all', fn_hash=None):
        """Initialize the super.

        This bit is the same for both bash & python apps.
        """
        super().__init__(func, executor=executor, walltime=60, sites=sites, exec_type="bash")
        self.fn_hash = fn_hash
        self.cache = cache

    def __call__(self, *args, **kwargs):
        """Handle the call to a Bash app.

        Args:
             - Arbitrary

        Kwargs:
             - Arbitrary

        Returns:
             If outputs=[...] was a kwarg then:
                   App_fut, [Data_Futures...]
             else:
                   App_fut

        """
        # Update kwargs in the app definition with ones passed in at calltime
        self.kwargs.update(kwargs)

        if self.executor is None:
            self.executor = DataFlowKernelLoader.dfk()

        app_fut = self.executor.submit(remote_side_bash_executor, self.func, *args,
                                       parsl_sites=self.sites,
                                       fn_hash=self.fn_hash,
                                       cache=self.cache,
                                       **self.kwargs)

        out_futs = [DataFuture(app_fut, o, parent=app_fut, tid=app_fut.tid)
                    for o in kwargs.get('outputs', [])]
        app_fut._outputs = out_futs

        return app_fut
