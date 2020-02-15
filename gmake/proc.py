import os

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

def rmPointing(outvis,verbose=False):
    """
    Empty the POINTING table
    """
    if  verbose==True:
        print("Before rmPointing()")
        os.system("du -hs "+outvis)
    
    ctb=ctools.table()
    ctb.open(outvis+'/POINTING',nomodify=False)
    ctb.removerows(range(ctb.nrows()))
    ctb.done()
    
    # rmtables(outvis+'/POINTING') # doesn't work
    
    if  verbose==True:
        print("After rmPointing()")
        os.system("du -hs "+outvis)
    
def setLogfile(logfile,overwrite=False,rmlast=False,onconsole=True):
    """
    Set CASA log file
    """
    if  overwrite==True:
        os.system('rm -rf '+logfile)
    if  rmlast==True:
        os.system('rm -rf '+ctasks.casalog.logfile())
    ctasks.casalog.setlogfile(logfile)
    ctasks.casalog.showconsole(onconsole=onconsole)


def checkchflag(vis):
    """
    check flag consistancy across channels
    it's able to handle ms with multiple spw/pol.

    note: miriad/invert slop=1,zero could include
          partionally flagged records into imaging
          We can run xutils.unchflag() and zero-out such data
          to implement a similar treatment:
          http://www.atnf.csiro.au/computing/software/miriad/userguide/node145.html
    """
    print("")
    print("run checkchflag on "+vis)
    print("")
        
    ctb=ctools.table()
    ctb.open(vis)
    ids=np.unique(ctb.getcol("DATA_DESC_ID"))

    for id in ids:
        
        print("")
        print('query: DATA_DESC_ID=='+str(id))        

        subtb=ctb.query('DATA_DESC_ID=='+str(id))
        flag=subtb.getcol('FLAG')
        shape=flag.shape
        
        print('data shape:  '+str(shape))
        print("")        
        
        for i in range(0,shape[0]):

            flag0=flag[[i],:,:] # this will make a copy
            flag0=flag0[0,:,:]  # otehrwise .view will not work
                                # flag0.strides
            flag0=flag0.view(','.join(shape[1]* ['i1']))
            unique_vals,indicies=np.unique(flag0, return_inverse=True)
            counts = np.bincount(indicies)
            
            print("pol id: "+str(i)+' variety: '+str(len(counts)))
            
            for j in range(0,len(counts)):
                u=str(unique_vals[j])
                u=re.sub('[(), ]', '', u)
                print(u+' '+str(counts[j])+'/'+str(shape[-1]))
        subtb.close()

    ctb.close()
    print("")
    
def getfreqs(vis,frame='LSRK',spwids=[0],edge=0):
    """
    get the frequency sampling grid of one SPW in a MS, in a specified frame 
    edge is for original grid
    """
    
    ms=ctools.ms()
    ms.open(vis)
    fgrid=ms.cvelfreqs(spwids=spwids,
                       mode='channel',
                       start=0,nchan=-1,width=1,outframe=frame)
    ms.close()
    if  edge>0:
        fgrid=fgrid[int(edge):-int(edge)]
    return fgrid

def getcommonfreqs(vis_list,spw_list,chanbin=2,frame='LSRK',edge=1):
    """
    chanbin: the channel width will be chanbin*max(chanwidth among vis_list)
    output freqgrid will be covered by all vis_list
    """
    fgrid_min=[]
    fgrid_max=[]
    fgrid_df=[]    
    for i in range(len(vis_list)):
        fgrid=getfreqs(vis=vis_list[i],spwids=[int(spw_list[i])],frame=frame,edge=edge)
        df=np.max(np.abs(fgrid[1:]-fgrid[:-1]))
        fgrid_min+=[min(fgrid)-df*0.5]
        fgrid_max+=[max(fgrid)+df*0.5]
        fgrid_df+=[df]
    fgrid_common_min=np.max(fgrid_min)
    fgrid_common_max=np.min(fgrid_max)
    fgrid_common_df=np.max(fgrid_df)
    
    df=fgrid_common_df*chanbin
    fgrid_start=fgrid_common_min+df*0.5
    fgrid_end=fgrid_common_max-df*0.5
    fgrid=np.arange(fgrid_start,fgrid_end,df)
    fgrid=fgrid[(fgrid >= fgrid_start) & (fgrid <= fgrid_end)]        
    
    return fgrid,df
    