import time
import os
import numpy as np
from astropy.io import fits
import emcee
import uuid
import random
import cPickle as pickle
from reproject import reproject_interp

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import subprocess
import corner
from copy import deepcopy
from astropy.io import ascii
import fnmatch
import pprint
import fitsio
import shutil
import commands
import multiprocessing
import numpy as np
import copy
import sys
import FITS_tools


from scipy.interpolate import Rbf
from scipy.interpolate import interpn
from astropy.convolution import Gaussian2DKernel, interpolate_replace_nans, convolve


def sort_on_runtime(p):
    p = np.atleast_2d(p)
    idx = np.argsort(p[:, 0])[::-1]
    return p[idx], idx

def unique_id(method='time',tic=0.0):
    """
    Generate a unique id for a single thread run
        method='time': not good enough for fast multi-threading programs
        method='uuid': long name but indeed unique
    """
    id=''
    if  method=='time':
        time.sleep(1.0/1e6)
        id=int((time.time()-tic)*1e5)
        print id
    if  method=='uuid':
        id=uuid.uuid4()
    if  method=='random':
        int_max=sys.maxint
        id=random.randint(0, INT_MAX)

    id=str(id)
    return id


def tirific_imprep(infile='',
                   outfile='',
                   delbeam=False,
                   newbeam=[]
                   ):
    
    im,hd=fits.getdata(infile,header=True)
    
    if  delbeam==True:
        del hd['BMAJ']
        del hd['BMIN']
        del hd['BPA']
    
    if  len(newbeam)==3:
        hd['BMAJ']=newmbeam[0]/3600.
        hd['BMIN']=newmbeam[1]/3600.
        hd['BPA']=newmbeam[2]
    
    hd['EPOCH']=2000.0
    fits.writeto(outfile,im,hd,overwrite=True)
    

def tirific_def():
    """
    default basic tirific parameter setup
    note:    only uppercase keys are for the tirific "def" file 
    """
    pars={  'LOGNAME':  'default.log',
            'PROMPT':   0,
            # for emcee, nwalker > cpu_core
            # use th nthreads rather than ncores here is more efcineint to avoid overhead
            'NCORES':   1, #multiprocessing.cpu_count(),  # quardcore machine ; turn off threading as emcee will take care of this
                           #ncores>1 will lead to overhead for multi-threads analaysi at higher-level 
            'INIMODE':  0,  # INIMODE=1, default in tirific
            'INSET':    'default.fits',
            'OUTSET':   'default_out.fits',
            'OUTCUBUP': 10000000.0,
            'BMIN':     10,
            'BMAJ':     10,
            'BPA':      -45,
            'RMS':      0.001,
            'NDISKS':    1,
            'NUR':      7,
            'REFRING':  2,
            'RADI':    '0 20 40 60 80 100 120 140 160 180 200',
            'VROT':     400,
            'SDIS':     100,
            'CLNR':     1,
            'Z0':       0.03,
            'SBR':      1E-4,
            'INCL':     75,
            'PA':       0,
            'XPOS':     0,
            'YPOS':     0,
            'LC0':      0.0,
            'LS0':      0.0,
            'VSYS':     1185,
            'AZ1P':     0,
            'AZ1W':     360,
            'CONDISP':  0.0,
            'LTYPE':    2.0,
            'CFLUX':    1e-2,
            'WEIGHT':   0,
            'ISEED':    8981,
            'RADSEP':   0.05,
            'FITMODE':   2,
            'LOOPS':    0,
            'MAXITER':  '',
            'CALLITE':  '',
            'SIZE':     4,
            'INTY':     0,
            'VARINDX':  '',
            'VARY':     'VROT',
            'ACTION':   1,
            'COOLGAL':  '',
            'COOLBEAM': 0.06,
            'COOLBIN':  1,
            #   PARAMETER PLOTTING,
            'GR_CONT':      1,
            'GR_DEVICE':    '',
            'GR_PARMS':     'RADI SBR VROT PA INCL SDIS',
            'GR_SBRP':      1,
            'GR_LGND':      1,    
            'GR_TXHT':      1.0,
            'GR_SBHT':      0.5,   
            'GR_MR':        5, 
            'GR_ML':        5,
            'GR_SYMB_1':    -1,
            'GR_SIZE_1':    1,  
            'GR_COL_1':     1, 
            'GR_LINES_1':   1,
            'GR_SYMB_2':    -1,
            'GR_SIZE_2':    1,  
            'GR_COL_2':     1, 
            'GR_LINES_2':   1,
            'GR_SYMB_3':    -1,
            'GR_SIZE_3':    1,  
            'GR_COL_3':     1, 
            'GR_LINES_3':   1,
            'GR_SYMB_4':    -1,
            'GR_SIZE_4':    1,  
            'GR_COL_4':     1, 
            'GR_LINES_4':   1,
            'GR_SYMB_5':    -1,
            'GR_SIZE_5':    1,  
            'GR_COL_5':     1, 
            'GR_LINES_5':   1
            }                        
    
    return pars

