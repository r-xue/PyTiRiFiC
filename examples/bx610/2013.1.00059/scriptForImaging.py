# Imaging script for 2013.1.00059.S, BX610_a_04_TE

########################################
# Check CASA version

import re

if (re.search('^4.2', casadef.casa_version) or re.search('^4.3', casadef.casa_version) or re.search('^4.4', casadef.casa_version))  == None:
 sys.exit('ERROR: PLEASE USE THE SAME VERSION OF CASA THAT YOU USED FOR GENERATING THE SCRIPT: 4.2, 4.3, or 4.4')

########################################
# Getting a list of ms files to image

import glob

vislist=glob.glob('*.ms.split.cal')

########################################
# Removing pointing table

# This step removes the pointing table from the data to avoid
# a bug with mosaics in CASA 4.2.2.

if casadef.casa_version < '4.5.0':
    for vis in vislist:
        tb.open( vis + '/POINTING',
                 nomodify = False)
        a = tb.rownumbers()
        tb.removerows(a)
        tb.close()

###############################################################
# Combining Measurement Sets from Multiple Executions 

concatvis='calibrated.ms'

rmtables(concatvis)
os.system('rm -rf ' + concatvis + '.flagversions')
concat(vis=vislist,
       concatvis=concatvis)

###################################
# Splitting off science target data

vishead(vis=concatvis)

#2015-11-25 20:50:00 INFO ms	   Observer: maravena     Project: uid://A001/X10b/X76  
#2015-11-25 20:50:00 INFO ms	Observation: ALMA(44 antennas)
#2015-11-25 20:50:00 INFO ms	   
#2015-11-25 20:50:00 INFO ms	  Telescope Observation Date    Observer       Project        
#2015-11-25 20:50:00 INFO ms	  ALMA      [                   4.94228e+09, 4.94229e+09]maravena       uid://A001/X10b/X76
#2015-11-25 20:50:00 INFO ms	  ALMA      [                   4.94246e+09, 4.94246e+09]maravena       uid://A001/X10b/X76
#2015-11-25 20:50:01 INFO ms	Data records: 4548540       Total elapsed time = 176725 seconds
#2015-11-25 20:50:01 INFO ms	   Observed from   29-Jun-2015/08:50:17.1   to   01-Jul-2015/09:55:42.5 (UTC)
#2015-11-25 20:50:05 INFO ms	   
#2015-11-25 20:50:06 INFO ms	Fields: 6
#2015-11-25 20:50:06 INFO ms	  ID   Code Name                RA               Decl           Epoch   SrcId      nRows
#2015-11-25 20:50:06 INFO ms	  0    none J2232+1143          22:32:36.408900 +11.43.50.90410 J2000   0         369800
#2015-11-25 20:50:06 INFO ms	  2    none Ceres               20:47:57.483134 -27.30.06.64236 J2000   2          90300
#2015-11-25 20:50:06 INFO ms	  3    none J0010+1058          00:10:31.005910 +10.58.29.50430 J2000   3         369800
#2015-11-25 20:50:06 INFO ms	  4    none J0019+2021          00:19:37.854500 +20.21.45.64460 J2000   4         184900
#2015-11-25 20:50:06 INFO ms	  5    none BX610               23:46:09.430000 +12.49.19.21000 J2000   5        3439140
#2015-11-25 20:50:06 INFO ms	  6    none Ceres               20:46:48.135925 -27.43.07.64508 J2000   8          94600
#2015-11-25 20:50:07 INFO ms	Spectral Windows:  (4 unique spectral windows and 1 unique polarization setups)
#2015-11-25 20:50:07 INFO ms	  SpwID  Name                           #Chans   Frame   Ch0(MHz)  ChanWid(kHz)  TotBW(kHz) CtrFreq(MHz) BBC Num  Corrs  
#2015-11-25 20:50:07 INFO ms	  0      ALMA_RB_04#BB_1#SW-01#FULL_RES    480   TOPO  152373.278      3906.250   1875000.0 153308.8250        1  XX  YY
#2015-11-25 20:50:07 INFO ms	  1      ALMA_RB_04#BB_2#SW-01#FULL_RES    480   TOPO  154248.278      3906.250   1875000.0 155183.8250        2  XX  YY
#2015-11-25 20:50:07 INFO ms	  2      ALMA_RB_04#BB_3#SW-01#FULL_RES    480   TOPO  144202.372     -3906.250   1875000.0 143266.8250        3  XX  YY
#2015-11-25 20:50:07 INFO ms	  3      ALMA_RB_04#BB_4#SW-01#FULL_RES    480   TOPO  142369.372     -3906.250   1875000.0 141433.8250        4  XX  YY
#2015-11-25 20:50:07 INFO ms	Antennas: 44 'name'='station' 
#2015-11-25 20:50:07 INFO ms	   ID=   0-3: 'DA41'='A137', 'DA42'='A082', 'DA43'='A079', 'DA44'='A104', 
#2015-11-25 20:50:07 INFO ms	   ID=   4-7: 'DA45'='A135', 'DA46'='A058', 'DA47'='A101', 'DA49'='A029', 
#2015-11-25 20:50:07 INFO ms	   ID=  8-11: 'DA51'='A085', 'DA52'='A105', 'DA53'='A069', 'DA54'='A090', 
#2015-11-25 20:50:07 INFO ms	   ID= 12-15: 'DA55'='A060', 'DA57'='A113', 'DA58'='A091', 'DA59'='A021', 
#2015-11-25 20:50:07 INFO ms	   ID= 16-19: 'DA60'='A089', 'DA61'='A075', 'DA62'='A097', 'DA63'='A073', 
#2015-11-25 20:50:07 INFO ms	   ID= 20-23: 'DA64'='A107', 'DV01'='A072', 'DV02'='A094', 'DV03'='A103', 
#2015-11-25 20:50:07 INFO ms	   ID= 24-27: 'DV04'='A011', 'DV05'='A084', 'DV07'='A112', 'DV10'='A096', 
#2015-11-25 20:50:07 INFO ms	   ID= 28-31: 'DV11'='A115', 'DV12'='A092', 'DV13'='A076', 'DV14'='A086', 
#2015-11-25 20:50:07 INFO ms	   ID= 32-35: 'DV15'='A078', 'DV16'='A077', 'DV17'='A136', 'DV18'='A015', 
#2015-11-25 20:50:07 INFO ms	   ID= 36-39: 'DV19'='A033', 'DV20'='A088', 'DV22'='A110', 'DV23'='A087', 
#2015-11-25 20:50:07 INFO ms	   ID= 40-43: 'DV24'='A080', 'DV25'='A083', 'DA50'='A064', 'DV21'='A093'

