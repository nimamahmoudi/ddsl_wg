|PyPI| |PyPI - Status| |Travis (.com)| |Libraries.io dependency status
for latest release| |GitHub|

DDSL Lambda Workload Generator
==============================

This is a workload generator designed especifically to perform load
testing for several applications. The internal use case of this workload
generator is for load testing AWS Lambda functions, but it can be used
for other purposes. All you have to do is give it a ``worker`` function
and the number of requests per second you want to achieve on average and
it will do the rest for you.

Usage
=====

Check out the example.

Installation
============

Install using pip:

.. code:: bash

   $ pip install ddsl-lambda-wg

Upgrading:

.. code:: bash

   pip install ddsl-lambda-wg --upgrade

.. |PyPI| image:: https://img.shields.io/pypi/v/ddsl-lambda-wg.svg
.. |PyPI - Status| image:: https://img.shields.io/pypi/status/ddsl-lambda-wg.svg
.. |Travis (.com)| image:: https://img.shields.io/travis/com/nimamahmoudi/ddsl_lambda_workload_generator.svg
.. |Libraries.io dependency status for latest release| image:: https://img.shields.io/librariesio/release/pypi/ddsl_lambda_wg.svg
.. |GitHub| image:: https://img.shields.io/github/license/nimamahmoudi/ddsl_lambda_workload_generator.svg