def tirific_diskmod(imset,disks,
                    verbose=True,
                    decomp=True,
                    beam=True,
                    moms=False,
                    inty=0,
                    maxnur=None,
                    ppp=True):
    """
        computing time tests:
            1x124x48x38:    1.208s
            1x124x48x36:    1.200s
            1x60x50x25:     0.792s
            128x48x36:      1.155s
            128x128x128:    6.666s
            124x50x25:      1.010s  
            128x50x25:      0.982s
            96x36x25:       0.874s 
            2a 3b 5c 7d 11e 13f, where e+f is either 0 or 1,
            Most computing time is spend on FFT, so...
            We want to:
                * keep the FFT pixel optimnzation rule
                * reduce the velocity channel number as much as possible
                    +typically the cube is not heavily oversampled in velocity, so avoid rebin to loose velocity infromation
                    +we can restrict to velocity range interested in... (alising won't happen in velocity for TIRIFIC+sdis)
                + pixel is typically heavily oversampled, so we can rebin to 1/2 and 1/3 FWHM without lossing much....
                  We still want some pading space around ROI.  
        machine test:
            96x36x25: hr  0.820s (openmp,v2.3.9,OSX)
            96x36x25: nuc 0.895s (openmp,v2.3.9,ubuntu16.04)
    """
    
    pars=tirific_def()
    
    #pars['INSET']=imset['INSET']
    #pars['BMAJ']=imset['BMAJ']
    #pars['BMIN']=imset['BMIN']
    #pars['BPA']=imset['BPA']
    #pars['c']=imset['CONDISP']
    #   ABOUT CONDISP:
    #       http://gigjozsa.github.io/tirific/model_geometry.html#Gridding
    #
    #   LOAD UPPER CASE KEYWORDS <---
    #   RADI, RADSEP, BMAJ, BMIN, BPA, CONDISP, which are valid for all disks (not _i)
    pars['INTY']=inty

    
    for k, v in imset.items():
        if  k.isupper()==True: 
            pars[k]=deepcopy(v)
    
    if  beam==False:
        pars['BMAJ']=0.0
        pars['BMIN']=0.0
        pars['COOLBEAM']=0.03

        #   CLNR time penalty
        #http://gigjozsa.github.io/tirific/model_geometry.html#Velocity%20dispersion 
        #   noteL BEAM CONVOLVING FFT is the most costly actually.
        #   1:  1.48s   x10
        #   3:  1.48s   x10
        #   5:  1.52s   x10
        #   10: 1.56s   x10
        #   overall, increasing point source doesn't add up much for computing time.
        #   most time was spended on FFT
        #
        # the trade-off between condisp and sdist
        #http://gigjozsa.github.io/tirific/model_geometry.html#Instrumental function
        #   condisp: using FFT to introduce dispersion
        #   sdist:   using random MCMC process.....
        #   this two methods actually make different if pixel sampling is coarse
        # avoid aliasing:
        #Always leave a border of 5-6sigmaor 2.5 - 3 HPBWs between the model and the borders of the float-accuracy (input) data cube.
        #   CONDISP introduce a smoothing in velocity after gridding.
        #   after the gridding already taken careful of cube pixelization.
        # since our channel sampling is bad, we prefer to fold the instructmetal braoding into sdis
    if  verbose==True:
        print "+"*90
        print "outfolder:"+imset['outfolder']
        print "outname:  "+imset['outname']
        print "imset:    "+imset['INSET']
        print "lines:    "+imset['lines']
        print "objects:  "+imset['objects']
        print "+"*90
    # LOAD DISK ONE BY ONE
    idisk=0
    comp_name=[]
    comp_tag=[]
    
    #   pick the common RADI/NUR Values
    pars['RADI']=0
    pars['NUR']=1
    
                

    #tic=time.time() #<---
    #print '-->Took {0} seconds to execute TiRiFic'.format(float(time.time()-tic)/float(1)) #<-
    for disk in disks:

        #tic=time.time() #<---
        #print fnmatch.fnmatch(imset['lines'],'*'+disk['line']+'*') and fnmatch.fnmatch(imset['objects'],'*'+disk['object']+'*')
        #print 'Took {0} seconds to execute TiRiFic'.format(float(time.time()-tic)/float(1)) #<--    
        #tic=time.time() #<---
        #reg1=re.compile('.*'+disk['line']+'.*\\Z(?ms)')
        #reg2=re.compile('.*'+disk['object']+'.*\\Z(?ms)')
        #print reg1.match(imset['lines']) and reg1.match(imset['objects'])
        #print '->Took {0} seconds to execute TiRiFic'.format(float(time.time()-tic)/float(1)) #<--   
        #tic=time.time() #<---
        #print (disk['line'] in imset['lines']) and (disk['object'] in imset['objects'])
        #print '-->Took {0} seconds to execute TiRiFic'.format(float(time.time()-tic)/float(1)) #<-- 
        
        # use in rather than fnmatch.fnmatch
          
        if  (disk['line'] in imset['lines']) and (disk['object'] in imset['objects']):            
            if  len(disk['radi'])>pars['NUR']:
                pars['RADI']=disk['radi'] ; pars['NUR']=len(disk['radi'])

    if  verbose==True:
        print 'common radi',pars['RADI']
      
    
    for disk in disks:
        
        if  (disk['line'] in imset['lines']) and (disk['object'] in imset['objects']):
            
            idisk+=1
            disktag='' if  idisk==1 else '_'+str(idisk)
            
            comp_name+=['_'+disk['line']+'_'+disk['object']]
            comp_tag+=[disktag]
            
            pars['PA'+disktag]=disk['pa']
            pars['VSYS'+disktag]=disk['vsys']
            pars['INCL'+disktag]=disk['inc']
            pars['XPOS'+disktag]=disk['xypos'][0] ; pars['YPOS'+disktag]=disk['xypos'][1]

            pars['VROT'+disktag]=disk['vrot']
            
            ####################################
            #   PICK A VDISP SETUP
            ####################################
            
            pars['SDIS'+disktag]=pars['RADI']*0.+10.0
            
            pars['Z0'+disktag]=deepcopy(pars['Z0'])
            pars['LTYPE'+disktag]=deepcopy(pars['LTYPE'])
            
            # notnesscary, willrepeat by itself
            pars['CLNR'+disktag]=deepcopy(pars['CLNR'])
            pars['RADSEP'+disktag]=deepcopy(pars['RADSEP'])
            
            pars['LC0'+disktag]=pars['RADI']*0.
            pars['LS0'+disktag]=pars['RADI']*0.
            if  'lc0' in disk.keys():
                (pars['LC0'+disktag])[0:len(disk['radi'])]=disk['lc0']
            if  'ls0' in disk.keys():
                (pars['LS0'+disktag])[0:len(disk['radi'])]=disk['ls0']                
            
            if  'vdisp' in disk.keys():            
                (pars['SDIS'+disktag])[0:len(disk['radi'])]=disk['vdisp']
            if  'ldisp' in disk.keys():
                (pars['SDIS'+disktag])[0:len(disk['radi'])]=disk['ldisp'][0]+\
                (disk['ldisp'][1]-disk['ldisp'][0])/(np.max(disk['radi'])-np.min(disk['radi']))*disk['radi']
            if  'edisp' in disk.keys():
                (pars['SDIS'+disktag])[0:len(disk['radi'])]=disk['edisp'][0]*np.exp(-disk['edisp'][1]*disk['radi'])              
            
            if  'ltype' in disk.keys():
                pars['LTYPE'+disktag]=disk['ltype']
            if  'z0' in disk.keys():
                pars['Z0'+disktag]=disk['z0']            

                            
            ####################################
            #   PICK A SURFACE BRIGHTNESS SETUP
            ####################################
            #build analytical profile if the parameters are provided
            #https://en.wikipedia.org/wiki/Sersic_profile
            #   [0] normalization
            #   [2] sersic index
            #   EXP S-BRIGHTNESS
            #   I=I0exp(-R/RS) <==> Itotal=2pi*RS^2*I
            pars['SBR'+disktag]=pars['RADI']*0.0
            if  'sbr' in disk.keys():
                (pars['SBR'+disktag])[0:len(disk['radi'])]=disk['sbr']
            if  'esbr' in disk.keys():
                (pars['SBR'+disktag])[0:len(disk['radi'])]=disk['esbr'][0]/2.0/np.pi/(disk['esbr'][1]**2)*np.exp(-disk['radi']/disk['esbr'][1])
            if  'dsbr' in disk.keys():
                (pars['SBR'+disktag])[0:len(disk['radi'])]=sdisk['dsbr'][0]*np.exp(-disk['dsbr'][1]*(disk['radi']**0.25))
            if  'ssbr' in disk.keys():
                (pars['SBR'+disktag])[0:len(disk['radi'])]=disk['ssbr'][0]*np.exp(-disk['ssbr'][1]*(disk['radi']**(pars['ssbr'][2])))


            pars['SM1A'+disktag]=pars['RADI']*0.0
            pars['SM1P'+disktag]=pars['RADI']*0.0
            if  'sm1a' in disk.keys():
                (pars['SM1A'+disktag])[0:len(disk['radi'])]=disk['sm1a']*(pars['SBR'+disktag])[0:len(disk['radi'])]
            if  'sm1p' in disk.keys():
                (pars['SM1P'+disktag])[0:len(disk['radi'])]=disk['sm1p']
    
            # cflux_scale:  relative units
            # cflux:        absolute units
            #   cflux is not costly either (same as CLNR)
            #   1e-4:   1.2s    <- no point source is created because it's just too high....
            #   1e-5    1.4s
            #   1e-6    1.6s
            pars['CFLUX'+disktag]=0
            if 'cflux_scale' in imset.keys():
                pars['CFLUX'+disktag]=np.min((pars['SBR'+disktag])[0:len(disk['radi'])])*imset['cflux_scale']
            if 'cflux' in imset.keys():
                pars['CFLUX'+disktag]=deepcopy(imset['cflux'])
            if  pars['CFLUX'+disktag]==0:
                pars['CFLUX'+disktag]=1e-5
            
            
            
                
            if  'vshift_'+disk['line'].lower() in imset.keys():
                pars['VSYS'+disktag]+=imset['vshift_'+disk['line'].lower()]
            
            #   hack for ealier imsets save; wil be removed later
            #if  'vshift_water' not in imset.keys():
            #    if  ('CO76' in imset['lines']) and ('CI' in imset['lines']) and disk['line']=='CI':
            #        pars['VSYS'+disktag]=-997.17281
            
            if  verbose==True:
                print ""
                print ">>>disk"+str(idisk)+':'
                pprint.pprint(disk)
            
    
    pars['NDISKS']=idisk
    

            
    if  not os.path.exists(imset['outfolder']):
            os.makedirs(imset['outfolder'])
            
    postfix=['']
    # skip the combined run
    if  decomp==True:
        #postfix=[]
        postfix+=comp_name


    if  maxnur!=None:
        pars['NUR']=deepcopy(maxnur)
        pars['RADI']=deepcopy((pars['RADI'])[0:maxnur])
        
    for ind in range(len(postfix)):

        parfile=imset['outfolder']+'/'+imset['outname']+postfix[ind]+'.par'
        if  os.path.exists('/opt/tirific-2.3.9/bin/tirific'):
            cmd='/opt/tirific-2.3.9/bin/tirific'
        else:
            cmd='/home/rui/tirific-2.3.9/bin/tirific'

        cmd+=' deffile='+parfile
        
        pars['OUTSET']=imset['outfolder']+'/'+imset['outname']+postfix[ind]+'_ppv.fits'
        if  os.path.exists(pars['OUTSET']): os.remove(pars['OUTSET'])
        
        if  ppp==True:
            
            pars['COOLGAL']=imset['outfolder']+'/'+imset['outname']+postfix[ind]+'_ppp.fits'
            pars['TABLE']=imset['outfolder']+'/'+imset['outname']+postfix[ind]+'_table.txt'
            pars['BIGTABLE']=imset['outfolder']+'/'+imset['outname']+postfix[ind]+'_bigtable.txt'
            pars['GR_DEVICE']=imset['outfolder']+'/'+imset['outname']+postfix[ind]+'_rad.ps/vcps'
            # avoid appending bigtable/table
            
            if os.path.exists(pars['BIGTABLE']): os.remove(pars['BIGTABLE'])
            if os.path.exists(pars['TABLE']): os.remove(pars['TABLE'])
            if os.path.exists(pars['COOLGAL']): os.remove(pars['COOLGAL'])
            
        pars['LOGNAME']=imset['outfolder']+'/'+imset['outname']+postfix[ind]+'.log'
        
        pars0=deepcopy(pars)

        if  ind>0:
            for tag in comp_tag:
                if  comp_tag[ind-1]!=tag:
                    pars0['SBR'+tag]=pars0['SBR'+tag]*0.0
                    pars0['SM1A'+tag]=pars0['SM1A'+tag]*0.0
            pars0['GR_PARMS']=  'RADI'+' SBR'+comp_tag[ind-1]+\
                                ' VROT'+comp_tag[ind-1]+' PA'+comp_tag[ind-1]+\
                                ' INCL'+comp_tag[ind-1]+' SDIS'+comp_tag[ind-1]+\
                                ' SM1A'+comp_tag[ind-1]+' SM1P'+comp_tag[ind-1]
        fo=open(parfile, "w")
        fo.write('#\n')
        fo.write('#'+cmd+'\n')
        fo.write('#\n\n')

        keys=pars0.keys()
        keys=sorted(keys)
        for k in keys:
            v=pars0[k]
            if  k.isupper()==True:  #only the uppercase keywords are loaded 
                if  type(v)!=type(''):
                    try:
                        iter(v)
                        v_str=" ".join('{0}'.format(x) for x in v)
                    except TypeError:
                        v_str=str(v)
                else:
                    v_str=str(v)
                output="{0:<25} = {1:<60}".format(str(k),v_str)+"\n"
                fo.write(output)
        fo.close()

        
        if  verbose==True:
             
            tic=time.time()
            os.system(cmd)
            print 'Took {0} seconds to execute TiRiFic'.format(float(time.time()-tic)/float(1))
                      
        else:
            
            # pick the fast one
            #tic=time.time()
            sstdout=commands.getoutput(cmd)
            #print 'Took {0} seconds to execute TiRiFic'.format(float(time.time()-tic)/float(1))
            #os.system(cmd)
            #status=subprocess.call(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            
        if  moms==True:
            data_cube,data_hd=fits.getdata(imset['outfolder']+'/'+imset['outname']+postfix[ind]+'_ppv.fits',header=True)
            data_mom0=np.sum(data_cube,axis=0)*data_hd['CDELT3']/1000.0
            fits.writeto(imset['outfolder']+'/'+imset['outname']+postfix[ind]+'_ppv_mom0.fits',data_mom0,data_hd,overwrite=True)

    if  verbose==True:
        print "+"*90
        print ""
      #
      
    return