sourcevis='calibrated_source.ms'
rmtables(sourcevis)
os.system('rm -rf ' + sourcevis + '.flagversions')
split(vis=concatvis,
      intent='*TARGET*', # split off the target sources
      outputvis=sourcevis,
      datacolumn='data')

# Check that split worked as desired.
vishead(vis=sourcevis) 

############################################
# Rename and backup data set

os.system('mv -i ' + sourcevis + ' ' + 'calibrated_final.ms')

# At this point you should create a backup of your final data set in
# case the ms you are working with gets corrupted by clean. 

os.system('cp -ir calibrated_final.ms calibrated_final.ms.backup')

##################################################
# Create an Averaged Continuum MS

finalvis='calibrated_final.ms' # This is your output ms from the data
                               # preparation script.

# Use plotms to identify line and continuum spectral windows.
plotms(vis=finalvis, xaxis='channel', yaxis='amplitude',
       ydatacolumn='data',
       avgtime='1e8', avgscan=True, avgchannel='1', 
       iteraxis='spw' )

# Set spws to be used to form continuum
contspws = '0,1,2,3'

# If you have complex line emission and no dedicated continuum
# windows, you will need to flag the line channels prior to averaging.
flagmanager(vis=finalvis,mode='save',
            versionname='before_cont_flags')

# Flag the "line channels"; spw 1 has increased noise at the edge of the window (as does the bandpass), spw 3 has the atmospheric line. both will be excluded from the continuum image.
flagchannels='1:400~479,3:30~80' 

flagdata(vis=finalvis,mode='manual',
          spw=flagchannels,flagbackup=False)

# check that flags are as expected, NOTE must check reload on plotms
# gui if its still open.
plotms(vis=finalvis,yaxis='amp',xaxis='channel',
       avgchannel='1',avgtime='1e8',avgscan=True,iteraxis='spw') 

# Average the channels within spws
contvis='calibrated_final_cont.ms'
rmtables(contvis)
os.system('rm -rf ' + contvis + '.flagversions')

split(vis=finalvis,
      spw=contspws,      
      outputvis=contvis,
      width=[480,480,480,480], # number of channels to average together. change to appropriate value for each spectral window in contspws (use listobs or vishead to find) and make sure to use the native number of channels per SPW (that is, not the number of channels left after flagging any lines)
      datacolumn='data')

# Note: There is a bug in split that does not average the data
# properly if the width is set to a value larger than the number of
# channels in an SPW. Specifying the width of each spw (as done above)
# is necessary for producing properly weighted data.

