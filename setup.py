"""
    Setup file for this module
    v 0.5.6.2
"""
from setuptools import setup

setup(
    name='easy-openshift',
    version='0.5.6.2',
    packages=["easy_openshift"],
    url='https://github.com/GoDllkE/python-api-openshift',
    download_url=('https://github.com/GoDllkE/Easy-Openshift/archive/master.zip'),
    description='A python module to interact with openshift API.',
    author='Gustavo Toledo de Oliveira, Tiago Albuquerque',
    author_email='gustavot53@gmail.com, Tiago.gba@hotmail.com',
    keywords=[
        'openshift',
        'origin',
        'easy-openshift',
        'openshift api',
        'python openshift',
        'oc.py'
    ],
    install_requires=[
        'jsonschema>=2.6.0',
        'json-rpc>=1.10.8',
        'requests>=2.18.4',
    ],
    classifiers=[
        # Development status
        'Development Status :: 3 - Alpha',

        # Intention
        'Intended Audience :: Developers',

        # Os requirement
        'Operating System :: OS Independent',

        # License
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        # Languages
        'Natural Language :: Portuguese (Brazilian)',

        # Supported versions
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only'
    ],
    project_urls={
        'Source': 'https://github.com/GoDllkE/python-api-openshift',
        'Documentaion': 'https://github.com/GoDllkE/python-api-openshift/docs',
        'Tracker': 'https://github.com/GoDllkE/python-api-openshift/issues'
    },
    long_description="""
    Easy-Openshift
========================
This module has purpose to create easy and fast ways to communicate with the API/OAPI from Openshift, allowing the developer to create and manage their own data with their own way. Python is a great language and very well used for DevOps Automantions. With it, creating a Openshift module will easy many steps and automantions allowing a better infrastructure automation or management with great performance.
This version requires Python 3 or later; a Python 2 version is not available... yet.

Features
========================
- Handle openshift through your python script.
- Free to manage the data from openshift API on your own way.
- There's functions to manage it too, if you don't like the previous ideia.
- Simplify most of the openshift client functions to simple and unique interactions.
- Simple code, simple functions, simple management. Keep simple!

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

Gustavo Toledo, Tiago Abluquerque. "Easy-Openshift: Improving openshift auto-management through Python 3", 2018

.. _PYPI: https://pypi.python.org/pypi/Easy-Openshift
.. _Github: https://github.com/GoDllkE/python-api-openshift
    """
)
