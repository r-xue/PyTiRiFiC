export CXX=/opt/local/bin/g++
export clang=/opt/local/bin/clang
export gcc=/opt/local/bin/gcc

sudo port select gcc mp-gcc9

python3 setup.py build
python3 setup.py install --user

 git clone https://github.com/pydata/numexpr.git
 cd numexpr
 git checkout numexpr-3.0
  python setup.py build
  python setup.py install --user
  
   pip install --user .
 
