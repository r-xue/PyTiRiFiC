

"""
Hi,

I have a set of MS which contains a single spw with 240 channels in TOPO. My goal is to create a single wide-band channel from it in "LSRK" (let's ignore the bandwidth smearing at this moment).

I did some experiments and found the output visibility/flags/weight/values in the output MS is not very consistent, depending on what procedure I tried.
My test procedures and comments were attached.

In short, it seems that I can't do this in one shot of mstranform(), and I need to transfer the frame to "LSRK" first and then do binning in two separate steps to get the expected results. The drawback is just I/O, but I would like to understand why this happens from experts insight. From the documentation, mstranfom() has an order for called operations: first average then spectrum regridding+frame transform if both operations are called. I thought the sequence should be fine for my case but I eventually got flagged data with wrong weight values.


best,
Rui

#### test1

# This doesn't work
# 
# Looks like the pre-average of spectral regrdding is disabled since CASA 5.0
# Without this pre-averaging, even after I set the desired output grid as a very wide (2G) single channel, 
# the output wideband continuum channel will only be based on the adjacent/nearest spectral channels near the desired output "wide-band" channel center frequency.
# In this case, depending on the interpolation, SNR will only be boosted by a factor of:
#   x ~1 nearest (no boost)
#   x ~sqrt(2) nearest
#   x ~sqrt(3) cubic
# So I turn on chanaverage=True.
# Note: if some task can handle channel binning/resampling in a flux conservative fashion (i.e. mapping all corresponding fractions of input channels into one output channel using a frequency bracket ),
# this will be nice to clear up the confusion in the average-resampe mixing case.

visout1='visout1.ms'
vis='sample.ms'

#   averaging all channels into one continuum channel and transfer the frame at the same time.
#   the results are not right
#   all visibility is flagged
#   all weights values (from flagged data) are written as weight_spectrum X nbin x nbin (which is odd)

os.system('rm -rf '+visout1)
mstransform(vis=vis,outputvis=visout1,datacolumn='data',
            spw='0:249.188425~251.0087375GHz',
            regridms=True,outframe='LSRK',interpolation='nearest',
            chanaverage=True,chanbin=240,
            keepflags=False)
plotms(visout1,yaxis='weight',xaxis='uvdist') 
xu.checkchflag(visout1)
statwt(vis=visout1,preview=True,datacolumn='data',timebin=20,spw='0')  

#### test2

# This doesn't work either

visout2='visout2.ms'
visout1='visout1.ms'
vis='sample.ms'

#   averging all channels into one continuue channel 
#   the results looks fine execept that it's still in the TOPO frame
#   ouput weight = input weight_spectrum x nbin which is good
os.system('rm -rf '+visout1)
mstransform(vis=vis,outputvis=visout1,datacolumn='data',
            spw='0:249.188425~251.0087375GHz',
            chanaverage=True,chanbin=240,
            keepflags=False)
plotms(visout1,yaxis='weight',xaxis='uvdist') 
xu.checkchflag(visout1)
statwt(vis=visout1,preview=True,datacolumn='data',timebin=20,spw='0')  

#   transfer the single continuum channel from TOPO to LSRK
#   the results were completed flagged. Why is that? Not what I expected.
os.system('rm -rf '+visout2)
mstransform(vis=visout1,outputvis=visout2,datacolumn='data',
            regridms=True,outframe='LSRK',interpolation='nearest',
            keepflags=False)
plotms(visout2,yaxis='weight',xaxis='uvdist')
xu.checkchflag(visout2)
statwt(vis=visout2,preview=True,datacolumn='data',timebin=20,spw='0')  

#### test3

# This Works

visout2='bb1.mfs.ms'
visout1='bb1.lsrk.ms'
vis='sample.ms'

#   transfer all spectral channel from TOPO to LSRK without channel-wise binning 
os.system('rm -rf '+visout1)
mstransform(vis=vis,outputvis=visout1,datacolumn='data',
            regridms=True,outframe='LSRK',interpolation='nearest',
            keepflags=False)
#plotms(msname1,yaxis='weight',xaxis='uvdist') 
xu.checkchflag(visout1)
statwt(vis=visout1,preview=True,datacolumn='data',timebin=20,spw='0')  

#   binning in the 'LSRK' frame
#   the results looks good
os.system('rm -rf '+visout2)
mstransform(vis=visout1,outputvis=visout2,datacolumn='data',
            spw='0:249.188425~251.0087375GHz',
            chanaverage=True,chanbin=240,
            keepflags=False)
#plotms(msname,yaxis='weight',xaxis='uvdist')
xu.checkchflag(visout2)
statwt(vis=visout2,preview=True,datacolumn='data',timebin=20,spw='0')  

"""



















