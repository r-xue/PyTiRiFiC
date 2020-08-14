Welcome to ISM3D's documentation!
======================================

.. include:: ../../README.rst

.. toctree::
    :maxdepth: 3
    :caption: User Guide

    install/install
    usage
    authors
    history
    reference

.. toctree::
    :maxdepth: 3
    :caption: Technical Specification/Notes 

    notes/inpfile
    notes/casa6
    notes/keywords

.. toctree::
    :maxdepth: 3
    :caption: Development
    
    develop/background
    develop/goals
    develop/ack
    develop/seealso
    develop/controbuting
    develop/reference
    develop/dictionary
    develop/callgraph  

.. toctree::
    :maxdepth: 3
    :caption: Tutorials: Direct API Usage

    tutorials/demo_api_uvhelper
    tutorials/demo_api_arts
    tutorials/demo_api_lens
    tutorials/demo_api_maskmoment
    #tutorials/jupyter_test
    #tutorials/widgets_render3d
    
    ..
        tutorials/bx610
        tutorials/gn20
        tutorials/simvla
        demos/demo_bx610_display

.. toctree::
    :maxdepth: 3
    :caption: Benchmarking

    benchmark/demo_invert_ft
    tests/test_uvsample_performance

.. toctree::
    :maxdepth: 3
    :caption: Tutorials: Modeling
 
    demos/demo_bx610_b4c2_uv_ab
    demos/demo_bx610_b4c5_uv_ab
    demos/demo_bx610_b6c3_uv_ab
    demos/demo_bx610_model_1dspec
    demos/demo_bx610_emcee
    demos/demo_hxmm01_simulate
    demos/demo_hxmm01_dynamics
    
.. toctree::
    :maxdepth: 3
    :caption: Tutorials: misc

    tutorials/demo_notebook

.. toctree::
    :maxdepth: 3
    :caption: Tutorials: Data Preparation

    demos/demo_gn20_prep
    demos/demo_bx610_prep    
    demos/demo_hxmm01_prep
    demos/demo_gn20_imaging
    demos/demo_bx610_imaging    

    tutorials/demo_notebook    

.. note::

    GMaKE is an evolving package. 
    Although we make an effort to maintain backwards compatibility for the parameter file syntax,
    the Python API can rapidly change at the current alpha development stage.

.. autosummary::
   :toctree: _autosummary
   :caption: API Reference
   :template: custom-module-template.rst
   :recursive:
   
   ism3d    

Indices and tables
==================
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