# If you flagged any line channels, restore the previous flags
flagmanager(vis=finalvis,mode='restore',
            versionname='before_cont_flags')

# Inspect continuum for any problems
plotms(vis=contvis,xaxis='uvdist',yaxis='amp',coloraxis='spw')

# #############################################
# Image Parameters

# source parameters
# ------------------

field='5' # science field(s). For a mosaic, select all mosaic fields. DO NOT LEAVE BLANK ('') OR YOU WILL TRIGGER A BUG IN CLEAN THAT WILL PUT THE WRONG COORDINATE SYSTEM ON YOUR FINAL IMAGE.
imagermode='csclean' # uncomment if single field
# phasecenter=3 # uncomment and set to field number for phase
                # center. Note lack of ''.  Use the weblog to
                # determine which pointing to use. Remember that the
                # field ids for each pointing will be re-numbered
                # after your initial split. You can also specify the
                # phase center using coordinates, e.g.,
                # phasecenter='J2000 19h30m00 -40d00m00'

# image parameters.
# ----------------

cell='0.04arcsec' # cell size for imaging.
imsize = [1000,1000] # size of image in pixels.

# velocity parameters
# -------------------

outframe='topo' # velocity reference frame. See science goals.
veltype='radio' # velocity type. See note below.

# imaging control
# ----------------

# The cleaning below is done interactively, so niter and threshold can
# be controlled within clean. 

weighting = 'briggs'
robust=0.5
niter=1000
threshold = '0.0mJy'

#############################################
# Imaging the Continuuum

# Set the ms and continuum image name.
contvis = 'calibrated_final_cont.ms'         
contimagename = 'calibrated_final_cont'

# If necessary, run the following commands to get rid of older clean
# data.

#clearcal(vis=contvis)
#delmod(vis=contvis)

for ext in ['.flux','.image','.mask','.model','.pbcor','.psf','.residual','.flux.pbcoverage']:
    rmtables(contimagename+ext)

clean(vis=contvis,
      imagename=contimagename,
      field=field,
#      phasecenter=phasecenter, # uncomment if mosaic.      
      mode='mfs',
      psfmode='clark',
      imsize = imsize, 
      cell= cell, 
      weighting = weighting, 
      robust = robust,
      niter = niter, 
      threshold = threshold, 
      interactive = True,
      imagermode = imagermode)

# rms in continuum image: 12 uJy in a 0.35"x0.30" beam, PA=26.66deg 

# If you'd like to redo your clean, but don't want to make a new mask
# use the following commands to save your original mask. This is an optional step.
#contmaskname = 'cont.mask'
##rmtables(contmaskname) # if you want to delete the old mask
#os.system('cp -ir ' + contimagename + '.mask ' + contmaskname)

########################################
# Continuum Subtraction for Line Imaging

fitspw = '0,1:0~400,2,3:0~30;80~479' # line-free channel for fitting continuum
linespw = '0,2' # line spectral windows. You can subtract the continuum from multiple spectral line windows at once.

finalvis='calibrated_final.ms'

uvcontsub(vis=finalvis,
          spw=linespw, # spw to do continuum subtraction on
          fitspw=fitspw, # select spws to fit continuum. exclude regions with strong lines.
          combine='spw', 
          solint='int',
          fitorder=1,
          want_cont=False) # This value should not be changed.

# NOTE: Imaging the continuum produced by uvcontsub with
# want_cont=True will lead to extremely poor continuum images because
# of bandwidth smearing effects. For imaging the continuum, you should
# always create a line-free continuum data set using the process
# outlined above.

linevis = finalvis+'.contsub'

##############################################
# Image line emission [REPEAT AS NECESSARY]

finalvis = 'calibrated_final.ms'
# linevis = finalvis # uncomment if you neither continuum subtracted nor self-calibrated your data.
linevis = finalvis + '.contsub' # uncomment if continuum subtracted

sourcename ='BX610' # name of source
linename = 'CI' # name of transition (see science goals in OT for name) 
lineimagename = sourcename+'_'+linename # name of line image

restfreq='153.307GHz' # Typically the rest frequency of the line of
                        # interest. If the source has a significant
                        # redshift (z>0.2), use the observed sky
                        # frequency (nu_rest/(1+z)) instead of the
                        # rest frequency of the
                        # line.

spw='0' # uncomment and replace with appropriate spw if necessary.

start='' # start velocity. See science goals for appropriate value.
width='50km/s' # velocity width. See science goals.
nchan = 80  # number of channels. See science goals for appropriate value.

