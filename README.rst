Flake8 Extension to lint for quotes.
===========================================

.. image:: https://travis-ci.org/zheller/flake8-quotes.svg?branch=master
   :target: https://travis-ci.org/zheller/flake8-quotes
   :alt: Build Status

Deprecation notice in 0.3.0
---------------------------
To anticipate multiline support, we are renaming ``--quotes`` to ``--inline-quotes``. Please adjust your configurations appropriately.

Usage
-----

If you are using flake8 it's as easy as:

.. code:: shell

    pip install flake8-quotes

Now you don't need to worry about people like @sectioneight constantly
complaining that you are using double-quotes and not single-quotes.

Configuration
-------------

By default, we expect single quotes (') and look for unwanted double quotes ("). To expect double quotes (") and find unwanted single quotes ('), use the CLI option:

.. code:: shell

    flake8 --inline-quotes '"'
    # We also support "double" and "single"
    # flake8 --inline-quotes 'double'

or configuration option in `tox.ini`/`setup.cfg`.

.. code:: ini

    inline-quotes = "
    # We also support "double" and "single"
    # inline-quotes = double
