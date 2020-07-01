import os
import glob

import numpy as np
import re

import casatasks as ctasks
import casatools as ctools


def casa_version():
    """
    show the CASA 6 tools/tasks version number
    """
    print('casatools ver:',ctools.version_string())
    print('casatasks ver:',ctasks.version_string())

def plotuv_freqtime_amp(vis='',spw=[''],xaxis='freq'):
    """
        vis='calibrated_target.ms',spw
    """
    if  'freq' in xaxis:
        for spw0 in spw:
            plotms(vis,xaxis='freq',yaxis='amp',spw=spw0,
                   plotfile=vis+'.spw'+spw0+'_freq_amp.png',overwrite=True,showgui=False,
                   showatm=True,showtsky=False)
    if  'time' in xaxis:
        for spw0 in spw:
            plotms(vis,xaxis='time',yaxis='amp',spw=spw0,
                   plotfile=vis+'.spw'+spw0+'_time_amp.png',overwrite=True,showgui=False,
                   showatm=False,showtsky=False)

def rawSelect(name,correlation='RR,LL',keepflags=False,datacolumn='data'):
    """
    get rid of trunk rows to reduce the data size
    """
    mslist=glob.glob(name)
    for ms in mslist:
        os.system('rm -rf '+ms.replace('.ms','.selected.ms'))
        ctasks.mstransform(vis=ms,outputvis=ms.replace('.ms','.selected.ms'),correlation='RR,LL',keepflags=False,datacolumn='data')    
    
    return


