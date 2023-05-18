Test Jupyter Sphinx Extension
=============================

Test
----

Test

.. jupyter-execute::

  from ipywidgets import VBox, jsdlink, IntSlider, Button
  s1, s2 = IntSlider(max=200, value=100), IntSlider(value=40)
  b = Button(icon='legal')
  jsdlink((s1, 'value'), (s2, 'max'))
  VBox([s1, s2, b])


.. jupyter-execute::

  import ipyvolume as ipv
  import numpy as np

  N = 1000
  x, y, z = np.random.normal(0, 1, (3, N))
  fig = ipv.figure()
  scatter = ipv.scatter(x, y, z)
  ipv.show()

  V = np.random.random((128,128,128)) # our 3d array
  ipv.quickvolshow(V)