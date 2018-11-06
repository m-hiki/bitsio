BitsIO: A bit stream I/O class
========================

.. image:: https://travis-ci.org/m-hiki/bitsio.svg?branch=master
  :target: https://travis-ci.org/m-hiki/bitsio

.. image:: https://img.shields.io/github/license/m-hiki/bitsio.svg
  :target: https://github.com/m-hiki/bitsio

.. image:: https://img.shields.io/pypi/m-hiki/bitsio.svg
  :target: https://pypi.python.org/pypi/bitsio

.. image:: https://img.shields.io/pypi/v/bitsio.svg
  :target: https://pypi.python.org/pypi/bitsio


---------------

Installing
------------

Use pip to install BitsIO:

.. code-block:: bash

    pip install bitsio

Usage
------------

Example for reading:

.. code-block:: python

    from io import BytesIO
    from bitsio import BitsIO
    
    bytesio = BytesIO(b'HELLO')
    bitsio = BitsIO(bytesio, bitorder='big')
    for _ in range(1, 5):
        print(chr(bitsio.read(8)))

Example for writing:

.. code-block:: python

    from bitsio import BitsIO

    test_input = 'HELLO'

    with open('hello.txt', 'wb') as f:
        bitsio = BitsIO(f, bitorder='big')
        for s in test_input:
            bitsio.write(ord(s), 8)


Example test running:

.. code-block:: bash

    python -m unittest discover ./tests/



`Release notes <https://github.com/m-hiki/bitsio/releases>`__.


Copyright (c) 2018 Minoru Hiki. All rights reserved.