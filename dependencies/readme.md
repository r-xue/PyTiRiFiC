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
pip install --user --upgrade git+https://github.com/IntelPython/mkl_fft.git@v1.0.14


galpy+icc:


git clone https://github.com/jobovy/galpy.git
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
