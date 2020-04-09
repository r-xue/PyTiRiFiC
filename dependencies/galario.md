
https://mtazzari.github.io/galario/install.html#

install fftw-3 gcc8 py38-cython py38-SPHINX

sudo port install py38-sphinx fftw-3 fftw-3-single fftw-3-long py38-cython
sudo port select --set sphinx py38-sphinx
sudo port select --set cython cython38

# using HPC gcc: /usr/local/bin/gcc 
#    sudo port select gcc none
#    cmake may get confused by bin/gmake.
#    Removing bin/gamake may be a temp solution
#    also pip uninstall gmake doesn;t really remove bin/gmake 
rm -rf build && mkdir build && cd build
cmake -DCMAKE_INSTALL_PREFIX=/opt/galario \
      -DPython_ADDITIONAL_VERSIONS=3.8 \
      -Wno-dev \
      -DCMAKE_C_COMPILER=gcc \
      -DCMAKE_CXX_FLAGS='-march=native -ffast-math' \
      -DCMAKE_CXX_COMPILER=g++ ..

make -j12 && make install # hexa-core

pip install --user sphinx_py3doc_enhanced_theme sphinxcontrib-fulltoc

## some options of loading the Python binding of galario:

option 1 (after the "cmake" step)
    bbedit  CMakeCache.txt
    change -GALARIO_PYTHON_PKG_DIR=/Users/Rui/Library/Python/3.7/lib/python/site-packages (not need)

option 2 (may not work in a non-interative model call)
    add this to your Python startup file specified by PYTHONSTARTUP
        sys.path.insert(1,'/opt/galario/lib/python3.7/site-packages/')

option 3 (preferred)
    add this to .bashrc:
        export PYTHONPATH=$PYTHONPATH:/opt/galario/lib/python3.8/site-packages
        #https://stackoverflow.com/questions/3146274/is-it-ok-to-use-dyld-library-path-on-mac-os-x-and-whats-the-dynamic-library-s
        export DYLD_FALLBACK_LIBRARY_PATH=$DYLD_FALLBACK_LIBRARY_PATH:/opt/galario/lib/
        
        
        echo $DYLD_LIBRARY_PATH
        echo $DYLD_FALLBACK_LIBRARY_PATH
        echo $LD_LIBRARY_PATH