def tirific_lnlike(theta,data,
                   imsets,disks,
                   mcpars,
                   beam=True,inty=1,maxnur=None,
                   ppp=False,uuid=True,verbose=False,moms=False,
                   decomp=False,faceon=False,
                   tmpfolder=True,
                   usesp=True,
                   keepfile=False):
    """
    the likelihood function
        theta:   the fitting parameter to be evaluated 
        data:    data to be evaluated
        pars:    the mcmc run setups parameters
        uuid:    if uuid is off... we would treat the run as a test for MC samplings
        usesp:   false: do not use sampling array
    NOTE:
        we try to prevent the BBarolo exception from:
           + high inc
        p_keys example:
            xy1_roi4_water
            the first element of 'xypos' from the disk roi4/water
    """

    #   MODIFIELD DISKS TO CREATE SAMPLING MODELS
    
    
    
    mdisks=deepcopy(disks)
    p_keys=deepcopy(mcpars['p_keys'])
    
    blobs={'lnprob':0.0,'chisq':0.0,'ndata':0.0,'npar':len(theta)}
    postproc=False
    
    for ind in range(len(mdisks)):

        
        theta_sub=[theta[x] for x in range(len(theta)) if ('x'+mdisks[ind]['object']==p_keys[x])] 
        if  len(theta_sub)!=0:
            (mdisks[ind]['xypos'])[0]=theta_sub[0]
        
        
        theta_sub=[theta[x] for x in range(len(theta)) if ('y'+mdisks[ind]['object']==p_keys[x])]
        if  len(theta_sub)!=0:
            (mdisks[ind]['xypos'])[1]=theta_sub[0]            
        
        theta_sub=[theta[x] for x in range(len(theta)) if ('vr' in p_keys[x]) and (mdisks[ind]['object'] in p_keys[x]) ]
        if  len(theta_sub)!=0:
            # skip the missing elements
            tmp3=len(mdisks[ind]['vrot'])-len(theta_sub)
            (mdisks[ind]['vrot'])[tmp3:]=theta_sub
            
        theta_sub=[theta[x] for x in range(len(theta)) if ('lc' in p_keys[x]) and (mdisks[ind]['object'] in p_keys[x]) ]
        if  len(theta_sub)!=0:
            # skip the missing elements
            tmp3=len(mdisks[ind]['lc0'])-len(theta_sub)
            (mdisks[ind]['lc0'])[tmp3:]=theta_sub
        theta_sub=[theta[x] for x in range(len(theta)) if ('ls' in p_keys[x]) and (mdisks[ind]['object'] in p_keys[x]) ]
        if  len(theta_sub)!=0:
            # skip the missing elements
            tmp3=len(mdisks[ind]['ls0'])-len(theta_sub)
            (mdisks[ind]['ls0'])[tmp3:]=theta_sub                        
            
        theta_sub=[theta[x] for x in range(len(theta)) if ('pa'+mdisks[ind]['object']==p_keys[x])]
        if  len(theta_sub)!=0:
            mdisks[ind]['pa']=theta_sub[0]
            
        theta_sub=[theta[x] for x in range(len(theta)) if ('in'+mdisks[ind]['object']==p_keys[x])]
        if  len(theta_sub)!=0:
            mdisks[ind]['inc']=theta_sub[0]
        if  faceon==True:
            mdisks[ind]['inc']=mdisks[ind]['inc']*0.0

        theta_sub=[theta[x] for x in range(len(theta)) if ('vs'+mdisks[ind]['object']==p_keys[x])]
        if  len(theta_sub)!=0:
            mdisks[ind]['vsys']=theta_sub[0]                                          
        

        theta_sub=[theta[x] for x in range(len(theta)) if ('vd' in p_keys[x]) and (mdisks[ind]['object'] in p_keys[x]) ]
        if  len(theta_sub)!=0:
            mdisks[ind]['vdisp']=np.array(mdisks[ind]['vrot'])*0.0+theta_sub[0]
            
        theta_sub=[theta[x] for x in range(len(theta)) if ('vd' in p_keys[x]) and (mdisks[ind]['line']+mdisks[ind]['object'] in p_keys[x]) ]
        if  len(theta_sub)!=0:
            mdisks[ind]['vdisp']=np.array(mdisks[ind]['vrot'])*0.0+theta_sub            

            
        theta_sub=[theta[x] for x in range(len(theta)) if ('ld' in p_keys[x]) and (mdisks[ind]['object'] in p_keys[x]) ]
        if  len(theta_sub)!=0:
            mdisks[ind]['ldisp']=theta_sub            

        theta_sub=[theta[x] for x in range(len(theta)) if ('ed' in p_keys[x]) and (mdisks[ind]['object'] in p_keys[x]) ]
        if  len(theta_sub)!=0:
            mdisks[ind]['edisp']=theta_sub            
            
        theta_sub=[theta[x] for x in range(len(theta)) if ('es' in p_keys[x]) and (mdisks[ind]['line']+mdisks[ind]['object'] in p_keys[x]) ]
        if  len(theta_sub)!=0:
            mdisks[ind]['esbr']=theta_sub     

        theta_sub=[theta[x] for x in range(len(theta)) if ('sb' in p_keys[x]) and (mdisks[ind]['line']+mdisks[ind]['object'] in p_keys[x]) ]
        if  len(theta_sub)!=0:
            mdisks[ind]['sbr']=theta_sub 

            
        theta_sub=[theta[x] for x in range(len(theta)) if ('sm1a' in p_keys[x]) and (mdisks[ind]['line']+mdisks[ind]['object'] in p_keys[x]) ]
        if  len(theta_sub)!=0:
            tmp3=len(mdisks[ind]['sm1a'])-len(theta_sub)
            #mdisks[ind]['sm1a'][tmp3:]=theta_sub   
            mdisks[ind]['sm1a'][1:(1+len(theta_sub))]=theta_sub                                             
        
        theta_sub=[theta[x] for x in range(len(theta)) if ('sm1p' in p_keys[x]) and (mdisks[ind]['line']+mdisks[ind]['object'] in p_keys[x]) ]
        if  len(theta_sub)!=0:
            tmp3=len(mdisks[ind]['sm1p'])-len(theta_sub)
            mdisks[ind]['sm1p'][1:(1+len(theta_sub))]=theta_sub

        #   when the "flat-field" model is detected, start the model with a constant surface brightness first.
        theta_sub=[theta[x] for x in range(len(theta)) if ('is' in p_keys[x]) and (mdisks[ind]['line']+mdisks[ind]['object'] in p_keys[x]) ]
        if  len(theta_sub)!=0:
            mdisks[ind]['esbr']=[1.0,0.0]      
            postproc=True
            
    #   MAKE MODEL IMAGE BY IMAGE
    #   DIR Structure:
    #       mcpars['outfolder']+'/'+uuid:
    #           imlist0*fits
    #           imlist1*fits
    #           imlist2*fits
    outfolder=mcpars['outfolder']      
    if  uuid==True:
        if  tmpfolder==True:
            outfolder='/tmp/'+unique_id(method='uuid')
        else:
            outfolder=outfolder+'/'+unique_id(method='uuid')
    
    
    for imlist0 in mcpars['imlist']:
        
        imset=deepcopy(imsets[imlist0])
        imset['outname']=imlist0
        imset['outfolder']=outfolder
        
        #tic=time.time() #<---
        #print postproc
        if  postproc==False:
            #tic0=time.time()
            tirific_diskmod(imset,mdisks,verbose=verbose,decomp=decomp,ppp=ppp,beam=beam,moms=moms,inty=inty,maxnur=maxnur)
            #print 'Took {0} second for one trial'.format(float(time.time()-tic0))
        else:
            tirific_diskmod(imset,mdisks,verbose=verbose,decomp=True,ppp=ppp,beam=False,moms=moms,inty=inty,maxnur=maxnur)
            mo_smo=0.0
            for disk in mdisks:
                if  (disk['line'] in imset['lines']) and (disk['object'] in imset['objects']):
                    comp_name=disk['line']+'_'+disk['object']
                    #print disk['line']+disk['object']
                    theta_sub=[theta[x] for x in range(len(theta)) if ('is' in p_keys[x]) and (disk['line']+disk['object'] in p_keys[x]) ]
                    #print np.shape(data[imlist0]['ix'])
                    #print np.shape(theta_sub)
                    rbf=Rbf(data[imlist0]['ix'],data[imlist0]['iy'],theta_sub,function='linear')
                    fs=rbf(data[imlist0]['xx'],data[imlist0]['yy'])
                    mo=fitsio.read(imset['outfolder']+'/'+imset['outname']+'_'+comp_name+'_ppv.fits')
                    mo_smo=mo_smo+convolve(mo*fs,data[imlist0]['pf'])
                    if  uuid==False:
                        fits.writeto(imset['outfolder']+'/'+imset['outname']+'_'+comp_name+'_ppv_smo.fits',mo_smo,data[imlist0]['hd'],overwrite=True) # use the data hd
                        fits.writeto(imset['outfolder']+'/'+imset['outname']+'_'+comp_name+'_ppv_fis.fits',fs,data[imlist0]['hd'],overwrite=True) # use the data hd
                        fs=fs*0.0
                        fs[data[imlist0]['iy'],data[imlist0]['ix']]=theta_sub
                        fits.writeto(imset['outfolder']+'/'+imset['outname']+'_'+comp_name+'_ppv_fs.fits',fs,data[imlist0]['hd'],overwrite=True) # use the data hd
        #print 'Took {0} seconds to execute TiRiFic'.format(float(time.time()-tic)/float(1)) #<---
        
        lnf=imset['lnf']
        theta_sub=[theta[x] for x in range(len(theta)) if (p_keys[x]=='lnf'+imlist0)]
        if  len(theta_sub)!=0:
            lnf=theta_sub[0]
        #print lnf
        #    EVALUET LIKELIHOOD
        lnl=-np.inf
        lnl1=np.inf
        lnl2=np.inf
        
        
        if  'sp_fine' in (data[imlist0]).keys():
            spcube_fine=deepcopy(data[imlist0]['sp_fine'])
            if  usesp==False:
                spcube_fine=spcube_fine*0.0+1.0
        
        spcube=deepcopy(data[imlist0]['sp'])
        if  usesp==False:
            spcube=spcube*0.0+1.0
        # method 1; use finner cube
        # method 2; oversample corsar cube
        # method 4: sparse sampling coarsar cube
        if  (postproc==False and os.path.isfile(imset['outfolder']+'/'+imset['outname']+'_ppv.fits')) or postproc==True:
            #   the keywords from tirific (.ppv) can be imcompleted (e.g. bmaj/bmin missed)
            #   fitsios is slightly faster
            #   mo=fits.getdata(imset['outfolder']+'/'+imset['outname']+'_ppv.fits')              
            if  postproc==True:
                mo=deepcopy(mo_smo)
            else:
                mo=fitsio.read(imset['outfolder']+'/'+imset['outname']+'_ppv.fits')
            
            if  'sp_fine' in (data[imlist0]).keys():
                
                #hdu = fits.open(imset['outfolder']+'/'+imset['outname']+'_ppv.fits')[0]
                #hdu.header=deepcopy(data[imlist0]['hd'])
                #hdu.data=np.expand_dims(hdu.data,axis=0)
                #tmphd=deepcopy(data[imlist0]['hd_fine'])
                
                # method 1 (signifcant slower)
                #ticx=time.time()
                #mo_fine,fp=reproject_interp(hdu,tmphd)
                #print 'Took {0} second for rpj'.format(float(time.time()-ticx))
                #fits.writeto('test_mo.fits',mo_fine,tmphd,overwrite=True)
                #fits.writeto('test_fp.fits',fp,tmphd,overwrite=True)
                
                
                # method 2 (faster, results more or less the same)
                #ticx=time.time()
                mo_fine=FITS_tools.regrid_cube(mo,deepcopy(data[imlist0]['hd']),deepcopy(data[imlist0]['hd_fine']),\
                                               order=1,mode='constant',out_of_bounds=0.0,preserve_bad_pixels=False)
                #print 'Took {0} second for rpj'.format(float(time.time()-ticx))
                #fits.writeto('test2_mo.fits',mo_fine,deepcopy(data[imlist0]['hd_fine']),overwrite=True)
                
                sigma2_fine=data[imlist0]['em_fine']**2.0*np.exp(2.0*lnf)
                lnl1=np.sum( (data[imlist0]['im_fine']-mo_fine)**2/sigma2_fine*spcube_fine )
                lnl2=np.sum( np.log(sigma2_fine*2.0*np.pi)*spcube_fine )
                lnl=-0.5*(lnl1+lnl2)
                
            else:
                
                
                imtmp=np.squeeze(data[imlist0]['em'])
                nxyz=np.shape(imtmp)
                #print nxyz
                imtmp=interpn((np.arange(nxyz[0]),np.arange(nxyz[1]),np.arange(nxyz[2])),\
                                                imtmp,data[imlist0]['hex_ind'],method='linear')
                sigma2=imtmp**2.0*np.exp(2.0*lnf)
                imtmp=np.squeeze(data[imlist0]['im']-mo)
                imtmp=interpn((np.arange(nxyz[0]),np.arange(nxyz[1]),np.arange(nxyz[2])),\
                                                imtmp,data[imlist0]['hex_ind'],method='linear')
                lnl1=np.sum( (imtmp)**2/sigma2 )
                lnl2=np.sum( np.log(sigma2*2.0*np.pi) )
                
                
                """
                sigma2=data[imlist0]['em']**2.0*np.exp(2.0*lnf)
                lnl1=np.sum( (data[imlist0]['im']-mo)**2/sigma2*spcube )
                lnl2=np.sum( np.log(sigma2*2.0*np.pi)*spcube )
                """
                
                lnl=-0.5*(lnl1+lnl2)
                
            if  uuid==False:
                fits.writeto(imset['outfolder']+'/'+imset['outname']+'_ppv.fits',mo,data[imlist0]['hd'],overwrite=True) # use the data hd
                fits.writeto(imset['outfolder']+'/'+imset['outname']+'_rs.fits',data[imlist0]['im']-mo,data[imlist0]['hd'],overwrite=True)

        if  uuid==False:
            fits.writeto(imset['outfolder']+'/'+imset['outname']+'_im.fits',data[imlist0]['im'],data[imlist0]['hd'],overwrite=True)
            fits.writeto(imset['outfolder']+'/'+imset['outname']+'_em.fits',data[imlist0]['em'],data[imlist0]['hd'],overwrite=True)
            fits.writeto(imset['outfolder']+'/'+imset['outname']+'_bl.fits',data[imlist0]['bl'],data[imlist0]['hd'],overwrite=True)
            fits.writeto(imset['outfolder']+'/'+imset['outname']+'_dt.fits',data[imlist0]['dt'],data[imlist0]['hd'],overwrite=True)
            fits.writeto(imset['outfolder']+'/'+imset['outname']+'_hx.fits',data[imlist0]['hx'],data[imlist0]['hd'],overwrite=True)
            fits.writeto(imset['outfolder']+'/'+imset['outname']+'_sp.fits',spcube,data[imlist0]['hd'],overwrite=True)
            tmp=np.squeeze(deepcopy(spcube*0.0))
            nd=np.shape(data[imlist0]['hex_ind'])
            for kk in range(nd[0]):
                ind=np.int_((data[imlist0]['hex_ind'])[kk,:])
                tmp[ind[0]][ind[1]][ind[2]]=1.0
            fits.writeto(imset['outfolder']+'/'+imset['outname']+'_si.fits',tmp,data[imlist0]['hd'],overwrite=True)
            
        if  verbose==True:
            print imset['outfolder']+'/'+imset['outname']+'_ppv.fits'
            print lnl1,lnl2,lnl

            
        blobs['lnprob']+=lnl
        blobs['chisq']+=lnl1
        if  'sp_fine' in (data[imlist0]).keys():
            blobs['ndata']+=np.sum(spcube_fine)
        else:
            #blobs['ndata']+=np.sum(spcube)
            blobs['ndata']+=(np.shape(data[imlist0]['hex_ind']))[0]
    
        
        
    lnl=blobs['lnprob']
    
    if  verbose==True:
        print""
        print outfolder
        print lnl,blobs
    
    
    if  keepfile==False:
        shutil.rmtree(outfolder)
        # subprocess is slower than os.syetem("rm -rf XXX") and shutil.rmtree()
        #cmd0clean='rm -rf '+outfolder
        #status=subprocess.call(cmd0clean,shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    
    
    return lnl,blobs 
    
    

