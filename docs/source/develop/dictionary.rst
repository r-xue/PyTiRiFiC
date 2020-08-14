ISM3D Dictionary
~~~~~~~~~~~~~~~~

Here I highlight major ism3d subpackage/modules and some complementary tools offering equivalent functions

.. list-table:: Title
   :widths: 8 10 8
   :header-rows: 1

   * - ism3d Module/Function
     - description
     - equivalent to / inspired by     
   * - ism3d.arts.disk3d
     - generate cloudlet-based disk model
     - kinmspy, galmod, barolo3d
   * - ism3d.arts/.simxy/.modeling
     - source modeling in the image domain up to 3d (position-position-frequency/wavelength, regular or sparse) 
     - galfit (2D), TiRiFiC (3D), Barolo3d (3D)
   * - ism3d.arts/.simuv/.modeling
     - source modeling in the visibility domain up to 3d (uu-vv-frequency/wavelength, sparse) 
     - UVMULTIFIT (3D?)
   * - ims3d.uvhelper.uv_render
     - render source model int a uv data frame
     - galario
   * - ism3d.uvhelper.invert_ft
     - invert uv data into dirty map
     - miriad.invert, casa.tclean