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
        
def rmColumns(vis,column=""):
    """
    remove columns from MS (only handle one column currently)
    By default, the function will check the available column names without removing any column.
    e.g. column='WEIGHT_SPECTRUM'
    """
    
    ctb=ctools.table()
    ctb.open(vis,nomodify=False)
    if  (column!='' and (column in ctb.colnames()) ):
        ctb.removecols(column)
    #ctb.close()
    ctb.done()
    
    
def setLogfile(logfile,overwrite=False,rmlast=False,onconsole=True):
    """
    Set CASA log file
    """
    if  overwrite==True:
        os.system('rm -rf '+logfile)
    if  rmlast==True:
        os.system('rm -rf '+ctasks.casalog.logfile())
    if  logfile is None:
        fd, logfile= tempfile.mkstemp(suffix='.log')        
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
        
        
    """
    Additional Note
    ####
    # ToolBox can be used
    #   imager.advisechansel()
    #   ms.cvelfreqs()
    #   msmetadata.
    #   or something in analysisUtils
    ###
    
    
    
    
    setLogfile('tets_advisechansel.log')
    
    im=ctools.imager()
    msname='uid___A002_Xc69057_X91a.ms'
    #ctasks.listobs(vis=msname,field='BX610',intent='OBSERVE_TARGET#ON_SOURCE',spw='25,27,29,31')
    
    
    # im.advisechansel(getfreqrange=True) will give you
    # left edge and right edge
    
    out=im.advisechansel(msname=msname,\
                         spwselection='25',
                         getfreqrange=True,freqframe='LSRK')
    print(out)
    out=im.advisechansel(msname=msname,\
                         spwselection='25:0',
                         getfreqrange=True,freqframe='LSRK')
    print(out)
    
    msmd=ctools.msmetadata()
    msmd.open(msname)
    
    meanfreq = msmd.meanfreq(25)
    bandwidth = msmd.bandwidths(25)
    chanwidth = msmd.chanwidths(25)[0]
    
    msmd.close()
        
    import numpy as np
    print(fgrid-np.roll(fgrid,1)) 
    """    
        
    return fgrid

def getcommonfreqs(vis_list,spw_list,edge_list=None,frame='LSRK',chanbin=2):
    """
    edge_list: for each vis, we exclude some edge channels for evluation as they might be flagged in pipeline
    chanbin: the channel width will be chanbin*max(chanwidth among vis_list)
    output freqgrid will be covered by all vis_list
    fgrid:     freqeuncy grid
    df:        frequency resolution
    """
    fgrid_min=[]
    fgrid_max=[]
    fgrid_df=[]
    if  edge_list is None:
        edge_list=[0]*len(vis_list)    
    for i in range(len(vis_list)):
        fgrid=getfreqs(vis=vis_list[i],spwids=[int(spw_list[i])],frame=frame,edge=edge_list[i])
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

def flagbywt(vis,datacolumn='data',fitspw=''):
    """
    doesn't really work yet (see statwt.py)
    performe the following procedures:
        1. save current flagging
        2. use statwt to recalculate weight
        3. flag weightoutlier
    """

               
    if  not os.path.exists(vis+'.flagversions/flags.Original'):
        flagmanager(vis=vis,mode='save',versionname='Original',merge='replace',\
            comment='Before Flag by Weight')
    else:
        flagmanager(vis=vis,mode='restore',versionname='Original',merge='replace')

    statwt(vis=vis,fitspw=fitspw,combine='corr',minsamp=5,preview=False,\
           datacolumn=datacolumn,chanbin='spw',statalg='classic') #,timebin='300s',slidetimebin=True

    median_wt=au.getMeanWeights(vis,reportMedian=True)
    print(vis,'median_wt before flagging:',median_wt)
    
    flagdata(vis=vis,
           mode='clip',
           datacolumn='weight',
           clipminmax=[0,median_wt*5.0],clipoutside=True,clipzeros=True,action='apply')    

    median_wt=au.getMeanWeights(vis,reportMedian=True)
    print(vis,'median_wt after flagging:',median_wt)     
    
def flagrow(vis):      
    """
    flagged the entire row if it's partially flagged
    use this with cautions and you're removing potentially large amount of rows
    """
    ctb=ctools.table()
    ctb.open(vis,nomodify=False)
    flag=ctb.getcol('FLAG')
    shape=flag.shape
    # flag.shape: npol x nchanel x nrow
    print(vis+' '+str(shape))
    ncount=0
    
    """
    for i in range(0,shape[0]):
        for j in range(0,shape[-1]):
            flag0=np.sum(flag[i,:,j])
            if  flag0!=0 and flag0!=shape[-2]:
                flag[i,:,j]=True
                ncount+=1
    """
    for j in range(0,shape[-1]):
        flag0=np.sum(flag[:,:,j])
        if  flag0!=0 and flag0!=(shape[-2]*shape[-3]):
            flag[:,:,j]=True
            ncount+=1                
    
    print(ncount)
    ctb.putcol('FLAG',flag)
    ctb.done()    
    
    
def flagchan():
    """
    flagged the channel if the data from contributing rows are partially flagged
    this is <unchflag> in the CASA 5 xutils
    """
    pass
    