def tirific_lnprior(theta,mcpars):
    """
    pass through the likelihood prior function (limiting the parameter space)
    """
    p_keys=mcpars['p_keys']
    p_lo=mcpars['p_lo']
    p_up=mcpars['p_up']
    for index in range(len(theta)):
        if  theta[index]<p_lo[index] or theta[index]>p_up[index]:
            return -np.inf
    return 0.0

def tirific_lnprob(theta,data,imsets,disks,mcpars,verbose=False):
    """
    pass through a validation
    +++ this is the function for MCMC 
    """
    lp = tirific_lnprior(theta,mcpars)
    if  not np.isfinite(lp):
        blobs={'lnprob':-np.inf,'chisq':+np.inf,'ndata':0.0,'npar':len(theta)}
        return -np.inf,blobs
    if  verbose==True:
        print "try ->",theta
    lnl,blobs=tirific_lnlike(theta,data,imsets,disks,mcpars)
    return lp+lnl,blobs

def tirific_chisq(theta,data=None,imsets=None,disks=None,mcpars=None,verbose=False):
    """
    pass through a validation
    +++ this is the function for AMOEBA_FIT
    don't use the sampling array here: 
        for iterative fitting, we don't care about the absolute value of chisq here
        for MCMC, we may want to keep usesp=True
    example: chisq0=tirific_chisq(mcpars['p_start'],data=data,imsets=imsets,disks=disks,mcpars=mcpars,verbose=False)
    """
    
    if  verbose==True:
        print "try ->",theta
    lp = tirific_lnprior(theta,mcpars)
    if  not np.isfinite(lp):
        blobs={'lnprob':-np.inf,'chisq':+np.inf,'ndata':0.0,'npar':len(theta)}
        if  verbose==True:
            print "chisq ->",+np.inf
        return +np.inf

    lnl,blobs=tirific_lnlike(theta,data,imsets,disks,mcpars,usesp=False)
    chisq=blobs['chisq']
    if  verbose==True:
        print "chisq ->",chisq
    
    return chisq

