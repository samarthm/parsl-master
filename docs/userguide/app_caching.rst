.. _label-appcaching:

App caching
----------

When developing a workflow, developers often run the same workflow
with incremental changes over and over. Often large fragments of
a workflow will not have changed, yet apps will be executed again, wasting
valuable developer time and computation resources. App caching
solves this problem by storing results from apps that have completed
so that they can be re-used. App caching can be enabled by setting the `cache`
argument to the :func:`~parsl.app.app` decorator to `True` (by default it is `False`). App caching
can be globally disabled by setting `app_cache=False` (which by default is `True`)
in the :class:`~parsl.config.Config`.

.. code-block:: python

   @app('bash', dfk, cache=True)
   def hello (msg, stdout=None):
       return 'echo {}'.format(msg)


App caching can be particularly useful when developing interactive workflows such as when
using a Jupyter notebook. In this case, cells containing apps are often re-executed as 
during development. Using app caching will ensure that only modified apps are re-executed.

Caveats
^^^^^^^

It is important to consider several important issues when using app caching:

- Determinism:  App caching is generally useful only when the apps are deterministic.
  If the outputs may be different for identical inputs, app caching will hide
  this non-deterministic behavior. For instance, caching an app that returns
  a random number will result in every invocation returning the same result.

- Timing: If several identical calls to a previously defined app are
  made for the first time, many instances of the app will be launched as no cached
  result is yet available. Once one such app completes and the result is cached
  all subsequent calls will return immediately with the cached result.

- Performance: If app caching is enabled, there is likely to be some performance
  overhead especially if a large number of short duration tasks are launched rapidly.

.. note::
   The performance penalty has not yet been quantified.
