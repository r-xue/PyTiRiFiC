.. highlight:: shell

From Docker Hub
---------------

The ``ism3d`` `repository <https://github.com/r-xue/ism3d>`_ contains a `Dockerfile <https://github.com/r-xue/casa6-docker/blob/master/Dockerfile.dev>`_, that automatically builds the `rxastro/ism3d:dev` images hosted at the `Docker Hub <https://hub.docker.com/r/rxastro/ism3d/tags>`_.
The image contains a base Linux environment (based on `Ubuntu 20.04 <https://releases.ubuntu.com/20.04/>`_) with the ``ism3d`` prototype, `casa6 <https://casa.nrao.edu/casa_obtaining.shtml>`_, and other Python packages (`astropy <https://www.astropy.org/>`_, `Jupyter <https://jupyter.org>`_, etc.) already installed. 

    https://registry.hub.docker.com/r/rxastro/ism3d

.. note::

    The  Docker image ``rxastro/ism3d:dev`` is built upon the base image offered by the `casa6-docker <https://r-xue.github.io/casa6-docker>`_ project:

        https://registry.hub.docker.com/r/rxastro/casa6

    The container launch instruction is the similar with `that <https://www.magclouds.org/casa6-docker/html/docker/usage.html>`_ of ``rxastro/casa6:latest``.


Launch with an interactive shell
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To launch the container with an interactive shell on a host with `Docker Desktop <https://docs.docker.com/docker-for-mac/install/>`_ running, just type:

.. code-block:: console

    $ docker run -it -v ~/Workspace:/root/WorkDir rxastro/ism3d:dev bash

This will download the image ``rxastro/ism3d:dev``, start a container instance, and login as ``root`` (bravely...). It will also try to mount the host directory ``~/Workspace`` (assuming it exists) to ``/root/WorkDir`` of your container.
After this, you can perform code development and data analysis in ``/root/WorkDir`` of your container (now pointing to ``~/Workspace`` on the host), with the access of tools/environment (e.g. **casa6**, **astropy**, etc.) residing in the image.

In case you would like to manually update local-cached images for whatever reasons, you probably want to run this before launching the container again:

.. code-block:: console

    $ docker pull rxastro/ism3d:dev


Run a Jupyter server
^^^^^^^^^^^^^^^^^^^^

A Jupyter server has been built in the Docker image ``rxastro/ism3d:dev`` (see the `Dockerfile <https://github.com/r-xue/casa6-docker/blob/master/Dockerfile>`_ content for its customization).
This creates a useful feature of ``rx.astro/ism3d:dev``: you can connect your host web browser to the Jupyter server running its container instance.
This gives you a portable development environment semi-isolated from your host OS that offers all Jupyter-based features (e.g. `Widgets <https://ipywidgets.readthedocs.io>`_) along with many Python packages: **casatools**, **casatasks**, **astropy**, **numpy**, **matplotlib**, and more.

To log in a ``rxastro/ism3d:dev`` container and start the Jupyter session,

.. code-block:: console

    user@host      $ docker run -v ~/Workspace:/root/WorkDir --env PORT=8890 -it -p 8890:8890 rxastro/ism3d:dev bash
    root@container $ jupyter-lab # start a Jupyter session

Then you can move back to the host, open a web browser, and connect it to the Jupyter server running on the guest OS:

.. code-block:: console

    user@host      $ firefox --new-window ${address:8890-with-token}


Launch with Singularity
^^^^^^^^^^^^^^^^^^^^

Docker images can be imported to `Singularity <https://singularity.lbl.gov/docs-hpc>`_ for HPC-based deployment:

.. code-block:: console

    $ singularity pull docker://rxastro/ism3d:dev
    $ file casa6_latest.sif
    $ singularity inspect casa6_latest.sif
    $ singularity exec -H $HOME/vh:/Users/Rui casa6_latest.sif /bin/bash

.. note::
    
    There are significant design `differences <https://sylabs.io/guides/3.6/user-guide/singularity_and_docker.html>`_ between Docker and Singularity, and a detailed demonstration is beyond the scope of this documentation.