def tirific_chisq_d(theta,data,imsets,disks,mcpars):
    """
    pass through a validation
    +++ this is the function for SCIPY.OPTIMIZE 
    """
    verbose=False
    
    if  verbose==True:
        print "try ->",theta
    lp = tirific_lnprior(theta,mcpars)
    if  not np.isfinite(lp):
        blobs={'lnprob':-np.inf,'chisq':+np.inf,'ndata':0.0,'npar':len(theta)}
        if  verbose==True:
            print "chisq ->",+np.inf
        return +np.inf

    lnl,blobs=tirific_lnlike(theta,data,imsets,disks,mcpars)
    chisq=blobs['chisq']
    if  verbose==True:
        print "chisq ->",chisq
    
    return chisq

def getdisk(disks,object,line):
    
    for disk in disks:
        if  disk['object']==object and disk['line']==line:
            return disk


def py_tirific_pprint(p_keys,p_value,p_start,p_lo,p_up,p_format):
    
    for index in range(len(p_keys)):
        print(("{0:<3} {1:15} p = {2:"+p_format[index]+"} "+" {3:"+p_format[index]+"} "+\
                             " {4:"+p_format[index]+"} "+" {5:"+p_format[index]+"}"\
                             ).format(index,p_keys[index],p_value[index],p_start[index],p_lo[index],p_up[index]))
    
