
https://mtazzari.github.io/galario/install.html#

install fftw-3 gcc8 py27-cpython py27-SPHINX
sudo port select cython py27-cython
sudo port select --set sphinx py27-sphinx


rm -rf build && mkdir build && cd build
cmake -DCMAKE_INSTALL_PREFIX=/opt/galario \
      -DPython_ADDITIONAL_VERSIONS=3.7 \
      -DCMAKE_C_COMPILER=gcc \
      -DCMAKE_CXX_COMPILER=g++ ..

# bbedit  CMakeCache.txt
# change -GALARIO_PYTHON_PKG_DIR=/Users/Rui/Library/Python/2.7/lib/python/site-packages (not need)

^
add to the start star files

make -j8 && make install
