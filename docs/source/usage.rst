Usage
=====

.. _installation:

Installation
------------

You can start by creating a virtual environment and install scara 
package in development mode:

.. code-block:: console

    $ python -m venv nelen
    $ source nelen/bin/activate
    (nelen) $ pip install -e .

Interacting with the robot
--------------------------

After installation, you can initialize a python prompt and start sending 
instructions to the whole robot or just a joint:

.. code-block:: console

    (nelen) $ python
    >>> import scara
    >>> import logging
    >>> scara.logger.setLevel(logging.INFO)  # set info level for logger
    >>> nelen = scara.Robot()  # creates an instance of the scara robot
    >>> nelen.setup()  # setup motors
    >>> nelen.go_home()  # do homing routine

You can also talk directly with a joint (hombro, codo or z), as follows:

.. code-block:: console

    (nelen) $ python
    >>> import scara
    >>> import logging
    >>> scara.logger.setLevel(logging.INFO)  # set info level for logger
    >>> joint = scara.Joint(odrv_serial_num, axis) # check config/default.yaml
    >>> joint.j_setup()  # setup motors
    >>> joint.j_go_home()  # do homing routine