def py_tirific_mc_pformat(mcpars):
    """
    set up p_format / p_format_keys
    """
    p_format=[]
    p_format_keys=[]
    print "+"*90
    print 'varying parameters:'
    for ind in range(len(mcpars['p_keys'])):
        
        p_key=mcpars['p_keys'][ind]
        smin=len(p_key)
        print("{0:<3} {1}".format(ind,p_key))

        p_format0='<'+str(max(smin,5))
        p_format0_keys='<'+str(max(smin,5))
        #   VELOCITY
        if  fnmatch.fnmatch(p_key,'v*'):
            p_format0='<'+str(max(smin,5))+'.0f'
            p_format0_keys='<'+str(max(smin,5))
        #   SURFACE BRIGHTNESS
        if  fnmatch.fnmatch(p_key,'es*'):
            p_format0='<'+str(max(smin,5))+'.4f'
            p_format0_keys='<'+str(max(smin,5))
        #   INC OR PA
        if  fnmatch.fnmatch(p_key,'in*') or fnmatch.fnmatch(p_key,'pa*'):
            p_format0='<'+str(max(smin,3))+'.0f'
            p_format0_keys='<'+str(max(smin,3))         
        #   ERRR SCALING
        if  fnmatch.fnmatch(p_key,'lnf*'):
            p_format0='<'+str(max(smin,4))+'.4f'
            p_format0_keys='<'+str(max(smin,4))
        
        p_format+=[p_format0]
        p_format_keys+=[p_format0_keys]
    print "+"*90
    
    mcpars['p_format']=deepcopy(p_format)
    mcpars['p_format_keys']=deepcopy(p_format_keys)
    
    return  mcpars

