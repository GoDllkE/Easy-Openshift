Easy-Openshift
========================
This module has purpose to create easy and fast ways to communicate with the API/OAPI from Openshift, allowing the developer to create and manage their own data with their own way. Python is a great language and very well used for DevOps Automantions. With it, creating a Openshift module will easy many steps and automantions allowing a better infrastructure automation or management with great performance.
This version requires Python 3 or later; a Python 2 version is not available... yet.

Features
========================
- Handle openshift through your own python script.
- Free to manage the data from openshift API on your own way.
- There's functions to manage it too, if you don't like the previous ideia of doing it on your own way.
- Simplify most of the openshift client functions to simple and unique interactions with server.
- Simple code, simple functions, simple management. Just simple!

Installation
============
To install easy-openshift from PYPI:

.. code-block:: bash

    $ pip install easy-openshift

To install easy-openshift manually (please download the source code from either
PYPI_ or Github_ first):

.. code-block:: bash

    $ python setup.py install


Usage
========
To use easy-openshift, just import this module with:

.. code-block:: bash

    $ from easy_openshift import openshift, openshift_utils

Then, create a instance of the class with the functionality you desire:

.. code-block:: bash

    $ oc = openshift.Openshift()

 or

.. code-block:: bash

    $ oc = openshift_utils.OpenshiftTools()

After this, you will be able to use and explore all functionalities.

Enjoy!


Citing
======
Please cite the following paper if you use easy-openshift in a published work:

Gustavo Toledo. "Easy-Openshift: Improving openshift auto-management through python", 2018

- PYPI: https://pypi.python.org/pypi/Easy-Openshift
- Github: https://github.com/GoDllkE/python-api-openshift
- Linkedl: https://www.linkedin.com/in/gustavotoliveira/
