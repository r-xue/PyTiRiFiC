# Diretory Structure




# macports/python configuration on olivine.cv.nrao.edu

link `python3` to py36 (in case you use the official casatools .whl from NRAO) and `python` to py38 (default), respectively

```shell
sudo port install python36 py36-pip py36-ipython
sudo port install python38 py38-pip py38-ipython

sudo port select --set python python38
sudo port select --set pip pip38
sudo port select --set ipython py38-ipython

sudo port select --set python3 python36
sudo port select --set pip3 pip36
sudo port select --set ipython3 py36-ipython
```

verify
```shell
olivine:~ rxue$ pip3 --version
pip 21.0.1 from /opt/local/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/pip (python 3.6)
```

**From here, we start to use `pip3`/`ipython3`/`python3`.**
Also maybe do this:
```shell
PATH="~/Library/Python/3.6/bin:${PATH}" # if using bash
```

# install `ism3d`

In a working directory,
```shell
git clone https://github.com/r-xue/ism3d
cd ism3d/
pip3 install --user -e . # editable mode since we are still working on it..
```

Now you have:
```
working/
    ism3d/
```

# dependency

Currently, the dependecy libraries are specified in multiple places (which is not ideal)

## `install_requires` in `setup.cfg`

Currently, only some essential libraries are included here

## requirements_dev.txt (everything except casa6)

## modular [casa6](https://casa.nrao.edu/casadocs/casa-6.1.0/usingcasa/obtaining-and-installing) (`casatools`, optionally `casatasks`)


```shell
# ver 6.2
pip3 install --user --index-url https://casa-pip.nrao.edu/repository/pypi-group/simple casatools
pip3 install --user --index-url https://casa-pip.nrao.edu/repository/pypi-group/simple casatasks
pip3 install --user --index-url https://casa-pip.nrao.edu/repository/pypi-group/simple casaplotms casaviewer casashell
```
or
```
# ver 6.1
pip3 install --user --index-url https://casa-pip.nrao.edu/repository/pypi-casa-release/simple casatools
pip3 install --user --index-url https://casa-pip.nrao.edu/repository/pypi-casa-release/simple casatasks
pip3 install --user --index-url https://casa-pip.nrao.edu/repository/pypi-casa-release/simple casaplotms casaviewer casashell
```
open a casaplotms session:
```
open ~/Library/Python/3.6/lib/python/site-packages/casaviewer/__bin__/casaplotms.app
```

## [finufft](https://github.com/flatironinstitute/finufft) (currently used in ism3d) or [NIFTy](http://ift.pages.mpcdf.de/nifty/volume.html) (used in RASCIL)

`finufft` recently started to release precompiled library (.whl) on PyPI, which make life easier on macOS (well maybe not.., missing libc++.1.dylib)

```shell
pip3 install --user finufft
```