#   mstranforming "mfs" ms needs some close examinations (check log)
#   mstranform will do channel averageing first then regridding if both are turned on (which is not preferred here)
#   we have to turn off chanaverage.
#   "mode" only help define the "units" in start/width

                                                    
"""
msname='bx610_band6.bb2.mfs.ms'
omsname='../calibrated/uid___A001_X2fe_X20f_target.ms'
os.system('rm -rf '+msname)
os.system('rm -rf '+msname+'.flagversions')
mstransform(vis='../calibrated/uid___A001_X2fe_X20f_target.ms',outputvis=msname,datacolumn='data',field='BX610',
            timeaverage=False,timebin='30s',
            
            spw='1:250.79375~251.0828125GHz;251.3953125~251.8875GHz;252.16875~252.6140625GHz', # this actually consider three spw:chan selection
            
            #start='251700.0000MHz',width='1875.0000MHz',nchan=1,mode='frequency',combinespws=False,
            #outframe='LSRK',regridms=True,interpolation='linear',usewtspectrum=True,preaverage=False, # preaverage is disabled since v5.0
            
            #chanaverage=True,chanbin=120,  # avoid this as the results are flagged:
            
            #start='2.517479946e+11Hz',width='1.22646e+09Hz',nchan=1,mode='frequency', # this was defcided by chanaverage but actually missed some input channel
            #outframe='LSRK',regridms=True,mode='frequency',
            #interpolation='linear',combinespws=False,
            
            #spw='1:40~48',
            chanaverage=True,chanbin=157,
            
            #nchan=1,
            #start='251700.0000MHz',width='2300.0000MHz',nchan=1,combinespws=False,
            #start='2.517479946e+11Hz',width='1875MHz',nchan=1,mode='frequency',combinespws=False,
            
            #start='251700.0000MHz',width='2875.0000MHz',nchan=1,mode='frequency',combinespws=True,
            #start=120,width=240,nchan=1,mode='channel', # this will use the first spw in the original ms table (not good)
            #see http://www.eso.org/~scastro/ALMA/casa/MST/MSTransformDocs/node7.html
            
            keepflags=False)
#flagdata(vis=msname,mode='unflag',flagbackup=True)
statwt(vis=msname,preview=True,datacolumn='data',timebin=20)      
 
#statwt(vis=omsname,preview=True,datacolumn='data',timebin=10,spw='1:250.79375~251.0828125GHz;251.3953125~251.8875GHz;252.16875~252.6140625GHz')
#plotms(omsname,yaxis='weight',xaxis='uvdist',spw='1:250.79375~251.0828125GHz;251.3953125~251.8875GHz;252.16875~252.6140625GHz')
#plotms(msname,yaxis='weight',xaxis='uvdist')

"""

"""
sample/regrid and average are two different methods:

    if you actually want to bin the data; you have to use split() or mstransform(chanaverage=True)
    In general, you should make sure that the number of channels you are averaging together is an integer multiple of the original total number of channels

   mstransform:
           output data
           1.  average=True: do channel averging on selected channel (weight accumulated)
           2.  spw regridding (step1 results mapped into desired output
               this is actually a grid vector to grid vector mapping
               not precisly bracket to bracket calculation (so if we map undersampe a inpt spw using regridding,
                                                            the behavior more like a picking some sparse channels 
                                                            only boosting the signal-to-noise by a factor of 2 in linear:
                                                            "nearest" will only use information from 1 chan not boost SNR
                                                            "linear" will only use information from 2 chan boost SNR by sqrt(2)
                                                            "cubic"/'spline' will only use information from 4 chans boost SNR by 2
                                                            see CASA cookbook p218
                                                            or MSTransformRegridder.cc
   tclean:
        When image channels are wider than data channels, visibilities and weights are binned and gridded 
        via multi-frequency synthesis (MFS) within each image channel.
        so there is a automatical pre-averaging



"""
