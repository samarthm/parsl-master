Parsl - Parallel Scripting Library
==================================
|licence| |build-status| |docs|

Parsl is a parallel scripting library that enables easy parallelism and workflow design.
The latest version available on PyPi is v0.5.1.

.. |licence| image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
   :target: https://github.com/Parsl/parsl/blob/master/LICENSE
   :alt: Apache Licence V2.0
.. |build-status| image:: https://travis-ci.org/Parsl/parsl.svg?branch=master
   :target: https://travis-ci.org/Parsl/parsl
   :alt: Build status
.. |docs| image:: https://readthedocs.org/projects/parsl/badge/?version=stable
   :target: http://parsl.readthedocs.io/en/stable/?badge=stable
   :alt: Documentation Status

QuickStart
==========

Parsl is now available on PyPI, but first make sure you have Python3.5+ ::

    $ python3 --version

Install Parsl using pip::

    $ pip3 install parsl

To run the Parsl tutorial notebooks you will need to install Jupyter::

    $ pip3 install jupyter

Detailed information about setting up Jupyter with Python3.5 is available `here <https://jupyter.readthedocs.io/en/latest/install.html>`_

Note: By default, Parsl collects anonymous usage statistics for reporting and improvement purposes. To understand what stats are collected and to disable collection please refer to the `usage tracking guide <http://parsl.readthedocs.io/en/stable/userguide/usage_tracking.html>`__

Documentation
=============

The complete parsl documentation is hosted `here <http://parsl.readthedocs.io/en/stable/>`_.

The Parsl tutorial is `here <http://parsl.readthedocs.io/en/stable/tutorial.html>`_ and the same tutorial set hosted on live Jupyter notebooks are available `here <http://try.parsl-project.org:8000/>`_


For Developers
--------------

1. Download Parsl::

    $ git clone https://github.com/Parsl/parsl

2. Install::

    $ cd parsl
    $ python3 setup.py install

3. Use Parsl!

Requirements
============

Parsl requires the following:

* Python 3.5+
* Jupyter (for running tutorial notebooks), with Python3.5+ kernel


For testing:

* nose
* coverage

For building documentation:

* nbsphinx
* sphinx
* sphinx_rtd_theme

Contributing
============

We welcome contributions from the community. Please see our `contributing guide <CONTRIBUTING.rst>`_. 

Citation
========

If you use Parsl, please cite:

Babuji, Yadu, Brizius, Alison, Chard, Kyle, Foster, Ian, Katz, Daniel S., Wilde, Michael, & Wozniak, Justin. (2017, August 30). Introducing Parsl: A Python Parallel Scripting Library. Zenodo. https://doi.org/10.5281/zenodo.853492
