numexpr-2.6.9/
python-casacore/
numexpr-numexpr-3.0/
mkl_fft-1.0.14/
galario/

for mkl_fft:

pip install --user .

export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES

pip install --user --upgrade git+https://github.com/IntelPython/mkl_fft.git
pip install --user --upgrade git+https://github.com/IntelPython/mkl_random.git
pip install --user --upgrade git+https://github.com/IntelPython/mkl-service.git
pip install --user --upgrade git+https://github.com/IntelPython/mkl_fft.git

pip install --user https://github.com/r-xue/GMaKE/archive/master.zip  # from GitHub


galpy+icc:


git clone https://github.com/jobovy/galpy.git@v1.5.0
cd galpy
git clone https://github.com/jobovy/Torus.git galpy/actionAngle/actionAngleTorus_c_ext/torus
cd galpy/actionAngle/actionAngleTorus_c_ext/torus
git checkout galpy
cd -
    
sudo port install py38-gsl
https://software.intel.com/en-us/cpp-compiler-developer-guide-and-reference-using-the-openmp-libraries
https://readthedocs.org/projects/galpy/downloads/pdf/latest/
https://docs.galpy.org/en/v1.5.0/installation.html#gsl-cflags

python setup.py build_ext --inplace --compiler=intelem -I/opt/local/include -L/opt/local/lib --no-openmp # (this will turn off gomp but icc will have -qopenmp added automatically)
python setup.py install --user

#work around to move  "gomp" first icc does;t work with gnu omp
#edit setup.py

/Users/Rui/Downloads/galpy/galpy/actionAngle/actionAngleTorus_c_ext/torus/src/utils/Numerics.cc
edit --> std::max(double(big), double(fabs(a[i][j])));

You can run the test suite using `pytest -v tests/` to check the installation (but note that the test suite currently takes about 50 minutes to run)


finufft:

commnet out:
    
    _opts['unix'] += ['-stdlib=libc++', '-mmacosx-version-min=10.7']

use clang.inc

    edit make
    CXXFLAGS = $(CFLAGS) -DNEED_EXTERN_C
    --->
    CXXFLAGS = $(CFLAGS) -DNEED_EXTERN_C -I/opt/local/include -L/opt/local/lib
    
    cp make.inc.macosx_ggc-8 make.inc
    edit make.inc
    edit setup.py


    OMPLIBS = -lomp -> OMPLIBS = -lgomp
    https://github.com/flatironinstitute/finufft/issues/68
    sudo port install numdiff
    
    ### option 1
    $make test
    
    ### option 2
    pip install --user --upgrade .
    pip install --user --upgrade --global-option=build_ext --global-option='-I/opt/local/include' --global-option='-L/opt/local/lib' .
    
    ### option 3
    
    https://pip.pypa.io/en/stable/reference/pip_install/#pip-install-examples
    
    pip install -v --user --upgrade .
    
    
    make test
    make test PREC=SINGLE
    
    edit setup.py
    
    try: pip install -v --user --upgrade .
    
    check makefile 254
    
"""
    makeclean
	pip3 install .
	pip install -v --user --upgrade .
	python python_tests/demo1d1.py
	python python_tests/run_accuracy_tests.py
	python python_tests/run_speed_tests.py
	
	check python_tests folder
"""    
    
/opt/local/bin/g++ -fPIC -O3 -funroll-loops -march=native -fcx-limited-range -I src  -I src -I/usr/local/include -I/opt/local/include -L/opt/local/lib -fopenmp -DNEED_EXTERN_C -fopenmp test/finufft1d_basicpassfail.cpp lib-static/libfinufft.a -lfftw3 -lm -L/usr/local/lib -lgomp -lfftw3_threads -lgomp -o test/finufft1d_basicpassfail
/opt/local/bin/g++ -fPIC -O3 -funroll-loops -march=native -fcx-limited-range -I src  -I src -I/usr/local/include -I/opt/local/include -L/opt/local/lib -fopenmp -DNEED_EXTERN_C -fopenmp test/testutils.cpp src/utils.o -o test/testutils
/opt/local/bin/g++ -fPIC -O3 -funroll-loops -march=native -fcx-limited-range -I src  -I src -I/usr/local/include -I/opt/local/include -L/opt/local/lib -fopenmp -DNEED_EXTERN_C -fopenmp test/finufft1d_test.cpp src/spreadinterp.o src/utils.o src/finufft1d.o src/dirft1d.o src/common.o contrib/legendre_rule_fast.o -lfftw3 -lm -L/usr/local/lib -lgomp -lfftw3_threads -lgomp -o test/finufft1d_test
/opt/local/bin/g++ -fPIC -O3 -funroll-loops -march=native -fcx-limited-range -I src  -I src -I/usr/local/include -I/opt/local/include -L/opt/local/lib -fopenmp -DNEED_EXTERN_C -fopenmp test/finufft2d_test.cpp src/spreadinterp.o src/utils.o src/finufft2d.o src/dirft2d.o src/common.o contrib/legendre_rule_fast.o -lfftw3 -lm -L/usr/local/lib -lgomp -lfftw3_threads -lgomp -o test/finufft2d_test
/opt/local/bin/g++ -fPIC -O3 -funroll-loops -march=native -fcx-limited-range -I src  -I src -I/usr/local/include -I/opt/local/include -L/opt/local/lib -fopenmp -DNEED_EXTERN_C -fopenmp test/finufft3d_test.cpp src/spreadinterp.o src/utils.o src/finufft3d.o src/dirft3d.o src/common.o contrib/legendre_rule_fast.o -lfftw3 -lm -L/usr/local/lib -lgomp -lfftw3_threads -lgomp -o test/finufft3d_test
/opt/local/bin/g++ -fPIC -O3 -funroll-loops -march=native -fcx-limited-range -I src  -I src -I/usr/local/include -I/opt/local/include -L/opt/local/lib -fopenmp -DNEED_EXTERN_C -fopenmp test/dumbinputs.cpp lib-static/libfinufft.a -lfftw3 -lm -L/usr/local/lib -lgomp -lfftw3_threads -lgomp -o test/dumbinputs
/opt/local/bin/g++ -fPIC -O3 -funroll-loops -march=native -fcx-limited-range -I src  -I src -I/usr/local/include -I/opt/local/include -L/opt/local/lib -fopenmp -DNEED_EXTERN_C -fopenmp test/finufft2dmany_test.cpp src/spreadinterp.o src/utils.o src/finufft2d.o src/dirft2d.o src/common.o contrib/legendre_rule_fast.o -lfftw3 -lm -L/usr/local/lib -lgomp -lfftw3_threads -lgomp -o test/finufft2dmany_test
test/finufft1d_basicpassfail