# If necessary, run the following commands to get rid of older clean
# data.

#clearcal(vis=linevis)
#delmod(vis=linevis)

for ext in ['.flux','.image','.mask','.model','.pbcor','.psf','.residual','.flux.pbcoverage']:
    rmtables(lineimagename + ext)

clean(vis=linevis,
      imagename=lineimagename, 
      field=field,
      spw=spw,
#      phasecenter=phasecenter, # uncomment if mosaic.      
      mode='velocity',
      start=start,
      width=width,
      nchan=nchan, 
      outframe=outframe, 
      veltype=veltype, 
      restfreq=restfreq, 
      niter=niter,  
      threshold=threshold, 
      interactive=True,
      cell=cell,
      imsize=imsize, 
      weighting=weighting, 
      robust=robust,
      imagermode=imagermode)

# CI detection in 5,55,105 km/s channels; boxes drawn, ~150 iterations of clean per channel (entire spw is imaged in cube)
# rms in one 50 km/s channel: 0.19 mJy/beam in a 0.34"x0.30" beam, PA=27.32deg

# If you'd like to redo your clean, but don't want to make a new mask
# use the following commands to save your original mask. This is an
# optional step.
# linemaskname = 'line.mask'
## rmtables(linemaskname) # uncomment if you want to overwrite the mask.
# os.system('cp -ir ' + lineimagename + '.mask ' + linemaskname)

##############################################
# Image line emission [REPEAT AS NECESSARY]

finalvis = 'calibrated_final.ms'
# linevis = finalvis # uncomment if you neither continuum subtracted nor self-calibrated your data.
linevis = finalvis + '.contsub' # uncomment if continuum subtracted

sourcename ='BX610' # name of source
linename = 'CO_43' # name of transition (see science goals in OT for name)
lineimagename = sourcename+'_'+linename # name of line image

restfreq='143.613GHz' # Typically the rest frequency of the line of
                        # interest. If the source has a significant
                        # redshift (z>0.2), use the observed sky
                        # frequency (nu_rest/(1+z)) instead of the
                        # rest frequency of the
                        # line.

spw='1' # uncomment and replace with appropriate spw if necessary.

start='' # start velocity. See science goals for appropriate value.
width='50km/s' # velocity width. See science goals.
nchan = 80  # number of channels. See science goals for appropriate value.

# If necessary, run the following commands to get rid of older clean
# data.

clearcal(vis=linevis)
delmod(vis=linevis)

for ext in ['.flux','.image','.mask','.model','.pbcor','.psf','.residual','.flux.pbcoverage']:
    rmtables(lineimagename + ext)

clean(vis=linevis,
      imagename=lineimagename,
      field=field,
      spw=spw,
#      phasecenter=phasecenter, # uncomment if mosaic.
      mode='velocity',
      start=start,
      width=width,
      nchan=nchan,
      outframe=outframe,
      veltype=veltype,
      restfreq=restfreq,
      niter=niter,
      threshold=threshold,
      interactive=True,
      cell=cell,
      imsize=imsize,
      weighting=weighting,
      robust=robust,
      imagermode=imagermode)

# CO 4-3 detection in 8 channels (-145 to 205 km/s); boxes drawn, ~130 iterations of clean per channel (entire spw is imaged in cube)
# rms in one 50 km/s channel: 0.18 mJy/beam in a 0.38"x0.32" beam, PA=33.10deg

# If you'd like to redo your clean, but don't want to make a new mask
# use the following commands to save your original mask. This is an
# optional step.
# linemaskname = 'line.mask'
## rmtables(linemaskname) # uncomment if you want to overwrite the mask.
# os.system('cp -ir ' + lineimagename + '.mask ' + linemaskname)

##############################################
# Apply a primary beam correction

import glob

myimages = glob.glob("*.image")

rmtables('*.pbcor')
for image in myimages:
    pbimage = image.rsplit('.',1)[0]+'.flux'
    outfile = image.rsplit('.',1)[0]+'.pbcor'
    impbcor(imagename=image, pbimage=pbimage, outfile = outfile)

##############################################
# Export the images

import glob

myimages = glob.glob("*.pbcor")
for image in myimages:
    exportfits(imagename=image, fitsimage=image+'.fits',overwrite=True)

myimages = glob.glob("*.flux")
for image in myimages:
    exportfits(imagename=image, fitsimage=image+'.fits',overwrite=True) 

##############################################
# Analysis

# For examples of how to get started analyzing your data, see 
#     http://casaguides.nrao.edu/index.php?title=TWHydraBand7_Imaging_4.2
