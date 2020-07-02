import base64
from IPython import display
from IPython.display import clear_output
import os

def show_gif(fname):
    """
    https://github.com/ipython/ipython/issues/10045#issuecomment-642640541
    
    another way:
        os.system('convert -delay 10 '+model_name+'_basis.images/imaging_ch*.pdf '+model_name+'_basis.images/imaging.gif')
        from IPython.display import Image
        Image(filename=model_name+"_basis.images/imaging.gif",embed=True)  
        but this doens't show correctly on github.com  
    """
    clear_output(wait=True) # remove previous plotting cache
    with open(fname, 'rb') as fd:
        b64 = base64.b64encode(fd.read()).decode('ascii')
    return display.HTML(f'<img src="data:image/gif;base64,{b64}" />')


def make_gif(fignames,gifname):
    """
    fname can be wildcard
    os.system('convert -delay 10 '+model_name+'_basis.images/imaging_ch*.pdf '+model_name+'_basis.images/imaging.gif')
    """
    if  isinstance(fignames,list):
        fignames=' '.join(fignames)
    os.system('convert -delay 10 '+fignames+' '+gifname)
