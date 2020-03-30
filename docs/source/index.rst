.. _package-template:


.. include:: ../../README.rst



..  toctree::
    :maxdepth: 3
    :caption: Quickstart

    install

..  toctree::
    :maxdepth: 3
    :caption: Parameter File
    
    inpfile

    
..  toctree::
    :maxdepth: 1
    :caption: Basic Tutorials
 
    demos/demo_gn20_prep
    
    demos/demo_gn20_imaging
 
    demos/demo_bx610_prep
    demos/demo_bx610_imaging
    demos/demo_bx610_display
 
    demos/demo_bx610_b4c2_uv_ab
    demos/demo_bx610_b4c5_uv_ab
    demos/demo_bx610_b6c3_uv_ab
 
    demos/demo_bx610_model_1dspec
 
    demos/demo_bx610_emcee
 
    demos/demo_hxmm01_prep
    demos/demo_hxmm01_simulate
    demos/demo_hxmm01_dynamics
    
    tests/test_uvsample_performance

..  toctree::
    :maxdepth: 3
    :caption: Examples
    
    tutorials/bx610
    tutorials/gn20
    tutorials/simvla

Tutorials & Examples
~~~~~~~~~

Additional tutorials are in Jupyter Notebooks:

* `basic_demo_amoeba.ipynb <http://colab.research.google.com/github/r-xue/GMaKE/blob/master/examples/notebook/basic_demo_amoeba.ipynb>`_

* `advanced_demo_amoeba.ipynb <http://colab.research.google.com/github/r-xue/GMaKE/blob/master/examples/notebook/basic_demo_amoeba.ipynb>`_

* `basic_demo_emcee.ipynb <http://colab.research.google.com/github/r-xue/GMaKE/blob/master/examples/notebook/basic_demo_emcee.ipynb>`_

* `advanced_demo_emcee.ipynb <http://colab.research.google.com/github/r-xue/GMaKE/blob/master/examples/notebook/basic_demo_emcee.ipynb>`_

* `basic_simulate.ipynb <http://colab.research.google.com/github/r-xue/GMaKE/blob/master/examples/notebook/basic_demo_emcee.ipynb>`_

..  toctree::
    :maxdepth: 3
    :caption: Background
    
    misc

Changelog
---------

.. include:: ../../CHANGELOG.rst
    
..  toctree::
    :maxdepth: 3
    :caption: Modules/Functions
    
    gmake    


..  note::

    GMaKE is an evolving package. 
    Although we make an effort to maintain backwards compatibility for the parameter file syntax,
    the Python API can rapidly change at the current alpha development stage.

..  automodule:: gmake
    :members:
    :undoc-members:
    :show-inheritance:
        
Indices
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
