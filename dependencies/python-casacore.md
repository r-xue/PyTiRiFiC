### No long relevant as the binary is available for modern Mac now from PyPI

export CFLAGS="-std=c++11 -stdlib=libc++ -I/opt/local/include -I/opt/casacore/include -L/opt/local/lib -L/opt/casacore/lib "
export LDFLAGS="-L/opt/local/lib -L/opt/casacore/lib"
export LD_LIBRARY_PATH="-L/opt/local/lib -L/opt/casacore/lib"
# likely you want to use the Apple cc instead (so don;t use the below line and make sure > port seletc gcc none)
#export CC=/opt/local/bin/gcc 
python3 setup.py install --user build_ext -I/opt/casacore/include:/opt/local/include -L/opt/casacore/lib:/opt/local/lib


#################

# -I/opt/local/include -I/opt/casacore/include -I/opt/local/include
pip3 install --user --upgrade python-casacore


pip3 uninstall python-casacore
rm -rf build
rm -rf dist

otool -l /Users/Rui/Library/Python/3.7/lib/python/site-packages/python_casacore-3.0.0-py3.7-macosx-10.14-x86_64.egg/casacore/tables/_tables.cpython-37m-darwin.so
otool -L /opt/local/lib/libboost_python3-mt.dylib

otool -hV /Users/Rui/Library/Python/3.7/lib/python/site-packages/python_casacore-3.0.0-py3.7-macosx-10.14-x86_64.egg/casacore/tables/_tables.cpython-37m-darwin.so


CFLAGS="-std=c++11 \
        -I/opt/casacore/include/
        -I/opt/local/include/ \
        -L/opt/casacore/lib/ \
        -L/opt/local/lib/" \
        pip3 install --user python-casacore


make sure python-casacore / libboost_python and casacore compiled with the same compiler:

otool -L /opt/local/lib/libboost_python3-mt.dylib
otool -L /opt/local/lib/libboost_python3-mt.dylib
---> /usr/lib/libc++.1.dylib (compatibility version 1.0.0, current version 400.9.4)

https://github.com/lofar-astron/PyBDSF/issues/11
https://github.com/casacore/casacore/issues/596#issuecomment-303708592
