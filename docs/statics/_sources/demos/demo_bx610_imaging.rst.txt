Example: BX610 (High-z SFG) : Data Imaging
------------------------------------------

Prepare visibiity data from the calibrated MS restored by the local ALMA pipeline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Load some essential Python modules + CASA 6 tasks/tools
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: ipython3

    
    import sys,os,glob,io,socket
    import logging
    from pprint import pprint
    import numpy as np
    
    import casatasks as ctasks
    import casatools as ctools
    
    # Import wurlitzer for display real-time console logs
    #   https://github.com/minrk/wurlitzer
    %reload_ext wurlitzer
    
    # for inline plots
    %matplotlib inline
    %config InlineBackend.figure_format = "retina"


Using the beta-version of CASA 6

.. code:: ipython3

    print('casatools ver:',ctools.version_string())
    print('casatasks ver:',ctasks.version_string())


.. parsed-literal::

    casatools ver: 2019.172
    casatasks ver: 2019.166


Import some convinient functions from ``rxutils``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: ipython3

    from rxutils.casa.imager import invert        # generate a small dirty image (invert) from a MS dataset as invert
    from rxutils.casa.proc import setLogfile        # help reset the casa 6 log file

2013.1.00059.S
^^^^^^^^^^^^^^

.. code:: ipython3

    demo_dir='/Users/Rui/Documents/Workspace/projects/GMaKE/examples/data/bx610/alma/2013.1.00059.S/'
    if  'hypersion' or 'mini' in socket.gethostname() :
        os.chdir(demo_dir)
    setLogfile(demo_dir+'/'+'demo_bx610_imaging.log')
    
    invert('bb1.ms','bb1.ci10/sci',cell=0.05,imsize=[64,64],datacolumn='data')
    invert('bb3.ms','bb3.co43/sci',cell=0.05,imsize=[64,64],datacolumn='data')
    invert(['bb2.ms.mfs','bb4.ms.mfs'],'bb24.cont/sci',cell=0.05,imsize=[64,64],datacolumn='data',specmode='mfs')


::


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-1-ed018757ed81> in <module>
          2 if  'hypersion' or 'mini' in socket.gethostname() :
          3     os.chdir(demo_dir)
    ----> 4 setLogfile(demo_dir+'/'+'demo_bx610_imaging.log')
          5 
          6 invert('bb1.ms','bb1.ci10/sci',cell=0.05,imsize=[64,64],datacolumn='data')


    NameError: name 'setLogfile' is not defined


2017.1.01045.S
^^^^^^^^^^^^^^

.. code:: ipython3

    demo_dir='/Users/Rui/Documents/Workspace/projects/GMaKE/examples/data/bx610/alma/2017.1.01045.S/'
    if  'hypersion' or 'mini' in socket.gethostname() :
        os.chdir(demo_dir)
    setLogfile(demo_dir+'/'+'demo_bx610_imaging.log')
    
    invert('bb1.ms','bb1.co43/sci',cell=0.01,imsize=[256,256],datacolumn='data')
    invert('bb3.ms','bb3.ci10/sci',cell=0.01,imsize=[256,256],datacolumn='data')
    invert(['bb2.ms.mfs','bb4.ms.mfs'],'bb24.cont/sci',cell=0.01,imsize=[256,256],datacolumn='data',specmode='mfs')


.. parsed-literal::

    2019-11-22 02:39:06	INFO	tclean::::casa	##########################################
    2019-11-22 02:39:06	INFO	tclean::::casa	##### Begin Task: tclean             #####
    2019-11-22 02:39:06	INFO	tclean::::casa	tclean( vis='bb1.ms', selectdata=True, field='', spw='', timerange='', uvrange='', antenna='', scan='', observation='', intent='', datacolumn='data', imagename='bb1.co43/sci', imsize=[256, 256], cell=0.01, phasecenter='', stokes='I', projection='SIN', startmodel='', specmode='cube', reffreq='', nchan=-1, start=0, width=1, outframe='LSRK', veltype='radio', restfreq=[], interpolation='nearest', perchanweightdensity=True, gridder='standard', facets=1, psfphasecenter='', chanchunks=1, wprojplanes=1, vptable='', mosweight=True, aterm=True, psterm=False, wbawp=True, conjbeams=False, cfcache='', usepointing=False, computepastep=360.0, rotatepastep=360.0, pointingoffsetsigdev=0.0, pblimit=0.2, normtype='flatnoise', deconvolver='hogbom', scales=[], nterms=2, smallscalebias=0.0, restoration=True, restoringbeam='', pbcor=False, outlierfile='', weighting='briggs', robust=1.0, noise='1.0Jy', npixels=0, uvtaper=[''], niter=0, gain=0.1, threshold=0.0, nsigma=0.0, cycleniter=-1, cyclefactor=1.0, minpsffraction=0.05, maxpsffraction=0.8, interactive=False, usemask='user', mask='', pbmask=0.0, sidelobethreshold=3.0, noisethreshold=5.0, lownoisethreshold=1.5, negativethreshold=0.0, smoothfactor=1.0, minbeamfrac=0.3, cutthreshold=0.01, growiterations=75, dogrowprune=True, minpercentchange=-1.0, verbose=False, fastnoise=True, restart=True, savemodel='none', calcres=True, calcpsf=True, parallel=False )
    2019-11-22 02:39:06	INFO	tclean::::casa	Verifying Input Parameters
    2019-11-22 02:39:06	INFO	SynthesisImagerVi2::selectData 	MS : bb1.ms | [Opened in readonly mode]
    2019-11-22 02:39:06	INFO	SynthesisImagerVi2::selectData 	  NRows selected : 275794
    2019-11-22 02:39:06	INFO	SynthesisImagerVi2::defineImage 	Define image coordinates for [bb1.co43/sci] : 
    2019-11-22 02:39:06	INFO	MSTransformRegridder::calcChanFreqs	 phaseCenter='Direction: [0.973286, -0.0588582, 0.221923]'  *** Encountered negative channel widths in input spectral window.
    2019-11-22 02:39:06	INFO	MSTransformRegridder::calcChanFreqs	 Channels equidistant in freq
    2019-11-22 02:39:06	INFO	MSTransformRegridder::calcChanFreqs+	 Central frequency (in output frame) = 1.43567e+11 Hz
    2019-11-22 02:39:06	INFO	MSTransformRegridder::calcChanFreqs+	 Channel central frequency is decreasing with increasing channel number.
    2019-11-22 02:39:06	INFO	MSTransformRegridder::calcChanFreqs+	 Width of central channel (in output frame) = 3.90647e+06 Hz
    2019-11-22 02:39:06	INFO	MSTransformRegridder::calcChanFreqs+	 Number of channels = 477
    2019-11-22 02:39:06	INFO	MSTransformRegridder::calcChanFreqs+	 Total width of SPW (in output frame) = 1.86339e+09 Hz
    2019-11-22 02:39:06	INFO	MSTransformRegridder::calcChanFreqs+	 Lower edge = 1.42635e+11 Hz, upper edge = 1.44498e+11 Hz
    2019-11-22 02:39:06	INFO	SynthesisImagerVi2::defineImage 	Impars : start 0
    2019-11-22 02:39:06	INFO	SynthesisImagerVi2::defineImage 	Shape : [256, 256, 1, 477]Spectral : [1.44496e+11] at [0] with increment [-3.90647e+06]
    2019-11-22 02:39:06	INFO	SynthesisImagerVi2::defineImage 	Set Gridding options for [bb1.co43/sci] with ftmachine : gridft
    2019-11-22 02:39:06	INFO	SynthesisImagerVi2::weight() 	Set imaging weights : Briggs weighting: sidelobes will be suppressed over full image
    2019-11-22 02:39:06	INFO	SynthesisImagerVi2::weight() 	Doing spectral cube Briggs weighting formula --  norm
    2019-11-22 02:39:06	INFO	SynthesisImager::tuneSelectData 	Tuning frequency data selection to match image spectral coordinates
    2019-11-22 02:39:06	INFO	SynthesisImagerVi2::selectData 	MS : bb1.ms | [Opened in readonly mode]
    2019-11-22 02:39:06	INFO	SynthesisImagerVi2::selectData 	  NRows selected : 275794
    2019-11-22 02:39:06	INFO	task_tclean::SynthesisDeconvolver::setupDeconvolution 	Set Deconvolution Options for [bb1.co43/sci] : hogbom
    2019-11-22 02:39:06	INFO	SynthesisImager::makePSF 	----------------------------------------------------------- Make PSF ---------------------------------------------
    
    0%....10....20....30....40....50....60....70....80....90....100%
    2019-11-22 02:42:20	INFO	SIImageStore::calcSensitivity 	[bb1.co43/sci] Theoretical sensitivity (Jy/bm):c0:5.3686e-05 c1:5.36859e-05 c2:5.36859e-05 c3:5.36859e-05 c4:5.3686e-05 c5:5.3686e-05 c6:5.3686e-05 c7:5.3686e-05 c8:5.3686e-05 c9:5.36861e-05 c10:5.3686e-05 c11:5.3686e-05 c12:5.36861e-05 c13:5.36861e-05 c14:5.36861e-05 c15:5.36861e-05 c16:5.36862e-05 c17:5.36862e-05 c18:5.36864e-05 c19:5.36862e-05 c20:5.36862e-05 c21:5.36862e-05 c22:5.36862e-05 c23:5.36862e-05 c24:5.3686e-05 c25:5.3686e-05 c26:5.3686e-05 c27:5.3686e-05 c28:5.36861e-05 c29:5.36861e-05 c30:5.36862e-05 c31:5.36861e-05 c32:5.36862e-05 c33:5.3686e-05 c34:5.3686e-05 c35:5.3686e-05 c36:5.36861e-05 c37:5.36861e-05 c38:5.36862e-05 c39:5.36861e-05 c40:5.36861e-05 c41:5.36862e-05 c42:5.36861e-05 c43:5.36863e-05 c44:5.36862e-05 c45:5.3686e-05 c46:5.3686e-05 c47:5.3686e-05 c48:5.36861e-05 c49:5.3686e-05 c50:5.36861e-05 c51:5.3686e-05 c52:5.3686e-05 c53:5.3686e-05 c54:5.36859e-05 c55:5.36857e-05 c56:5.36856e-05 c57:5.36856e-05 c58:5.36856e-05 c59:5.36856e-05 c60:5.36854e-05 c61:5.36854e-05 c62:5.36854e-05 c63:5.36855e-05 c64:5.36855e-05 c65:5.36857e-05 c66:5.36857e-05 c67:5.36857e-05 c68:5.36857e-05 c69:5.36857e-05 c70:5.36857e-05 c71:5.36857e-05 c72:5.36857e-05 c73:5.36856e-05 c74:5.36857e-05 c75:5.36857e-05 c76:5.36854e-05 c77:5.36854e-05 c78:5.36853e-05 c79:5.36853e-05 c80:5.36853e-05 c81:5.36852e-05 c82:5.36853e-05 c83:5.36853e-05 c84:5.36853e-05 c85:5.36852e-05 c86:5.36852e-05 c87:5.36853e-05 c88:5.36851e-05 c89:5.36851e-05 c90:5.3685e-05 c91:5.36848e-05 c92:5.36849e-05 c93:5.36848e-05 c94:5.36848e-05 c95:5.36849e-05 c96:5.36848e-05 c97:5.36849e-05 c98:5.36849e-05 c99:5.36849e-05 c100:5.36848e-05 c101:5.36848e-05 c102:5.36847e-05 c103:5.36848e-05 c104:5.36848e-05 c105:5.36848e-05 c106:5.36848e-05 c107:5.36848e-05 c108:5.36849e-05 c109:5.36848e-05 c110:5.36849e-05 c111:5.36849e-05 c112:5.36849e-05 c113:5.3685e-05 c114:5.36849e-05 c115:5.36849e-05 c116:5.36848e-05 c117:5.36849e-05 c118:5.36846e-05 c119:5.36846e-05 c120:5.36846e-05 c121:5.36845e-05 c122:5.36845e-05 c123:5.36845e-05 c124:5.36845e-05 c125:5.36845e-05 c126:5.36845e-05 c127:5.36845e-05 c128:5.36847e-05 c129:5.36848e-05 c130:5.36848e-05 c131:5.36848e-05 c132:5.36848e-05 c133:5.36847e-05 c134:5.36846e-05 c135:5.36847e-05 c136:5.36847e-05 c137:5.36847e-05 c138:5.36845e-05 c139:5.36846e-05 c140:5.36846e-05 c141:5.36846e-05 c142:5.36846e-05 c143:5.36845e-05 c144:5.36843e-05 c145:5.36844e-05 c146:5.36844e-05 c147:5.36845e-05 c148:5.36845e-05 c149:5.36846e-05 c150:5.36846e-05 c151:5.36846e-05 c152:5.36845e-05 c153:5.36846e-05 c154:5.36845e-05 c155:5.36845e-05 c156:5.36845e-05 c157:5.36844e-05 c158:5.36844e-05 c159:5.36843e-05 c160:5.36843e-05 c161:5.36843e-05 c162:5.36843e-05 c163:5.36844e-05 c164:5.36844e-05 c165:5.36844e-05 c166:5.36844e-05 c167:5.36844e-05 c168:5.36845e-05 c169:5.36845e-05 c170:5.36844e-05 c171:5.36844e-05 c172:5.36844e-05 c173:5.36844e-05 c174:5.36843e-05 c175:5.36843e-05 c176:5.36843e-05 c177:5.36842e-05 c178:5.36841e-05 c179:5.36839e-05 c180:5.36839e-05 c181:5.36839e-05 c182:5.36839e-05 c183:5.36839e-05 c184:5.36839e-05 c185:5.36839e-05 c186:5.36838e-05 c187:5.36838e-05 c188:5.36838e-05 c189:5.36839e-05 c190:5.36839e-05 c191:5.36837e-05 c192:5.36837e-05 c193:5.36838e-05 c194:5.36838e-05 c195:5.36837e-05 c196:5.36836e-05 c197:5.36836e-05 c198:5.36835e-05 c199:5.36835e-05 c200:5.36835e-05 c201:5.36833e-05 c202:5.36834e-05 c203:5.36834e-05 c204:5.36835e-05 c205:5.36835e-05 c206:5.36835e-05 c207:5.36835e-05 c208:5.36835e-05 c209:5.36834e-05 c210:5.36834e-05 c211:5.36834e-05 c212:5.36832e-05 c213:5.36833e-05 c214:5.36833e-05 c215:5.36834e-05 c216:5.36833e-05 c217:5.36832e-05 c218:5.36832e-05 c219:5.36832e-05 c220:5.36832e-05 c221:5.36832e-05 c222:5.36832e-05 c223:5.36833e-05 c224:5.36833e-05 c225:5.36832e-05 c226:5.36832e-05 c227:5.36832e-05 c228:5.36833e-05 c229:5.36833e-05 c230:5.36832e-05 c231:5.36832e-05 c232:5.36831e-05 c233:5.36831e-05 c234:5.36831e-05 c235:5.36831e-05 c236:5.36831e-05 c237:5.36832e-05 c238:5.36832e-05 c239:5.36832e-05 c240:5.36834e-05 c241:5.36833e-05 c242:5.36832e-05 c243:5.36832e-05 c244:5.36832e-05 c245:5.36833e-05 c246:5.36832e-05 c247:5.36832e-05 c248:5.36833e-05 c249:5.36833e-05 c250:5.36833e-05 c251:5.36834e-05 c252:5.36834e-05 c253:5.36834e-05 c254:5.36834e-05 c255:5.36834e-05 c256:5.36835e-05 c257:5.36835e-05 c258:5.36835e-05 c259:5.36834e-05 c260:5.36834e-05 c261:5.36834e-05 c262:5.36834e-05 c263:5.36834e-05 c264:5.36832e-05 c265:5.36832e-05 c266:5.36833e-05 c267:5.36833e-05 c268:5.36834e-05 c269:5.36834e-05 c270:5.36834e-05 c271:5.36834e-05 c272:5.36834e-05 c273:5.36832e-05 c274:5.36832e-05 c275:5.36832e-05 c276:5.36832e-05 c277:5.36832e-05 c278:5.36832e-05 c279:5.36832e-05 c280:5.3683e-05 c281:5.36831e-05 c282:5.36831e-05 c283:5.36831e-05 c284:5.36832e-05 c285:5.36832e-05 c286:5.36832e-05 c287:5.36831e-05 c288:5.36831e-05 c289:5.3683e-05 c290:5.36831e-05 c291:5.36831e-05 c292:5.3683e-05 c293:5.36831e-05 c294:5.36831e-05 c295:5.3683e-05 c296:5.3683e-05 c297:5.3683e-05 c298:5.3683e-05 c299:5.36831e-05 c300:5.36831e-05 c301:5.36831e-05 c302:5.36832e-05 c303:5.36831e-05 c304:5.36831e-05 c305:5.36829e-05 c306:5.36828e-05 c307:5.3683e-05 c308:5.3683e-05 c309:5.3683e-05 c310:5.3683e-05 c311:5.3683e-05 c312:5.3683e-05 c313:5.3683e-05 c314:5.36831e-05 c315:5.36831e-05 c316:5.36831e-05 c317:5.36831e-05 c318:5.36832e-05 c319:5.36832e-05 c320:5.3683e-05 c321:5.36829e-05 c322:5.36829e-05 c323:5.36829e-05 c324:5.36828e-05 c325:5.36827e-05 c326:5.36827e-05 c327:5.36827e-05 c328:5.36828e-05 c329:5.36827e-05 c330:5.36827e-05 c331:5.36827e-05 c332:5.36827e-05 c333:5.36827e-05 c334:5.36828e-05 c335:5.36827e-05 c336:5.36827e-05 c337:5.36828e-05 c338:5.36828e-05 c339:5.36829e-05 c340:5.36828e-05 c341:5.36829e-05 c342:5.36826e-05 c343:5.36826e-05 c344:5.36826e-05 c345:5.36825e-05 c346:5.36826e-05 c347:5.36827e-05 c348:5.36826e-05 c349:5.36827e-05 c350:5.36827e-05 c351:5.36827e-05 c352:5.36827e-05 c353:5.36827e-05 c354:5.36827e-05 c355:5.36825e-05 c356:5.36825e-05 c357:5.36824e-05 c358:5.36824e-05 c359:5.36824e-05 c360:5.36823e-05 c361:5.36824e-05 c362:5.36824e-05 c363:5.36825e-05 c364:5.36825e-05 c365:5.36824e-05 c366:5.36824e-05 c367:5.36824e-05 c368:5.36824e-05 c369:5.36824e-05 c370:5.36824e-05 c371:5.36824e-05 c372:5.36824e-05 c373:5.36822e-05 c374:5.36822e-05 c375:5.36822e-05 c376:5.36822e-05 c377:5.36822e-05 c378:5.36821e-05 c379:5.36822e-05 c380:5.36821e-05 c381:5.36821e-05 c382:5.36818e-05 c383:5.36817e-05 c384:5.36815e-05 c385:5.36814e-05 c386:5.36813e-05 c387:5.3681e-05 c388:5.3681e-05 c389:5.3681e-05 c390:5.3681e-05 c391:5.36808e-05 c392:5.36809e-05 c393:5.36808e-05 c394:5.36808e-05 c395:5.36808e-05 c396:5.36808e-05 c397:5.36807e-05 c398:5.36807e-05 c399:5.36806e-05 c400:5.36804e-05 c401:5.36805e-05 c402:5.36805e-05 c403:5.36805e-05 c404:5.36805e-05 c405:5.36805e-05 c406:5.36805e-05 c407:5.36805e-05 c408:5.36805e-05 c409:5.36804e-05 c410:5.36805e-05 c411:5.36804e-05 c412:5.36804e-05 c413:5.36804e-05 c414:5.36805e-05 c415:5.36805e-05 c416:5.36804e-05 c417:5.36805e-05 c418:5.36805e-05 c419:5.36804e-05 c420:5.36804e-05 c421:5.36804e-05 c422:5.36802e-05 c423:5.36801e-05 c424:5.36802e-05 c425:5.36801e-05 c426:5.36801e-05 c427:5.36801e-05 c428:5.36801e-05 c429:5.36801e-05 c430:5.36801e-05 c431:5.36801e-05 c432:5.368e-05 c433:5.368e-05 c434:5.36799e-05 c435:5.36799e-05 c436:5.36798e-05 c437:5.36798e-05 c438:5.36798e-05 c439:5.36798e-05 c440:5.36798e-05 c441:5.36798e-05 c442:5.36797e-05 c443:5.36796e-05 c444:5.36796e-05 c445:5.36796e-05 c446:5.36796e-05 c447:5.36796e-05 c448:5.36796e-05 c449:5.36795e-05 c450:5.36794e-05 c451:5.36794e-05 c452:5.36793e-05 c453:5.36793e-05 c454:5.36792e-05 c455:5.3679e-05 c456:5.36789e-05 c457:5.36788e-05 c458:5.36787e-05 c459:5.36784e-05 c460:5.36784e-05 c461:5.36784e-05 c462:5.36782e-05 c463:5.36781e-05 c464:5.36778e-05 c465:5.36777e-05 c466:5.36778e-05 c467:5.36778e-05 c468:5.36778e-05 c469:5.36778e-05 c470:5.36778e-05 c471:5.36778e-05 c472:5.36778e-05 c473:5.36778e-05 c474:5.36778e-05 c475:5.36777e-05 c476:5.36776e-05 
    2019-11-22 02:42:21	INFO	SIImageStore::printBeamSet 	Restoring Beams 
    2019-11-22 02:42:21	INFO	SIImageStore::printBeamSet +	Pol   Type Chan         Freq     Vel
    2019-11-22 02:42:21	INFO	SIImageStore::printBeamSet +	  I    Max  476 1.426369e+11 207038.68    0.0809 arcsec x    0.0661 arcsec pa=-30.1011 deg
    2019-11-22 02:42:21	INFO	SIImageStore::printBeamSet +	  I    Min    1 1.444925e+11 205832.04    0.0000 arcsec x    0.0000 arcsec pa=  0.0000 deg
    2019-11-22 02:42:21	INFO	SIImageStore::printBeamSet +	  I Median  238 1.435667e+11 206434.09    0.0808 arcsec x    0.0645 arcsec pa=-32.3214 deg
    2019-11-22 02:42:21	INFO	task_tclean::SynthesisImagerVi2::makePrimaryBeam 	vi2 : Evaluating Primary Beam model onto image grid(s)
    2019-11-22 02:42:25	INFO	task_tclean::SynthesisImager::executeMajorCycle 	----------------------------------------------------------- Run (Last) Major Cycle 1 -------------------------------------
    
    0%....10....20....30....40....50....60....70....80....90....100%
    2019-11-22 02:45:21	INFO	task_tclean::SDAlgorithmBase::restore 	[bb1.co43/sci] : Restoring model image.
    2019-11-22 02:45:21	WARN	task_tclean::SIImageStore::restore (file casa-source/code/synthesis/ImagerObjects/SIImageStore.cc, line 2068)	Restoring with an empty model image. Only residuals will be processed to form the output restored image.
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 0 : 0.0804214 arcsec, 0.0641638 arcsec, -32.3913 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 1 : 0.0804233 arcsec, 0.0641653 arcsec, -32.3911 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 2 : 0.0804248 arcsec, 0.0641667 arcsec, -32.3905 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 3 : 0.0804264 arcsec, 0.0641682 arcsec, -32.3899 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 4 : 0.0804279 arcsec, 0.0641695 arcsec, -32.3898 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 5 : 0.0804293 arcsec, 0.0641709 arcsec, -32.3896 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 6 : 0.0804309 arcsec, 0.0641724 arcsec, -32.3892 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 7 : 0.0804327 arcsec, 0.0641737 arcsec, -32.3889 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 8 : 0.0804343 arcsec, 0.064175 arcsec, -32.3887 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 9 : 0.080436 arcsec, 0.0641762 arcsec, -32.3885 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 10 : 0.0804376 arcsec, 0.0641777 arcsec, -32.388 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 11 : 0.0804393 arcsec, 0.0641791 arcsec, -32.3878 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 12 : 0.080441 arcsec, 0.0641804 arcsec, -32.3874 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 13 : 0.0804427 arcsec, 0.0641817 arcsec, -32.387 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 14 : 0.0804442 arcsec, 0.0641832 arcsec, -32.3868 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 15 : 0.0804457 arcsec, 0.0641844 arcsec, -32.3866 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 16 : 0.0804477 arcsec, 0.0641859 arcsec, -32.3857 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 17 : 0.080449 arcsec, 0.0641872 arcsec, -32.3859 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 18 : 0.0804506 arcsec, 0.0641897 arcsec, -32.3866 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 19 : 0.0804523 arcsec, 0.0641901 arcsec, -32.3852 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 20 : 0.0804539 arcsec, 0.0641917 arcsec, -32.3848 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 21 : 0.0804556 arcsec, 0.0641931 arcsec, -32.3846 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 22 : 0.0804572 arcsec, 0.0641944 arcsec, -32.3844 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 23 : 0.0804588 arcsec, 0.0641957 arcsec, -32.3842 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 24 : 0.0804609 arcsec, 0.0641973 arcsec, -32.384 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 25 : 0.0804624 arcsec, 0.0641987 arcsec, -32.3836 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 26 : 0.080464 arcsec, 0.0642 arcsec, -32.3835 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 27 : 0.0804656 arcsec, 0.0642012 arcsec, -32.3832 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 28 : 0.080467 arcsec, 0.0642026 arcsec, -32.3827 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 29 : 0.0804685 arcsec, 0.0642039 arcsec, -32.3823 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 30 : 0.08047 arcsec, 0.0642053 arcsec, -32.382 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 31 : 0.0804717 arcsec, 0.0642069 arcsec, -32.3815 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 32 : 0.0804733 arcsec, 0.0642083 arcsec, -32.3815 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 33 : 0.0804752 arcsec, 0.0642099 arcsec, -32.381 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 34 : 0.0804769 arcsec, 0.0642112 arcsec, -32.3805 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 35 : 0.0804783 arcsec, 0.0642125 arcsec, -32.3799 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 36 : 0.0804798 arcsec, 0.0642139 arcsec, -32.3794 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 37 : 0.0804814 arcsec, 0.0642152 arcsec, -32.3792 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 38 : 0.080483 arcsec, 0.0642173 arcsec, -32.3791 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 39 : 0.0804844 arcsec, 0.0642181 arcsec, -32.3784 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 40 : 0.0804861 arcsec, 0.0642194 arcsec, -32.378 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 41 : 0.0804876 arcsec, 0.0642208 arcsec, -32.3777 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 42 : 0.0804894 arcsec, 0.0642225 arcsec, -32.3771 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 43 : 0.0804911 arcsec, 0.0642247 arcsec, -32.3764 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 44 : 0.0804926 arcsec, 0.0642251 arcsec, -32.3764 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 45 : 0.0804946 arcsec, 0.0642268 arcsec, -32.3764 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 46 : 0.0804962 arcsec, 0.064228 arcsec, -32.376 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 47 : 0.080498 arcsec, 0.0642296 arcsec, -32.3757 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 48 : 0.0804996 arcsec, 0.0642311 arcsec, -32.3752 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 49 : 0.0805012 arcsec, 0.0642326 arcsec, -32.3746 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 50 : 0.0805028 arcsec, 0.0642341 arcsec, -32.3742 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 51 : 0.0805044 arcsec, 0.0642355 arcsec, -32.3739 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 52 : 0.0805059 arcsec, 0.064237 arcsec, -32.3734 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 53 : 0.0805074 arcsec, 0.0642384 arcsec, -32.3732 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 54 : 0.0805093 arcsec, 0.0642398 arcsec, -32.3731 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 55 : 0.0805112 arcsec, 0.0642414 arcsec, -32.3728 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 56 : 0.0805129 arcsec, 0.0642428 arcsec, -32.3726 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 57 : 0.0805145 arcsec, 0.0642442 arcsec, -32.3724 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 58 : 0.0805161 arcsec, 0.0642456 arcsec, -32.372 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 59 : 0.0805178 arcsec, 0.0642469 arcsec, -32.372 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 60 : 0.0805196 arcsec, 0.0642485 arcsec, -32.3717 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 61 : 0.0805213 arcsec, 0.0642498 arcsec, -32.3716 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 62 : 0.080523 arcsec, 0.0642512 arcsec, -32.3712 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 63 : 0.0805245 arcsec, 0.0642527 arcsec, -32.3709 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 64 : 0.0805261 arcsec, 0.0642541 arcsec, -32.3705 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 65 : 0.0805275 arcsec, 0.0642553 arcsec, -32.3704 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 66 : 0.0805292 arcsec, 0.0642567 arcsec, -32.3702 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 67 : 0.0805308 arcsec, 0.064258 arcsec, -32.37 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 68 : 0.0805325 arcsec, 0.0642595 arcsec, -32.3696 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 69 : 0.080534 arcsec, 0.0642609 arcsec, -32.3691 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 70 : 0.0805356 arcsec, 0.0642624 arcsec, -32.369 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 71 : 0.0805374 arcsec, 0.0642639 arcsec, -32.3687 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 72 : 0.0805389 arcsec, 0.0642652 arcsec, -32.3683 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 73 : 0.0805404 arcsec, 0.0642668 arcsec, -32.3677 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 74 : 0.0805421 arcsec, 0.0642681 arcsec, -32.3675 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 75 : 0.0805437 arcsec, 0.0642694 arcsec, -32.3668 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 76 : 0.0805457 arcsec, 0.0642712 arcsec, -32.3662 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 77 : 0.0805473 arcsec, 0.0642725 arcsec, -32.366 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 78 : 0.0805492 arcsec, 0.064274 arcsec, -32.3655 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 79 : 0.0805509 arcsec, 0.0642753 arcsec, -32.3653 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 80 : 0.0805526 arcsec, 0.0642767 arcsec, -32.365 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 81 : 0.0805544 arcsec, 0.0642781 arcsec, -32.3648 deg
    2019-11-22 02:45:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 82 : 0.0805559 arcsec, 0.0642795 arcsec, -32.3641 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 83 : 0.0805575 arcsec, 0.0642809 arcsec, -32.3639 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 84 : 0.0805591 arcsec, 0.0642822 arcsec, -32.3637 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 85 : 0.0805608 arcsec, 0.0642836 arcsec, -32.3635 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 86 : 0.0805624 arcsec, 0.0642851 arcsec, -32.3632 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 87 : 0.0805639 arcsec, 0.0642864 arcsec, -32.3629 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 88 : 0.0805659 arcsec, 0.0642881 arcsec, -32.3626 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 89 : 0.0805675 arcsec, 0.0642896 arcsec, -32.3623 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 90 : 0.0805694 arcsec, 0.0642911 arcsec, -32.3622 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 91 : 0.0805711 arcsec, 0.0642925 arcsec, -32.3618 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 92 : 0.0805728 arcsec, 0.0642937 arcsec, -32.3617 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 93 : 0.0805745 arcsec, 0.0642952 arcsec, -32.3615 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 94 : 0.0805762 arcsec, 0.0642967 arcsec, -32.3612 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 95 : 0.0805781 arcsec, 0.0642985 arcsec, -32.361 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 96 : 0.0805796 arcsec, 0.0642997 arcsec, -32.3607 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 97 : 0.0805811 arcsec, 0.064301 arcsec, -32.3606 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 98 : 0.0805827 arcsec, 0.0643025 arcsec, -32.3606 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 99 : 0.0805843 arcsec, 0.0643038 arcsec, -32.3605 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 100 : 0.0805863 arcsec, 0.0643055 arcsec, -32.3601 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 101 : 0.080588 arcsec, 0.0643068 arcsec, -32.3596 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 102 : 0.08059 arcsec, 0.0643084 arcsec, -32.3596 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 103 : 0.0805916 arcsec, 0.0643097 arcsec, -32.3592 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 104 : 0.0805931 arcsec, 0.0643111 arcsec, -32.3589 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 105 : 0.0805949 arcsec, 0.0643124 arcsec, -32.3587 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 106 : 0.0805965 arcsec, 0.0643138 arcsec, -32.3584 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 107 : 0.0805982 arcsec, 0.0643153 arcsec, -32.358 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 108 : 0.0805998 arcsec, 0.0643167 arcsec, -32.3575 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 109 : 0.0806014 arcsec, 0.0643182 arcsec, -32.357 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 110 : 0.0806031 arcsec, 0.0643196 arcsec, -32.3567 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 111 : 0.0806046 arcsec, 0.0643208 arcsec, -32.3567 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 112 : 0.0806062 arcsec, 0.0643221 arcsec, -32.3565 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 113 : 0.0806078 arcsec, 0.0643235 arcsec, -32.356 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 114 : 0.0806095 arcsec, 0.0643251 arcsec, -32.3555 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 115 : 0.0806112 arcsec, 0.0643265 arcsec, -32.3551 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 116 : 0.0806128 arcsec, 0.0643278 arcsec, -32.355 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 117 : 0.0806144 arcsec, 0.064329 arcsec, -32.3549 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 118 : 0.0806162 arcsec, 0.0643307 arcsec, -32.3544 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 119 : 0.0806178 arcsec, 0.0643323 arcsec, -32.3539 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 120 : 0.0806195 arcsec, 0.0643336 arcsec, -32.3538 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 121 : 0.0806211 arcsec, 0.0643349 arcsec, -32.3535 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 122 : 0.0806227 arcsec, 0.0643363 arcsec, -32.3533 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 123 : 0.0806245 arcsec, 0.0643377 arcsec, -32.353 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 124 : 0.0806261 arcsec, 0.0643391 arcsec, -32.3526 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 125 : 0.0806275 arcsec, 0.0643404 arcsec, -32.3523 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 126 : 0.0806291 arcsec, 0.0643418 arcsec, -32.3519 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 127 : 0.0806305 arcsec, 0.0643431 arcsec, -32.3515 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 128 : 0.080632 arcsec, 0.0643446 arcsec, -32.3513 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 129 : 0.0806338 arcsec, 0.064346 arcsec, -32.3509 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 130 : 0.0806353 arcsec, 0.0643475 arcsec, -32.3503 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 131 : 0.0806371 arcsec, 0.0643489 arcsec, -32.35 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 132 : 0.0806387 arcsec, 0.0643503 arcsec, -32.3497 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 133 : 0.0806404 arcsec, 0.0643517 arcsec, -32.3498 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 134 : 0.0806421 arcsec, 0.0643531 arcsec, -32.3495 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 135 : 0.0806436 arcsec, 0.0643545 arcsec, -32.3493 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 136 : 0.0806451 arcsec, 0.0643558 arcsec, -32.3492 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 137 : 0.0806468 arcsec, 0.0643573 arcsec, -32.349 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 138 : 0.0806486 arcsec, 0.0643587 arcsec, -32.3489 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 139 : 0.0806503 arcsec, 0.0643602 arcsec, -32.3486 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 140 : 0.0806519 arcsec, 0.0643614 arcsec, -32.3484 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 141 : 0.0806534 arcsec, 0.0643627 arcsec, -32.3479 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 142 : 0.080655 arcsec, 0.0643641 arcsec, -32.3479 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 143 : 0.0806567 arcsec, 0.0643655 arcsec, -32.3477 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 144 : 0.0806586 arcsec, 0.0643671 arcsec, -32.3471 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 145 : 0.0806602 arcsec, 0.0643683 arcsec, -32.3469 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 146 : 0.0806616 arcsec, 0.0643696 arcsec, -32.3465 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 147 : 0.0806631 arcsec, 0.0643711 arcsec, -32.3461 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 148 : 0.0806646 arcsec, 0.0643726 arcsec, -32.3458 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 149 : 0.0806663 arcsec, 0.0643741 arcsec, -32.3455 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 150 : 0.080668 arcsec, 0.0643754 arcsec, -32.3452 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 151 : 0.0806696 arcsec, 0.0643767 arcsec, -32.3451 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 152 : 0.0806713 arcsec, 0.0643782 arcsec, -32.3451 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 153 : 0.080673 arcsec, 0.0643795 arcsec, -32.3451 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 154 : 0.0806748 arcsec, 0.064381 arcsec, -32.3448 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 155 : 0.0806765 arcsec, 0.0643823 arcsec, -32.3444 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 156 : 0.080678 arcsec, 0.0643839 arcsec, -32.3442 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 157 : 0.0806798 arcsec, 0.0643856 arcsec, -32.3442 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 158 : 0.0806817 arcsec, 0.0643871 arcsec, -32.3439 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 159 : 0.0806834 arcsec, 0.0643885 arcsec, -32.344 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 160 : 0.080685 arcsec, 0.06439 arcsec, -32.3438 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 161 : 0.0806866 arcsec, 0.0643913 arcsec, -32.3434 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 162 : 0.0806883 arcsec, 0.0643928 arcsec, -32.3432 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 163 : 0.0806897 arcsec, 0.0643941 arcsec, -32.3429 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 164 : 0.0806911 arcsec, 0.0643953 arcsec, -32.3427 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 165 : 0.0806926 arcsec, 0.0643968 arcsec, -32.3424 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 166 : 0.0806943 arcsec, 0.0643981 arcsec, -32.3419 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 167 : 0.0806959 arcsec, 0.0643995 arcsec, -32.3416 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 168 : 0.0806974 arcsec, 0.0644007 arcsec, -32.3412 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 169 : 0.0806993 arcsec, 0.0644022 arcsec, -32.3411 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 170 : 0.080701 arcsec, 0.0644034 arcsec, -32.3408 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 171 : 0.0807026 arcsec, 0.0644048 arcsec, -32.3404 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 172 : 0.0807042 arcsec, 0.064406 arcsec, -32.3405 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 173 : 0.0807058 arcsec, 0.0644073 arcsec, -32.3399 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 174 : 0.0807076 arcsec, 0.0644089 arcsec, -32.3398 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 175 : 0.0807092 arcsec, 0.0644103 arcsec, -32.3395 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 176 : 0.0807108 arcsec, 0.0644116 arcsec, -32.3392 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 177 : 0.0807126 arcsec, 0.064413 arcsec, -32.3393 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 178 : 0.0807143 arcsec, 0.0644147 arcsec, -32.3388 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 179 : 0.0807163 arcsec, 0.0644162 arcsec, -32.3388 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 180 : 0.0807179 arcsec, 0.0644177 arcsec, -32.3384 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 181 : 0.0807195 arcsec, 0.0644191 arcsec, -32.338 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 182 : 0.0807213 arcsec, 0.0644205 arcsec, -32.3377 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 183 : 0.0807229 arcsec, 0.0644218 arcsec, -32.3375 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 184 : 0.0807245 arcsec, 0.0644231 arcsec, -32.3375 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 185 : 0.0807261 arcsec, 0.0644243 arcsec, -32.3373 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 186 : 0.0807279 arcsec, 0.0644258 arcsec, -32.3371 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 187 : 0.0807296 arcsec, 0.0644272 arcsec, -32.3368 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 188 : 0.0807313 arcsec, 0.0644288 arcsec, -32.3361 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 189 : 0.0807328 arcsec, 0.06443 arcsec, -32.3359 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 190 : 0.0807344 arcsec, 0.0644315 arcsec, -32.3358 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 191 : 0.0807361 arcsec, 0.064433 arcsec, -32.3355 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 192 : 0.0807375 arcsec, 0.0644344 arcsec, -32.3351 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 193 : 0.0807391 arcsec, 0.0644358 arcsec, -32.335 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 194 : 0.0807407 arcsec, 0.0644373 arcsec, -32.3346 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 195 : 0.0807425 arcsec, 0.0644388 arcsec, -32.3344 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 196 : 0.0807442 arcsec, 0.0644403 arcsec, -32.334 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 197 : 0.0807458 arcsec, 0.0644416 arcsec, -32.3335 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 198 : 0.0807476 arcsec, 0.0644429 arcsec, -32.3333 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 199 : 0.0807493 arcsec, 0.0644444 arcsec, -32.333 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 200 : 0.0807509 arcsec, 0.0644457 arcsec, -32.3328 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 201 : 0.0807527 arcsec, 0.0644473 arcsec, -32.3323 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 202 : 0.0807542 arcsec, 0.0644487 arcsec, -32.3318 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 203 : 0.0807557 arcsec, 0.06445 arcsec, -32.3315 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 204 : 0.0807572 arcsec, 0.0644514 arcsec, -32.3312 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 205 : 0.0807586 arcsec, 0.0644527 arcsec, -32.3307 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 206 : 0.0807602 arcsec, 0.064454 arcsec, -32.3302 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 207 : 0.0807619 arcsec, 0.0644555 arcsec, -32.3299 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 208 : 0.0807636 arcsec, 0.0644568 arcsec, -32.3298 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 209 : 0.0807657 arcsec, 0.0644584 arcsec, -32.3295 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 210 : 0.0807671 arcsec, 0.0644599 arcsec, -32.329 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 211 : 0.0807686 arcsec, 0.0644611 arcsec, -32.3288 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 212 : 0.0807705 arcsec, 0.0644627 arcsec, -32.3285 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 213 : 0.0807721 arcsec, 0.064464 arcsec, -32.3283 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 214 : 0.0807738 arcsec, 0.0644653 arcsec, -32.3284 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 215 : 0.0807753 arcsec, 0.0644665 arcsec, -32.3279 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 216 : 0.0807772 arcsec, 0.064468 arcsec, -32.3281 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 217 : 0.0807789 arcsec, 0.0644695 arcsec, -32.3279 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 218 : 0.0807806 arcsec, 0.064471 arcsec, -32.3274 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 219 : 0.0807821 arcsec, 0.0644724 arcsec, -32.327 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 220 : 0.0807837 arcsec, 0.0644737 arcsec, -32.3265 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 221 : 0.0807853 arcsec, 0.0644753 arcsec, -32.3262 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 222 : 0.0807868 arcsec, 0.0644768 arcsec, -32.326 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 223 : 0.0807884 arcsec, 0.0644782 arcsec, -32.3255 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 224 : 0.08079 arcsec, 0.0644796 arcsec, -32.3252 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 225 : 0.0807919 arcsec, 0.064481 arcsec, -32.3249 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 226 : 0.0807934 arcsec, 0.0644823 arcsec, -32.3244 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 227 : 0.0807949 arcsec, 0.0644837 arcsec, -32.3241 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 228 : 0.0807965 arcsec, 0.0644851 arcsec, -32.324 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 229 : 0.0807981 arcsec, 0.0644865 arcsec, -32.3238 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 230 : 0.0807999 arcsec, 0.0644879 arcsec, -32.3236 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 231 : 0.0808014 arcsec, 0.0644893 arcsec, -32.3234 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 232 : 0.0808033 arcsec, 0.0644908 arcsec, -32.3231 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 233 : 0.0808048 arcsec, 0.0644921 arcsec, -32.323 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 234 : 0.0808065 arcsec, 0.0644936 arcsec, -32.3227 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 235 : 0.0808078 arcsec, 0.0644949 arcsec, -32.3223 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 236 : 0.0808094 arcsec, 0.0644961 arcsec, -32.3218 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 237 : 0.0808109 arcsec, 0.0644975 arcsec, -32.3214 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 238 : 0.0808125 arcsec, 0.0644989 arcsec, -32.3214 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 239 : 0.0808141 arcsec, 0.0645002 arcsec, -32.3211 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 240 : 0.0808157 arcsec, 0.0645015 arcsec, -32.3209 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 241 : 0.0808175 arcsec, 0.064503 arcsec, -32.3209 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 242 : 0.0808192 arcsec, 0.0645045 arcsec, -32.3208 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 243 : 0.0808208 arcsec, 0.0645059 arcsec, -32.3205 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 244 : 0.0808222 arcsec, 0.0645073 arcsec, -32.32 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 245 : 0.0808239 arcsec, 0.0645085 arcsec, -32.3196 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 246 : 0.0808254 arcsec, 0.0645101 arcsec, -32.3192 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 247 : 0.0808269 arcsec, 0.0645115 arcsec, -32.3188 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 248 : 0.0808285 arcsec, 0.064513 arcsec, -32.3183 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 249 : 0.0808299 arcsec, 0.0645144 arcsec, -32.3179 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 250 : 0.0808316 arcsec, 0.0645158 arcsec, -32.3177 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 251 : 0.0808333 arcsec, 0.0645171 arcsec, -32.3175 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 252 : 0.0808349 arcsec, 0.0645184 arcsec, -32.3172 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 253 : 0.0808366 arcsec, 0.0645199 arcsec, -32.3169 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 254 : 0.080838 arcsec, 0.0645212 arcsec, -32.3165 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 255 : 0.0808398 arcsec, 0.0645226 arcsec, -32.3162 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 256 : 0.0808414 arcsec, 0.064524 arcsec, -32.3162 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 257 : 0.0808431 arcsec, 0.0645255 arcsec, -32.316 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 258 : 0.0808448 arcsec, 0.0645268 arcsec, -32.3158 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 259 : 0.0808467 arcsec, 0.0645283 arcsec, -32.3154 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 260 : 0.0808483 arcsec, 0.0645296 arcsec, -32.315 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 261 : 0.0808497 arcsec, 0.0645309 arcsec, -32.3144 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 262 : 0.0808514 arcsec, 0.0645323 arcsec, -32.3139 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 263 : 0.080853 arcsec, 0.0645335 arcsec, -32.3136 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 264 : 0.080855 arcsec, 0.0645351 arcsec, -32.3133 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 265 : 0.0808564 arcsec, 0.0645363 arcsec, -32.3128 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 266 : 0.080858 arcsec, 0.0645377 arcsec, -32.3127 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 267 : 0.0808598 arcsec, 0.0645391 arcsec, -32.3125 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 268 : 0.0808613 arcsec, 0.0645405 arcsec, -32.312 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 269 : 0.0808629 arcsec, 0.0645419 arcsec, -32.3117 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 270 : 0.0808645 arcsec, 0.0645432 arcsec, -32.3114 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 271 : 0.0808661 arcsec, 0.0645445 arcsec, -32.3113 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 272 : 0.0808676 arcsec, 0.0645458 arcsec, -32.3109 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 273 : 0.0808697 arcsec, 0.0645475 arcsec, -32.3106 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 274 : 0.0808713 arcsec, 0.0645488 arcsec, -32.3104 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 275 : 0.080873 arcsec, 0.0645501 arcsec, -32.3103 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 276 : 0.0808747 arcsec, 0.0645515 arcsec, -32.31 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 277 : 0.0808763 arcsec, 0.064553 arcsec, -32.3095 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 278 : 0.0808788 arcsec, 0.0645548 arcsec, -32.309 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 279 : 0.0808797 arcsec, 0.0645561 arcsec, -32.3087 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 280 : 0.0808814 arcsec, 0.0645575 arcsec, -32.3086 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 281 : 0.080883 arcsec, 0.0645588 arcsec, -32.3085 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 282 : 0.0808844 arcsec, 0.0645602 arcsec, -32.3081 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 283 : 0.0805841 arcsec, 0.0658151 arcsec, -30.1566 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 284 : 0.0805855 arcsec, 0.0658164 arcsec, -30.1561 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 285 : 0.0805872 arcsec, 0.0658179 arcsec, -30.1561 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 286 : 0.0805889 arcsec, 0.0658193 arcsec, -30.1558 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 287 : 0.0805906 arcsec, 0.0658209 arcsec, -30.1555 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 288 : 0.0805923 arcsec, 0.0658223 arcsec, -30.1552 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 289 : 0.0805941 arcsec, 0.0658239 arcsec, -30.1548 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 290 : 0.0805956 arcsec, 0.0658253 arcsec, -30.1542 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 291 : 0.0805972 arcsec, 0.0658266 arcsec, -30.1539 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 292 : 0.080599 arcsec, 0.0658282 arcsec, -30.1536 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 293 : 0.0806007 arcsec, 0.0658298 arcsec, -30.1533 deg
    2019-11-22 02:45:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 294 : 0.0806024 arcsec, 0.0658311 arcsec, -30.1532 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 295 : 0.0806041 arcsec, 0.0658327 arcsec, -30.1526 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 296 : 0.0806058 arcsec, 0.0658341 arcsec, -30.1528 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 297 : 0.0806076 arcsec, 0.0658357 arcsec, -30.1531 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 298 : 0.0806091 arcsec, 0.0658371 arcsec, -30.1528 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 299 : 0.0806106 arcsec, 0.0658384 arcsec, -30.1525 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 300 : 0.0806122 arcsec, 0.0658398 arcsec, -30.1522 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 301 : 0.0806138 arcsec, 0.0658415 arcsec, -30.1518 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 302 : 0.0806154 arcsec, 0.0658429 arcsec, -30.1517 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 303 : 0.0806172 arcsec, 0.0658443 arcsec, -30.1513 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 304 : 0.0806188 arcsec, 0.0658457 arcsec, -30.151 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 305 : 0.0806207 arcsec, 0.0658473 arcsec, -30.1504 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 306 : 0.0806226 arcsec, 0.0658489 arcsec, -30.1502 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 307 : 0.080624 arcsec, 0.0658502 arcsec, -30.15 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 308 : 0.0806255 arcsec, 0.0658518 arcsec, -30.1495 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 309 : 0.080627 arcsec, 0.0658532 arcsec, -30.1489 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 310 : 0.0806285 arcsec, 0.0658546 arcsec, -30.1487 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 311 : 0.08063 arcsec, 0.0658559 arcsec, -30.148 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 312 : 0.0806317 arcsec, 0.0658573 arcsec, -30.1478 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 313 : 0.0806334 arcsec, 0.0658587 arcsec, -30.1476 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 314 : 0.080635 arcsec, 0.0658602 arcsec, -30.1471 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 315 : 0.0806366 arcsec, 0.0658616 arcsec, -30.1466 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 316 : 0.0806382 arcsec, 0.065863 arcsec, -30.1463 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 317 : 0.0806398 arcsec, 0.0658645 arcsec, -30.1459 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 318 : 0.0806414 arcsec, 0.0658658 arcsec, -30.1456 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 319 : 0.080643 arcsec, 0.0658672 arcsec, -30.1454 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 320 : 0.0806448 arcsec, 0.0658689 arcsec, -30.145 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 321 : 0.0806465 arcsec, 0.0658702 arcsec, -30.1447 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 322 : 0.0806482 arcsec, 0.0658715 arcsec, -30.1445 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 323 : 0.0806499 arcsec, 0.0658729 arcsec, -30.1443 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 324 : 0.0806517 arcsec, 0.0658745 arcsec, -30.144 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 325 : 0.0806535 arcsec, 0.065876 arcsec, -30.1439 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 326 : 0.0806552 arcsec, 0.0658774 arcsec, -30.1435 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 327 : 0.0806568 arcsec, 0.065879 arcsec, -30.1429 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 328 : 0.0806584 arcsec, 0.0658803 arcsec, -30.1427 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 329 : 0.0806601 arcsec, 0.0658819 arcsec, -30.1422 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 330 : 0.0806617 arcsec, 0.0658834 arcsec, -30.1414 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 331 : 0.0806633 arcsec, 0.0658847 arcsec, -30.1414 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 332 : 0.0806647 arcsec, 0.0658862 arcsec, -30.141 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 333 : 0.0806663 arcsec, 0.0658877 arcsec, -30.1409 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 334 : 0.0806678 arcsec, 0.065889 arcsec, -30.1407 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 335 : 0.0806694 arcsec, 0.0658905 arcsec, -30.1402 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 336 : 0.080671 arcsec, 0.0658917 arcsec, -30.1399 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 337 : 0.0806726 arcsec, 0.0658931 arcsec, -30.1392 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 338 : 0.0806742 arcsec, 0.0658945 arcsec, -30.1387 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 339 : 0.0806759 arcsec, 0.0658959 arcsec, -30.1385 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 340 : 0.0806777 arcsec, 0.0658974 arcsec, -30.1377 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 341 : 0.0806792 arcsec, 0.0658987 arcsec, -30.1374 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 342 : 0.0806811 arcsec, 0.0659005 arcsec, -30.137 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 343 : 0.0806829 arcsec, 0.065902 arcsec, -30.1368 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 344 : 0.0806844 arcsec, 0.0659034 arcsec, -30.1366 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 345 : 0.0806861 arcsec, 0.0659048 arcsec, -30.1363 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 346 : 0.0806877 arcsec, 0.0659062 arcsec, -30.1361 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 347 : 0.0806895 arcsec, 0.0659082 arcsec, -30.1353 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 348 : 0.0806912 arcsec, 0.0659088 arcsec, -30.1361 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 349 : 0.0806927 arcsec, 0.0659102 arcsec, -30.1358 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 350 : 0.0806944 arcsec, 0.0659115 arcsec, -30.1358 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 351 : 0.080696 arcsec, 0.065913 arcsec, -30.1353 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 352 : 0.0806976 arcsec, 0.0659144 arcsec, -30.1352 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 353 : 0.0806991 arcsec, 0.0659159 arcsec, -30.1348 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 354 : 0.0807007 arcsec, 0.0659174 arcsec, -30.1342 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 355 : 0.0807025 arcsec, 0.0659191 arcsec, -30.1336 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 356 : 0.0807041 arcsec, 0.0659205 arcsec, -30.1331 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 357 : 0.080706 arcsec, 0.065922 arcsec, -30.133 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 358 : 0.0807077 arcsec, 0.0659234 arcsec, -30.1328 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 359 : 0.0807094 arcsec, 0.0659247 arcsec, -30.1326 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 360 : 0.0807112 arcsec, 0.0659263 arcsec, -30.1322 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 361 : 0.0807128 arcsec, 0.0659276 arcsec, -30.1319 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 362 : 0.0807144 arcsec, 0.0659287 arcsec, -30.132 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 363 : 0.0807161 arcsec, 0.06593 arcsec, -30.1319 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 364 : 0.0807177 arcsec, 0.0659313 arcsec, -30.1316 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 365 : 0.0807196 arcsec, 0.0659328 arcsec, -30.1312 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 366 : 0.0807213 arcsec, 0.0659341 arcsec, -30.1307 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 367 : 0.080723 arcsec, 0.0659355 arcsec, -30.1305 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 368 : 0.0807247 arcsec, 0.065937 arcsec, -30.1301 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 369 : 0.0807263 arcsec, 0.0659384 arcsec, -30.1297 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 370 : 0.0807281 arcsec, 0.0659397 arcsec, -30.1297 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 371 : 0.0807297 arcsec, 0.0659411 arcsec, -30.1294 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 372 : 0.0807314 arcsec, 0.0659425 arcsec, -30.129 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 373 : 0.0807334 arcsec, 0.0659442 arcsec, -30.1287 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 374 : 0.0807352 arcsec, 0.0659457 arcsec, -30.1287 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 375 : 0.080737 arcsec, 0.0659473 arcsec, -30.1284 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 376 : 0.0807387 arcsec, 0.0659487 arcsec, -30.128 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 377 : 0.0807403 arcsec, 0.0659502 arcsec, -30.1273 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 378 : 0.080742 arcsec, 0.0659517 arcsec, -30.1267 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 379 : 0.0807436 arcsec, 0.0659531 arcsec, -30.1264 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 380 : 0.0807454 arcsec, 0.0659545 arcsec, -30.1261 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 381 : 0.080747 arcsec, 0.0659559 arcsec, -30.1258 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 382 : 0.0807493 arcsec, 0.0659576 arcsec, -30.1256 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 383 : 0.0807511 arcsec, 0.0659591 arcsec, -30.1258 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 384 : 0.0807531 arcsec, 0.0659608 arcsec, -30.1254 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 385 : 0.0807549 arcsec, 0.0659625 arcsec, -30.1249 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 386 : 0.0807566 arcsec, 0.0659638 arcsec, -30.125 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 387 : 0.0807587 arcsec, 0.0659656 arcsec, -30.1249 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 388 : 0.0807603 arcsec, 0.0659669 arcsec, -30.1247 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 389 : 0.0807619 arcsec, 0.0659685 arcsec, -30.1242 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 390 : 0.0807636 arcsec, 0.0659699 arcsec, -30.1238 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 391 : 0.0807654 arcsec, 0.0659715 arcsec, -30.1233 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 392 : 0.0807668 arcsec, 0.0659727 arcsec, -30.1228 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 393 : 0.0807689 arcsec, 0.0659744 arcsec, -30.1228 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 394 : 0.0807704 arcsec, 0.0659758 arcsec, -30.1222 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 395 : 0.0807721 arcsec, 0.0659771 arcsec, -30.122 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 396 : 0.0807738 arcsec, 0.0659787 arcsec, -30.1213 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 397 : 0.0807756 arcsec, 0.0659801 arcsec, -30.121 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 398 : 0.0807773 arcsec, 0.0659815 arcsec, -30.1205 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 399 : 0.0807791 arcsec, 0.065983 arcsec, -30.1203 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 400 : 0.0807809 arcsec, 0.0659848 arcsec, -30.1197 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 401 : 0.0807825 arcsec, 0.0659861 arcsec, -30.1195 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 402 : 0.080784 arcsec, 0.0659875 arcsec, -30.1194 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 403 : 0.0807856 arcsec, 0.0659891 arcsec, -30.1189 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 404 : 0.0807873 arcsec, 0.0659904 arcsec, -30.1187 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 405 : 0.0807889 arcsec, 0.0659919 arcsec, -30.1182 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 406 : 0.0807906 arcsec, 0.0659934 arcsec, -30.118 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 407 : 0.0807922 arcsec, 0.0659948 arcsec, -30.1174 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 408 : 0.0807937 arcsec, 0.0659962 arcsec, -30.1171 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 409 : 0.0807955 arcsec, 0.0659977 arcsec, -30.1168 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 410 : 0.080797 arcsec, 0.0659991 arcsec, -30.1166 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 411 : 0.0807989 arcsec, 0.0660006 arcsec, -30.1164 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 412 : 0.0808006 arcsec, 0.0660022 arcsec, -30.1162 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 413 : 0.0808021 arcsec, 0.0660036 arcsec, -30.1158 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 414 : 0.0808036 arcsec, 0.066005 arcsec, -30.1153 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 415 : 0.0808052 arcsec, 0.0660064 arcsec, -30.115 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 416 : 0.0808069 arcsec, 0.0660079 arcsec, -30.1151 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 417 : 0.0808085 arcsec, 0.0660092 arcsec, -30.1146 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 418 : 0.0808102 arcsec, 0.0660106 arcsec, -30.1146 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 419 : 0.080812 arcsec, 0.0660122 arcsec, -30.1143 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 420 : 0.0808135 arcsec, 0.0660137 arcsec, -30.1136 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 421 : 0.0808151 arcsec, 0.0660151 arcsec, -30.1134 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 422 : 0.080817 arcsec, 0.0660167 arcsec, -30.1133 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 423 : 0.0808188 arcsec, 0.0660184 arcsec, -30.1131 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 424 : 0.0808204 arcsec, 0.0660197 arcsec, -30.1128 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 425 : 0.0808221 arcsec, 0.066021 arcsec, -30.1127 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 426 : 0.080824 arcsec, 0.0660225 arcsec, -30.1123 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 427 : 0.0808258 arcsec, 0.066024 arcsec, -30.1123 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 428 : 0.0808274 arcsec, 0.0660253 arcsec, -30.1117 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 429 : 0.0808292 arcsec, 0.0660269 arcsec, -30.1117 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 430 : 0.0808308 arcsec, 0.0660282 arcsec, -30.1114 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 431 : 0.0808325 arcsec, 0.0660298 arcsec, -30.111 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 432 : 0.0808342 arcsec, 0.0660313 arcsec, -30.1109 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 433 : 0.0808359 arcsec, 0.0660327 arcsec, -30.1104 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 434 : 0.0808377 arcsec, 0.0660343 arcsec, -30.1101 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 435 : 0.0808393 arcsec, 0.0660357 arcsec, -30.1098 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 436 : 0.0808409 arcsec, 0.066037 arcsec, -30.1098 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 437 : 0.0808426 arcsec, 0.0660385 arcsec, -30.1097 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 438 : 0.0808442 arcsec, 0.06604 arcsec, -30.1092 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 439 : 0.080846 arcsec, 0.0660415 arcsec, -30.1089 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 440 : 0.0808476 arcsec, 0.066043 arcsec, -30.1086 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 441 : 0.0808492 arcsec, 0.0660444 arcsec, -30.1082 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 442 : 0.0808512 arcsec, 0.0660459 arcsec, -30.108 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 443 : 0.0808529 arcsec, 0.0660472 arcsec, -30.1078 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 444 : 0.0808545 arcsec, 0.0660487 arcsec, -30.1074 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 445 : 0.0808562 arcsec, 0.0660502 arcsec, -30.1072 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 446 : 0.0808578 arcsec, 0.0660514 arcsec, -30.1069 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 447 : 0.0808593 arcsec, 0.0660528 arcsec, -30.1066 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 448 : 0.0808611 arcsec, 0.0660542 arcsec, -30.1065 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 449 : 0.0808627 arcsec, 0.0660559 arcsec, -30.106 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 450 : 0.0808645 arcsec, 0.0660574 arcsec, -30.1059 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 451 : 0.0808661 arcsec, 0.0660586 arcsec, -30.1058 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 452 : 0.0808679 arcsec, 0.0660601 arcsec, -30.1056 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 453 : 0.0808696 arcsec, 0.0660617 arcsec, -30.1053 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 454 : 0.0808714 arcsec, 0.066063 arcsec, -30.1054 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 455 : 0.0808734 arcsec, 0.0660648 arcsec, -30.105 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 456 : 0.0808754 arcsec, 0.0660666 arcsec, -30.1047 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 457 : 0.080877 arcsec, 0.0660682 arcsec, -30.1044 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 458 : 0.0808788 arcsec, 0.0660696 arcsec, -30.1045 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 459 : 0.080881 arcsec, 0.0660713 arcsec, -30.1044 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 460 : 0.0808826 arcsec, 0.0660728 arcsec, -30.1041 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 461 : 0.0808843 arcsec, 0.0660741 arcsec, -30.1039 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 462 : 0.0808864 arcsec, 0.0660757 arcsec, -30.104 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 463 : 0.0808881 arcsec, 0.0660773 arcsec, -30.1039 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 464 : 0.0808901 arcsec, 0.066079 arcsec, -30.1038 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 465 : 0.080892 arcsec, 0.0660805 arcsec, -30.1037 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 466 : 0.0808938 arcsec, 0.0660819 arcsec, -30.1033 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 467 : 0.0808953 arcsec, 0.0660833 arcsec, -30.1029 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 468 : 0.0808971 arcsec, 0.0660847 arcsec, -30.1029 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 469 : 0.0808986 arcsec, 0.066086 arcsec, -30.1027 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 470 : 0.0809003 arcsec, 0.0660873 arcsec, -30.1026 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 471 : 0.080902 arcsec, 0.0660887 arcsec, -30.1025 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 472 : 0.0809038 arcsec, 0.0660902 arcsec, -30.1021 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 473 : 0.0809053 arcsec, 0.0660916 arcsec, -30.1021 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 474 : 0.0809071 arcsec, 0.066093 arcsec, -30.1019 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 475 : 0.0809088 arcsec, 0.0660947 arcsec, -30.1014 deg
    2019-11-22 02:45:23	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 476 : 0.0809106 arcsec, 0.0660963 arcsec, -30.1011 deg
    2019-11-22 02:45:24	INFO	tclean::::casa	Result tclean: {}
    2019-11-22 02:45:24	INFO	tclean::::casa	Task tclean complete. Start time: 2019-11-21 20:39:05.657779 End time: 2019-11-21 20:45:23.623988
    2019-11-22 02:45:24	INFO	tclean::::casa	##### End Task: tclean               #####
    2019-11-22 02:45:24	INFO	tclean::::casa	##########################################
    2019-11-22 02:45:24	INFO	exportfits::::casa	##########################################
    2019-11-22 02:45:24	INFO	exportfits::::casa	##### Begin Task: exportfits         #####
    2019-11-22 02:45:24	INFO	exportfits::::casa	exportfits( imagename='bb1.co43/sci.image', fitsimage='bb1.co43/sci.fits', velocity=False, optical=False, bitpix=-32, minpix=0, maxpix=-1, overwrite=True, dropstokes=False, stokeslast=True, history=True, dropdeg=False )
    2019-11-22 02:45:24	INFO	exportfits::ImageFactory::toFITS	Applying mask of name 'mask0'
    2019-11-22 02:45:24	INFO	exportfits::ImageFitsConverter::ImageHeaderToFITS 	Truncating miscinfo field useweightimage to useweigh
    2019-11-22 02:45:24	INFO	exportfits::::casa	Result exportfits: None
    2019-11-22 02:45:24	INFO	exportfits::::casa	Task exportfits complete. Start time: 2019-11-21 20:45:23.631617 End time: 2019-11-21 20:45:24.486282
    2019-11-22 02:45:24	INFO	exportfits::::casa	##### End Task: exportfits           #####
    2019-11-22 02:45:24	INFO	exportfits::::casa	##########################################
    2019-11-22 02:45:27	INFO	tclean::::casa	##########################################
    2019-11-22 02:45:27	INFO	tclean::::casa	##### Begin Task: tclean             #####
    2019-11-22 02:45:27	INFO	tclean::::casa	tclean( vis='bb3.ms', selectdata=True, field='', spw='', timerange='', uvrange='', antenna='', scan='', observation='', intent='', datacolumn='data', imagename='bb3.ci10/sci', imsize=[256, 256], cell=0.01, phasecenter='', stokes='I', projection='SIN', startmodel='', specmode='cube', reffreq='', nchan=-1, start=0, width=1, outframe='LSRK', veltype='radio', restfreq=[], interpolation='nearest', perchanweightdensity=True, gridder='standard', facets=1, psfphasecenter='', chanchunks=1, wprojplanes=1, vptable='', mosweight=True, aterm=True, psterm=False, wbawp=True, conjbeams=False, cfcache='', usepointing=False, computepastep=360.0, rotatepastep=360.0, pointingoffsetsigdev=0.0, pblimit=0.2, normtype='flatnoise', deconvolver='hogbom', scales=[], nterms=2, smallscalebias=0.0, restoration=True, restoringbeam='', pbcor=False, outlierfile='', weighting='briggs', robust=1.0, noise='1.0Jy', npixels=0, uvtaper=[''], niter=0, gain=0.1, threshold=0.0, nsigma=0.0, cycleniter=-1, cyclefactor=1.0, minpsffraction=0.05, maxpsffraction=0.8, interactive=False, usemask='user', mask='', pbmask=0.0, sidelobethreshold=3.0, noisethreshold=5.0, lownoisethreshold=1.5, negativethreshold=0.0, smoothfactor=1.0, minbeamfrac=0.3, cutthreshold=0.01, growiterations=75, dogrowprune=True, minpercentchange=-1.0, verbose=False, fastnoise=True, restart=True, savemodel='none', calcres=True, calcpsf=True, parallel=False )
    2019-11-22 02:45:27	INFO	tclean::::casa	Verifying Input Parameters
    2019-11-22 02:45:27	INFO	SynthesisImagerVi2::selectData 	MS : bb3.ms | [Opened in readonly mode]
    2019-11-22 02:45:27	INFO	SynthesisImagerVi2::selectData 	  NRows selected : 276124
    2019-11-22 02:45:27	INFO	SynthesisImagerVi2::defineImage 	Define image coordinates for [bb3.ci10/sci] : 
    2019-11-22 02:45:27	INFO	MSTransformRegridder::calcChanFreqs	 phaseCenter='Direction: [0.973286, -0.0588582, 0.221923]'  Channels equidistant in freq
    2019-11-22 02:45:27	INFO	MSTransformRegridder::calcChanFreqs+	 Central frequency (in output frame) = 1.53609e+11 Hz
    2019-11-22 02:45:27	INFO	MSTransformRegridder::calcChanFreqs+	 Width of central channel (in output frame) = 3.90647e+06 Hz
    2019-11-22 02:45:27	INFO	MSTransformRegridder::calcChanFreqs+	 Number of channels = 477
    2019-11-22 02:45:27	INFO	MSTransformRegridder::calcChanFreqs+	 Total width of SPW (in output frame) = 1.86339e+09 Hz
    2019-11-22 02:45:27	INFO	MSTransformRegridder::calcChanFreqs+	 Lower edge = 1.52677e+11 Hz, upper edge = 1.54541e+11 Hz
    2019-11-22 02:45:27	INFO	SynthesisImagerVi2::defineImage 	Impars : start 0
    2019-11-22 02:45:27	INFO	SynthesisImagerVi2::defineImage 	Shape : [256, 256, 1, 477]Spectral : [1.52679e+11] at [0] with increment [3.90647e+06]
    2019-11-22 02:45:27	INFO	SynthesisImagerVi2::defineImage 	Set Gridding options for [bb3.ci10/sci] with ftmachine : gridft
    2019-11-22 02:45:27	INFO	SynthesisImagerVi2::weight() 	Set imaging weights : Briggs weighting: sidelobes will be suppressed over full image
    2019-11-22 02:45:27	INFO	SynthesisImagerVi2::weight() 	Doing spectral cube Briggs weighting formula --  norm
    2019-11-22 02:45:27	INFO	SynthesisImager::tuneSelectData 	Tuning frequency data selection to match image spectral coordinates
    2019-11-22 02:45:27	INFO	SynthesisImagerVi2::selectData 	MS : bb3.ms | [Opened in readonly mode]
    2019-11-22 02:45:27	INFO	SynthesisImagerVi2::selectData 	  NRows selected : 276124
    2019-11-22 02:45:27	INFO	task_tclean::SynthesisDeconvolver::setupDeconvolution 	Set Deconvolution Options for [bb3.ci10/sci] : hogbom
    2019-11-22 02:45:27	INFO	SynthesisImager::makePSF 	----------------------------------------------------------- Make PSF ---------------------------------------------
    
    0%....10....20....30....40....50....60....70....80....90....100%
    2019-11-22 02:48:36	INFO	SIImageStore::calcSensitivity 	[bb3.ci10/sci] Theoretical sensitivity (Jy/bm):c0:5.78688e-05 c1:5.78689e-05 c2:5.78688e-05 c3:5.7869e-05 c4:5.7869e-05 c5:5.78692e-05 c6:5.78692e-05 c7:5.78692e-05 c8:5.78691e-05 c9:5.78691e-05 c10:5.78691e-05 c11:5.78691e-05 c12:5.78691e-05 c13:5.78691e-05 c14:5.78691e-05 c15:5.78691e-05 c16:5.78692e-05 c17:5.78692e-05 c18:5.7869e-05 c19:5.7869e-05 c20:5.78689e-05 c21:5.78689e-05 c22:5.78689e-05 c23:5.78689e-05 c24:5.78689e-05 c25:5.7869e-05 c26:5.7869e-05 c27:5.78689e-05 c28:5.78689e-05 c29:5.78691e-05 c30:5.78691e-05 c31:5.7869e-05 c32:5.7869e-05 c33:5.7869e-05 c34:5.7869e-05 c35:5.7869e-05 c36:5.7869e-05 c37:5.7869e-05 c38:5.78692e-05 c39:5.78691e-05 c40:5.78691e-05 c41:5.78692e-05 c42:5.78692e-05 c43:5.78692e-05 c44:5.78692e-05 c45:5.78693e-05 c46:5.78693e-05 c47:5.78696e-05 c48:5.78696e-05 c49:5.78695e-05 c50:5.78695e-05 c51:5.78694e-05 c52:5.78694e-05 c53:5.78694e-05 c54:5.78694e-05 c55:5.78694e-05 c56:5.78694e-05 c57:5.78694e-05 c58:5.78695e-05 c59:5.78695e-05 c60:5.78695e-05 c61:5.78696e-05 c62:5.78695e-05 c63:5.78695e-05 c64:5.78695e-05 c65:5.78696e-05 c66:5.78696e-05 c67:5.78697e-05 c68:5.78697e-05 c69:5.78697e-05 c70:5.78697e-05 c71:5.78696e-05 c72:5.78699e-05 c73:5.787e-05 c74:5.787e-05 c75:5.787e-05 c76:5.78701e-05 c77:5.78702e-05 c78:5.78703e-05 c79:5.78702e-05 c80:5.78702e-05 c81:5.78702e-05 c82:5.78703e-05 c83:5.78703e-05 c84:5.78704e-05 c85:5.78703e-05 c86:5.78703e-05 c87:5.78702e-05 c88:5.78701e-05 c89:5.78701e-05 c90:5.78701e-05 c91:5.787e-05 c92:5.787e-05 c93:5.787e-05 c94:5.787e-05 c95:5.78699e-05 c96:5.78699e-05 c97:5.78698e-05 c98:5.78699e-05 c99:5.78698e-05 c100:5.787e-05 c101:5.78701e-05 c102:5.78702e-05 c103:5.78702e-05 c104:5.78703e-05 c105:5.78704e-05 c106:5.78706e-05 c107:5.78706e-05 c108:5.78706e-05 c109:5.78708e-05 c110:5.78707e-05 c111:5.78708e-05 c112:5.78708e-05 c113:5.78708e-05 c114:5.78708e-05 c115:5.78708e-05 c116:5.78708e-05 c117:5.78708e-05 c118:5.78708e-05 c119:5.78708e-05 c120:5.78708e-05 c121:5.7871e-05 c122:5.7871e-05 c123:5.78715e-05 c124:5.78714e-05 c125:5.78714e-05 c126:5.78713e-05 c127:5.78713e-05 c128:5.78713e-05 c129:5.78716e-05 c130:5.78718e-05 c131:5.78718e-05 c132:5.78718e-05 c133:5.78719e-05 c134:5.78721e-05 c135:5.78719e-05 c136:5.7872e-05 c137:5.78721e-05 c138:5.78721e-05 c139:5.78721e-05 c140:5.78721e-05 c141:5.78721e-05 c142:5.78722e-05 c143:5.78722e-05 c144:5.78723e-05 c145:5.78723e-05 c146:5.78724e-05 c147:5.78723e-05 c148:5.78723e-05 c149:5.78723e-05 c150:5.78722e-05 c151:5.78722e-05 c152:5.78722e-05 c153:5.78721e-05 c154:5.78721e-05 c155:5.78722e-05 c156:5.78721e-05 c157:5.78721e-05 c158:5.78721e-05 c159:5.78722e-05 c160:5.78722e-05 c161:5.78722e-05 c162:5.78722e-05 c163:5.78722e-05 c164:5.78722e-05 c165:5.78722e-05 c166:5.78723e-05 c167:5.78723e-05 c168:5.78723e-05 c169:5.78722e-05 c170:5.78722e-05 c171:5.78722e-05 c172:5.78722e-05 c173:5.78722e-05 c174:5.78721e-05 c175:5.78721e-05 c176:5.78722e-05 c177:5.78722e-05 c178:5.78723e-05 c179:5.78725e-05 c180:5.78726e-05 c181:5.78726e-05 c182:5.78726e-05 c183:5.78727e-05 c184:5.78727e-05 c185:5.78727e-05 c186:5.78727e-05 c187:5.78727e-05 c188:5.78727e-05 c189:5.78727e-05 c190:5.78726e-05 c191:5.78726e-05 c192:5.78726e-05 c193:5.78726e-05 c194:5.78727e-05 c195:5.78727e-05 c196:5.78728e-05 c197:5.78728e-05 c198:5.78727e-05 c199:5.78727e-05 c200:5.78727e-05 c201:5.78728e-05 c202:5.78728e-05 c203:5.78729e-05 c204:5.78729e-05 c205:5.7873e-05 c206:5.78729e-05 c207:5.78729e-05 c208:5.7873e-05 c209:5.7873e-05 c210:5.7873e-05 c211:5.7873e-05 c212:5.78731e-05 c213:5.78731e-05 c214:5.78731e-05 c215:5.78732e-05 c216:5.78734e-05 c217:5.78736e-05 c218:5.78737e-05 c219:5.78738e-05 c220:5.78739e-05 c221:5.78739e-05 c222:5.78739e-05 c223:5.78738e-05 c224:5.78738e-05 c225:5.78739e-05 c226:5.7874e-05 c227:5.7874e-05 c228:5.7874e-05 c229:5.7874e-05 c230:5.7874e-05 c231:5.7874e-05 c232:5.7874e-05 c233:5.7874e-05 c234:5.7874e-05 c235:5.7874e-05 c236:5.78741e-05 c237:5.78741e-05 c238:5.78741e-05 c239:5.78741e-05 c240:5.78742e-05 c241:5.78742e-05 c242:5.78742e-05 c243:5.78743e-05 c244:5.78742e-05 c245:5.78742e-05 c246:5.78742e-05 c247:5.78742e-05 c248:5.78742e-05 c249:5.78743e-05 c250:5.78743e-05 c251:5.78743e-05 c252:5.78742e-05 c253:5.78742e-05 c254:5.78742e-05 c255:5.78742e-05 c256:5.78742e-05 c257:5.78741e-05 c258:5.78741e-05 c259:5.78742e-05 c260:5.78741e-05 c261:5.78741e-05 c262:5.78741e-05 c263:5.78741e-05 c264:5.78741e-05 c265:5.78744e-05 c266:5.78743e-05 c267:5.78743e-05 c268:5.78743e-05 c269:5.78743e-05 c270:5.78743e-05 c271:5.78743e-05 c272:5.78742e-05 c273:5.78742e-05 c274:5.78744e-05 c275:5.78744e-05 c276:5.78744e-05 c277:5.78743e-05 c278:5.78746e-05 c279:5.78747e-05 c280:5.78747e-05 c281:5.78747e-05 c282:5.78746e-05 c283:5.78747e-05 c284:5.78748e-05 c285:5.78749e-05 c286:5.78748e-05 c287:5.78748e-05 c288:5.78747e-05 c289:5.78747e-05 c290:5.78749e-05 c291:5.78749e-05 c292:5.7875e-05 c293:5.78749e-05 c294:5.78751e-05 c295:5.78752e-05 c296:5.78752e-05 c297:5.78753e-05 c298:5.78753e-05 c299:5.78753e-05 c300:5.78753e-05 c301:5.78753e-05 c302:5.78753e-05 c303:5.78753e-05 c304:5.78753e-05 c305:5.78753e-05 c306:5.78753e-05 c307:5.78753e-05 c308:5.78753e-05 c309:5.78754e-05 c310:5.78753e-05 c311:5.78753e-05 c312:5.78753e-05 c313:5.78753e-05 c314:5.78753e-05 c315:5.78754e-05 c316:5.78755e-05 c317:5.78755e-05 c318:5.78757e-05 c319:5.78759e-05 c320:5.7876e-05 c321:5.7876e-05 c322:5.7876e-05 c323:5.78759e-05 c324:5.78761e-05 c325:5.78761e-05 c326:5.78761e-05 c327:5.78761e-05 c328:5.7876e-05 c329:5.7876e-05 c330:5.7876e-05 c331:5.78761e-05 c332:5.78762e-05 c333:5.78762e-05 c334:5.78763e-05 c335:5.78762e-05 c336:5.78763e-05 c337:5.78762e-05 c338:5.78762e-05 c339:5.78762e-05 c340:5.78761e-05 c341:5.78761e-05 c342:5.78761e-05 c343:5.78761e-05 c344:5.78761e-05 c345:5.78761e-05 c346:5.7876e-05 c347:5.7876e-05 c348:5.7876e-05 c349:5.7876e-05 c350:5.7876e-05 c351:5.7876e-05 c352:5.7876e-05 c353:5.7876e-05 c354:5.7876e-05 c355:5.7876e-05 c356:5.7876e-05 c357:5.78759e-05 c358:5.78759e-05 c359:5.78763e-05 c360:5.78764e-05 c361:5.78763e-05 c362:5.78764e-05 c363:5.78766e-05 c364:5.78766e-05 c365:5.78765e-05 c366:5.78766e-05 c367:5.78766e-05 c368:5.78766e-05 c369:5.78767e-05 c370:5.78767e-05 c371:5.78766e-05 c372:5.78766e-05 c373:5.78766e-05 c374:5.78766e-05 c375:5.78767e-05 c376:5.78767e-05 c377:5.78768e-05 c378:5.78768e-05 c379:5.78769e-05 c380:5.7877e-05 c381:5.7877e-05 c382:5.7877e-05 c383:5.78771e-05 c384:5.78771e-05 c385:5.78771e-05 c386:5.78771e-05 c387:5.78771e-05 c388:5.7877e-05 c389:5.7877e-05 c390:5.78768e-05 c391:5.78768e-05 c392:5.78769e-05 c393:5.7877e-05 c394:5.78772e-05 c395:5.78772e-05 c396:5.78772e-05 c397:5.78771e-05 c398:5.78771e-05 c399:5.78773e-05 c400:5.78774e-05 c401:5.78773e-05 c402:5.78773e-05 c403:5.78773e-05 c404:5.78773e-05 c405:5.78774e-05 c406:5.78774e-05 c407:5.78774e-05 c408:5.78775e-05 c409:5.78777e-05 c410:5.78777e-05 c411:5.78777e-05 c412:5.78776e-05 c413:5.78776e-05 c414:5.78776e-05 c415:5.78776e-05 c416:5.78776e-05 c417:5.78776e-05 c418:5.78777e-05 c419:5.78777e-05 c420:5.78776e-05 c421:5.78776e-05 c422:5.78776e-05 c423:5.78776e-05 c424:5.78776e-05 c425:5.78775e-05 c426:5.78774e-05 c427:5.78775e-05 c428:5.78775e-05 c429:5.78774e-05 c430:5.78774e-05 c431:5.78774e-05 c432:5.78773e-05 c433:5.78773e-05 c434:5.78772e-05 c435:5.78773e-05 c436:5.78773e-05 c437:5.78772e-05 c438:5.78773e-05 c439:5.78772e-05 c440:5.78773e-05 c441:5.78772e-05 c442:5.78773e-05 c443:5.78773e-05 c444:5.78775e-05 c445:5.78775e-05 c446:5.78776e-05 c447:5.78777e-05 c448:5.78776e-05 c449:5.78776e-05 c450:5.78776e-05 c451:5.78779e-05 c452:5.78779e-05 c453:5.7878e-05 c454:5.78781e-05 c455:5.78781e-05 c456:5.78781e-05 c457:5.78781e-05 c458:5.7878e-05 c459:5.7878e-05 c460:5.7878e-05 c461:5.78779e-05 c462:5.78779e-05 c463:5.78779e-05 c464:5.78779e-05 c465:5.78778e-05 c466:5.7878e-05 c467:5.7878e-05 c468:5.78781e-05 c469:5.78781e-05 c470:5.7878e-05 c471:5.7878e-05 c472:5.7878e-05 c473:5.7878e-05 c474:5.7878e-05 c475:5.7878e-05 c476:5.7878e-05 
    2019-11-22 02:48:38	INFO	SIImageStore::printBeamSet 	Restoring Beams 
    2019-11-22 02:48:38	INFO	SIImageStore::printBeamSet +	Pol   Type Chan        Freq     Vel
    2019-11-22 02:48:38	INFO	SIImageStore::printBeamSet +	  I    Max    0 1.52679e+11 206977.78    0.0767 arcsec x    0.0606 arcsec pa=-36.2303 deg
    2019-11-22 02:48:38	INFO	SIImageStore::printBeamSet +	  I    Min  476 1.54539e+11 205847.40    0.0760 arcsec x    0.0600 arcsec pa=-36.3047 deg
    2019-11-22 02:48:38	INFO	SIImageStore::printBeamSet +	  I Median  238 1.53609e+11 206412.59    0.0763 arcsec x    0.0603 arcsec pa=-36.2626 deg
    2019-11-22 02:48:38	INFO	task_tclean::SynthesisImagerVi2::makePrimaryBeam 	vi2 : Evaluating Primary Beam model onto image grid(s)
    2019-11-22 02:48:41	INFO	task_tclean::SynthesisImager::executeMajorCycle 	----------------------------------------------------------- Run (Last) Major Cycle 1 -------------------------------------
    
    0%....10....20....30....40....50....60....70....80....90....100%
    2019-11-22 02:51:43	INFO	task_tclean::SDAlgorithmBase::restore 	[bb3.ci10/sci] : Restoring model image.
    2019-11-22 02:51:43	WARN	task_tclean::SIImageStore::restore (file casa-source/code/synthesis/ImagerObjects/SIImageStore.cc, line 2068)	Restoring with an empty model image. Only residuals will be processed to form the output restored image.
    2019-11-22 02:51:43	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 0 : 0.0766514 arcsec, 0.0605668 arcsec, -36.2303 deg
    2019-11-22 02:51:43	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 1 : 0.07665 arcsec, 0.0605656 arcsec, -36.2303 deg
    2019-11-22 02:51:43	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 2 : 0.0766487 arcsec, 0.0605643 arcsec, -36.2306 deg
    2019-11-22 02:51:43	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 3 : 0.0766469 arcsec, 0.0605629 arcsec, -36.2307 deg
    2019-11-22 02:51:43	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 4 : 0.0766456 arcsec, 0.0605617 arcsec, -36.2306 deg
    2019-11-22 02:51:43	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 5 : 0.0766439 arcsec, 0.0605603 arcsec, -36.2309 deg
    2019-11-22 02:51:43	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 6 : 0.0766425 arcsec, 0.0605593 arcsec, -36.2308 deg
    2019-11-22 02:51:43	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 7 : 0.0766412 arcsec, 0.0605582 arcsec, -36.2311 deg
    2019-11-22 02:51:43	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 8 : 0.0766399 arcsec, 0.0605571 arcsec, -36.2312 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 9 : 0.0766385 arcsec, 0.0605559 arcsec, -36.2314 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 10 : 0.076637 arcsec, 0.0605547 arcsec, -36.2316 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 11 : 0.0766355 arcsec, 0.0605536 arcsec, -36.2316 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 12 : 0.076634 arcsec, 0.0605524 arcsec, -36.2314 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 13 : 0.0766326 arcsec, 0.0605514 arcsec, -36.2316 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 14 : 0.0766311 arcsec, 0.0605503 arcsec, -36.2321 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 15 : 0.0766299 arcsec, 0.0605492 arcsec, -36.2325 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 16 : 0.0766285 arcsec, 0.0605481 arcsec, -36.2328 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 17 : 0.0766271 arcsec, 0.0605469 arcsec, -36.2327 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 18 : 0.0766259 arcsec, 0.0605456 arcsec, -36.2329 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 19 : 0.0766244 arcsec, 0.0605442 arcsec, -36.2333 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 20 : 0.0766231 arcsec, 0.0605431 arcsec, -36.2334 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 21 : 0.0766218 arcsec, 0.060542 arcsec, -36.2335 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 22 : 0.0766203 arcsec, 0.0605408 arcsec, -36.2334 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 23 : 0.0766189 arcsec, 0.0605396 arcsec, -36.2335 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 24 : 0.0766176 arcsec, 0.0605383 arcsec, -36.2336 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 25 : 0.0766161 arcsec, 0.0605372 arcsec, -36.2339 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 26 : 0.0766146 arcsec, 0.0605361 arcsec, -36.2337 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 27 : 0.0766132 arcsec, 0.060535 arcsec, -36.2334 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 28 : 0.0766119 arcsec, 0.0605337 arcsec, -36.2335 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 29 : 0.0766102 arcsec, 0.0605323 arcsec, -36.2335 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 30 : 0.0766089 arcsec, 0.060531 arcsec, -36.2335 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 31 : 0.0766076 arcsec, 0.0605297 arcsec, -36.2337 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 32 : 0.0766061 arcsec, 0.0605286 arcsec, -36.2337 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 33 : 0.0766048 arcsec, 0.0605276 arcsec, -36.2337 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 34 : 0.0766034 arcsec, 0.0605264 arcsec, -36.2339 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 35 : 0.076602 arcsec, 0.0605252 arcsec, -36.2341 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 36 : 0.0766007 arcsec, 0.0605238 arcsec, -36.2345 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 37 : 0.0765994 arcsec, 0.0605227 arcsec, -36.2349 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 38 : 0.0765977 arcsec, 0.0605213 arcsec, -36.2348 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 39 : 0.0765963 arcsec, 0.0605202 arcsec, -36.235 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 40 : 0.0765949 arcsec, 0.060519 arcsec, -36.2353 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 41 : 0.0765935 arcsec, 0.0605179 arcsec, -36.2353 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 42 : 0.0765922 arcsec, 0.0605167 arcsec, -36.2355 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 43 : 0.0765909 arcsec, 0.0605154 arcsec, -36.2358 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 44 : 0.0765896 arcsec, 0.0605143 arcsec, -36.236 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 45 : 0.076588 arcsec, 0.0605129 arcsec, -36.236 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 46 : 0.0765865 arcsec, 0.0605116 arcsec, -36.2358 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 47 : 0.0765848 arcsec, 0.0605101 arcsec, -36.2359 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 48 : 0.0765834 arcsec, 0.0605089 arcsec, -36.2359 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 49 : 0.0765819 arcsec, 0.0605077 arcsec, -36.2359 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 50 : 0.0765805 arcsec, 0.0605064 arcsec, -36.2361 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 51 : 0.076579 arcsec, 0.0605052 arcsec, -36.2364 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 52 : 0.0765774 arcsec, 0.0605041 arcsec, -36.2365 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 53 : 0.076576 arcsec, 0.0605028 arcsec, -36.2366 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 54 : 0.0765746 arcsec, 0.0605017 arcsec, -36.2369 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 55 : 0.0765734 arcsec, 0.0605003 arcsec, -36.2372 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 56 : 0.0765721 arcsec, 0.0604991 arcsec, -36.2373 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 57 : 0.0765707 arcsec, 0.0604978 arcsec, -36.2374 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 58 : 0.0765691 arcsec, 0.0604964 arcsec, -36.2376 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 59 : 0.0765678 arcsec, 0.0604952 arcsec, -36.2379 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 60 : 0.0765664 arcsec, 0.0604939 arcsec, -36.238 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 61 : 0.0765649 arcsec, 0.0604926 arcsec, -36.2384 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 62 : 0.0765637 arcsec, 0.0604914 arcsec, -36.2385 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 63 : 0.0765622 arcsec, 0.0604903 arcsec, -36.2383 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 64 : 0.0765607 arcsec, 0.060489 arcsec, -36.2387 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 65 : 0.0765592 arcsec, 0.0604877 arcsec, -36.2387 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 66 : 0.0765576 arcsec, 0.0604867 arcsec, -36.2386 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 67 : 0.076556 arcsec, 0.0604855 arcsec, -36.2387 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 68 : 0.0765545 arcsec, 0.0604842 arcsec, -36.2387 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 69 : 0.0765531 arcsec, 0.060483 arcsec, -36.2388 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 70 : 0.0765515 arcsec, 0.0604818 arcsec, -36.2388 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 71 : 0.0765501 arcsec, 0.0604806 arcsec, -36.2386 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 72 : 0.0765485 arcsec, 0.0604792 arcsec, -36.239 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 73 : 0.076547 arcsec, 0.0604776 arcsec, -36.2394 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 74 : 0.0765457 arcsec, 0.0604767 arcsec, -36.2396 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 75 : 0.0765443 arcsec, 0.0604755 arcsec, -36.2398 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 76 : 0.076543 arcsec, 0.0604741 arcsec, -36.2399 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 77 : 0.0765416 arcsec, 0.0604726 arcsec, -36.2401 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 78 : 0.0765401 arcsec, 0.0604714 arcsec, -36.2402 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 79 : 0.0765386 arcsec, 0.06047 arcsec, -36.2405 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 80 : 0.0765374 arcsec, 0.0604687 arcsec, -36.2406 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 81 : 0.0765359 arcsec, 0.0604675 arcsec, -36.2406 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 82 : 0.0765343 arcsec, 0.0604661 arcsec, -36.2408 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 83 : 0.0765329 arcsec, 0.0604651 arcsec, -36.2407 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 84 : 0.0765314 arcsec, 0.0604638 arcsec, -36.2408 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 85 : 0.0765301 arcsec, 0.0604626 arcsec, -36.241 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 86 : 0.0765288 arcsec, 0.0604611 arcsec, -36.2414 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 87 : 0.0765275 arcsec, 0.0604599 arcsec, -36.2413 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 88 : 0.0765262 arcsec, 0.0604589 arcsec, -36.2414 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 89 : 0.0765249 arcsec, 0.0604575 arcsec, -36.242 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 90 : 0.0765236 arcsec, 0.0604564 arcsec, -36.2422 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 91 : 0.0765222 arcsec, 0.0604553 arcsec, -36.2423 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 92 : 0.0765208 arcsec, 0.060454 arcsec, -36.2424 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 93 : 0.0765194 arcsec, 0.0604529 arcsec, -36.2423 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 94 : 0.0765181 arcsec, 0.0604518 arcsec, -36.2426 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 95 : 0.0765167 arcsec, 0.0604505 arcsec, -36.2424 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 96 : 0.0765153 arcsec, 0.0604494 arcsec, -36.2425 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 97 : 0.0765141 arcsec, 0.0604484 arcsec, -36.2427 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 98 : 0.0765126 arcsec, 0.0604473 arcsec, -36.243 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 99 : 0.0765112 arcsec, 0.0604461 arcsec, -36.2429 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 100 : 0.0765096 arcsec, 0.0604449 arcsec, -36.2431 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 101 : 0.0765082 arcsec, 0.0604432 arcsec, -36.2436 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 102 : 0.0765065 arcsec, 0.0604419 arcsec, -36.2435 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 103 : 0.0765052 arcsec, 0.0604408 arcsec, -36.2435 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 104 : 0.0765038 arcsec, 0.0604395 arcsec, -36.2438 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 105 : 0.0765024 arcsec, 0.0604383 arcsec, -36.2439 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 106 : 0.0765008 arcsec, 0.0604368 arcsec, -36.2441 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 107 : 0.0764995 arcsec, 0.0604357 arcsec, -36.2443 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 108 : 0.076498 arcsec, 0.0604344 arcsec, -36.2444 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 109 : 0.0764965 arcsec, 0.0604331 arcsec, -36.2444 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 110 : 0.076495 arcsec, 0.0604319 arcsec, -36.2447 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 111 : 0.0764936 arcsec, 0.0604306 arcsec, -36.2447 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 112 : 0.0764922 arcsec, 0.0604295 arcsec, -36.2452 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 113 : 0.0764907 arcsec, 0.0604281 arcsec, -36.2452 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 114 : 0.0764893 arcsec, 0.0604269 arcsec, -36.2455 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 115 : 0.0764876 arcsec, 0.0604257 arcsec, -36.2455 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 116 : 0.076486 arcsec, 0.0604244 arcsec, -36.2456 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 117 : 0.0764848 arcsec, 0.0604228 arcsec, -36.246 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 118 : 0.0764834 arcsec, 0.0604216 arcsec, -36.2462 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 119 : 0.0764819 arcsec, 0.0604201 arcsec, -36.2463 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 120 : 0.0764804 arcsec, 0.0604188 arcsec, -36.2465 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 121 : 0.0764787 arcsec, 0.0604175 arcsec, -36.2465 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 122 : 0.0764773 arcsec, 0.0604161 arcsec, -36.2466 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 123 : 0.0764751 arcsec, 0.0604144 arcsec, -36.2469 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 124 : 0.076474 arcsec, 0.0604136 arcsec, -36.247 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 125 : 0.0764726 arcsec, 0.0604124 arcsec, -36.2469 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 126 : 0.0764713 arcsec, 0.0604112 arcsec, -36.247 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 127 : 0.0764699 arcsec, 0.0604099 arcsec, -36.2472 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 128 : 0.0764687 arcsec, 0.0604087 arcsec, -36.247 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 129 : 0.0764669 arcsec, 0.0604074 arcsec, -36.247 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 130 : 0.0764654 arcsec, 0.0604059 arcsec, -36.2472 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 131 : 0.0764642 arcsec, 0.0604047 arcsec, -36.2477 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 132 : 0.0764628 arcsec, 0.0604036 arcsec, -36.2478 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 133 : 0.0764615 arcsec, 0.0604025 arcsec, -36.2481 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 134 : 0.0764602 arcsec, 0.0604012 arcsec, -36.2484 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 135 : 0.0764584 arcsec, 0.0604001 arcsec, -36.2484 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 136 : 0.076457 arcsec, 0.060399 arcsec, -36.2485 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 137 : 0.0764556 arcsec, 0.0603976 arcsec, -36.2487 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 138 : 0.0764541 arcsec, 0.0603964 arcsec, -36.2488 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 139 : 0.0764527 arcsec, 0.0603951 arcsec, -36.2491 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 140 : 0.0764512 arcsec, 0.0603941 arcsec, -36.2494 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 141 : 0.0764498 arcsec, 0.060393 arcsec, -36.2493 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 142 : 0.0764483 arcsec, 0.0603918 arcsec, -36.2495 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 143 : 0.076447 arcsec, 0.0603907 arcsec, -36.2498 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 144 : 0.0764454 arcsec, 0.0603893 arcsec, -36.25 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 145 : 0.0764442 arcsec, 0.060388 arcsec, -36.2504 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 146 : 0.0764428 arcsec, 0.0603868 arcsec, -36.2506 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 147 : 0.0764414 arcsec, 0.0603856 arcsec, -36.2506 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 148 : 0.0764399 arcsec, 0.0603843 arcsec, -36.2508 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 149 : 0.0764386 arcsec, 0.0603831 arcsec, -36.2509 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 150 : 0.0764374 arcsec, 0.0603818 arcsec, -36.2513 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 151 : 0.0764362 arcsec, 0.0603807 arcsec, -36.2513 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 152 : 0.0764349 arcsec, 0.0603794 arcsec, -36.2514 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 153 : 0.0764334 arcsec, 0.0603782 arcsec, -36.2517 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 154 : 0.0764319 arcsec, 0.0603772 arcsec, -36.2517 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 155 : 0.0764305 arcsec, 0.0603757 arcsec, -36.2522 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 156 : 0.0764294 arcsec, 0.0603743 arcsec, -36.2528 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 157 : 0.0764281 arcsec, 0.0603731 arcsec, -36.253 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 158 : 0.0764267 arcsec, 0.0603719 arcsec, -36.2533 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 159 : 0.0764253 arcsec, 0.0603707 arcsec, -36.2536 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 160 : 0.0764237 arcsec, 0.0603694 arcsec, -36.2535 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 161 : 0.0764225 arcsec, 0.0603679 arcsec, -36.254 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 162 : 0.0764211 arcsec, 0.0603668 arcsec, -36.2538 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 163 : 0.0764197 arcsec, 0.0603656 arcsec, -36.2538 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 164 : 0.0764181 arcsec, 0.0603642 arcsec, -36.254 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 165 : 0.0764167 arcsec, 0.0603631 arcsec, -36.2541 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 166 : 0.0764152 arcsec, 0.0603619 arcsec, -36.2542 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 167 : 0.0764138 arcsec, 0.0603607 arcsec, -36.2545 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 168 : 0.0764125 arcsec, 0.0603596 arcsec, -36.2547 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 169 : 0.076411 arcsec, 0.0603583 arcsec, -36.2546 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 170 : 0.0764096 arcsec, 0.0603573 arcsec, -36.2547 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 171 : 0.0764082 arcsec, 0.0603561 arcsec, -36.2549 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 172 : 0.0764068 arcsec, 0.0603548 arcsec, -36.2549 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 173 : 0.0764055 arcsec, 0.0603537 arcsec, -36.2549 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 174 : 0.0764041 arcsec, 0.0603526 arcsec, -36.2548 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 175 : 0.0764029 arcsec, 0.0603513 arcsec, -36.255 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 176 : 0.0764013 arcsec, 0.0603499 arcsec, -36.2552 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 177 : 0.0763999 arcsec, 0.0603486 arcsec, -36.2552 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 178 : 0.0763987 arcsec, 0.0603475 arcsec, -36.2553 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 179 : 0.0763971 arcsec, 0.060346 arcsec, -36.2555 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 180 : 0.0763956 arcsec, 0.0603448 arcsec, -36.2556 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 181 : 0.0763943 arcsec, 0.0603438 arcsec, -36.2556 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 182 : 0.0763926 arcsec, 0.0603426 arcsec, -36.2559 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 183 : 0.0763911 arcsec, 0.0603411 arcsec, -36.2561 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 184 : 0.0763898 arcsec, 0.0603399 arcsec, -36.2563 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 185 : 0.0763884 arcsec, 0.0603388 arcsec, -36.2563 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 186 : 0.0763869 arcsec, 0.0603375 arcsec, -36.2564 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 187 : 0.0763856 arcsec, 0.0603363 arcsec, -36.2565 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 188 : 0.0763842 arcsec, 0.0603351 arcsec, -36.2567 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 189 : 0.0763829 arcsec, 0.0603338 arcsec, -36.257 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 190 : 0.0763816 arcsec, 0.0603325 arcsec, -36.2571 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 191 : 0.0763802 arcsec, 0.0603314 arcsec, -36.2567 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 192 : 0.0763788 arcsec, 0.0603302 arcsec, -36.2565 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 193 : 0.0763774 arcsec, 0.0603291 arcsec, -36.2563 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 194 : 0.0763761 arcsec, 0.0603278 arcsec, -36.2562 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 195 : 0.0763746 arcsec, 0.0603266 arcsec, -36.256 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 196 : 0.0763729 arcsec, 0.0603255 arcsec, -36.2558 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 197 : 0.0763715 arcsec, 0.0603242 arcsec, -36.2561 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 198 : 0.0763701 arcsec, 0.0603229 arcsec, -36.2561 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 199 : 0.0763687 arcsec, 0.0603217 arcsec, -36.2563 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 200 : 0.0763673 arcsec, 0.0603204 arcsec, -36.2565 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 201 : 0.0763659 arcsec, 0.0603193 arcsec, -36.2567 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 202 : 0.0763644 arcsec, 0.060318 arcsec, -36.2568 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 203 : 0.0763628 arcsec, 0.0603169 arcsec, -36.2569 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 204 : 0.0763614 arcsec, 0.0603156 arcsec, -36.257 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 205 : 0.0763601 arcsec, 0.0603142 arcsec, -36.2576 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 206 : 0.0763588 arcsec, 0.0603129 arcsec, -36.2581 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 207 : 0.0763572 arcsec, 0.0603119 arcsec, -36.2579 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 208 : 0.0763558 arcsec, 0.0603104 arcsec, -36.2582 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 209 : 0.0763544 arcsec, 0.0603092 arcsec, -36.2585 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 210 : 0.076353 arcsec, 0.060308 arcsec, -36.2586 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 211 : 0.0763516 arcsec, 0.0603068 arcsec, -36.2587 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 212 : 0.0763501 arcsec, 0.0603057 arcsec, -36.2587 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 213 : 0.0763489 arcsec, 0.0603044 arcsec, -36.2593 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 214 : 0.0763474 arcsec, 0.060303 arcsec, -36.2593 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 215 : 0.0763459 arcsec, 0.0603019 arcsec, -36.2595 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 216 : 0.0763441 arcsec, 0.0603004 arcsec, -36.2597 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 217 : 0.0763424 arcsec, 0.0602991 arcsec, -36.2596 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 218 : 0.0763409 arcsec, 0.0602977 arcsec, -36.2595 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 219 : 0.0763393 arcsec, 0.0602965 arcsec, -36.2593 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 220 : 0.0763377 arcsec, 0.0602951 arcsec, -36.2594 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 221 : 0.0763365 arcsec, 0.060294 arcsec, -36.2595 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 222 : 0.076335 arcsec, 0.0602927 arcsec, -36.2597 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 223 : 0.0763337 arcsec, 0.0602914 arcsec, -36.2599 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 224 : 0.0763323 arcsec, 0.0602899 arcsec, -36.2603 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 225 : 0.0763308 arcsec, 0.0602885 arcsec, -36.2607 deg
    2019-11-22 02:51:44	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 226 : 0.0763295 arcsec, 0.0602871 arcsec, -36.261 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 227 : 0.0763282 arcsec, 0.0602858 arcsec, -36.2612 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 228 : 0.0763267 arcsec, 0.0602848 arcsec, -36.2611 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 229 : 0.0763254 arcsec, 0.0602838 arcsec, -36.2613 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 230 : 0.0763242 arcsec, 0.0602825 arcsec, -36.2616 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 231 : 0.0763227 arcsec, 0.0602813 arcsec, -36.2614 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 232 : 0.0763211 arcsec, 0.0602801 arcsec, -36.2614 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 233 : 0.0763198 arcsec, 0.0602789 arcsec, -36.2615 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 234 : 0.0763185 arcsec, 0.0602776 arcsec, -36.2617 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 235 : 0.0763173 arcsec, 0.0602764 arcsec, -36.262 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 236 : 0.0763159 arcsec, 0.0602751 arcsec, -36.2624 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 237 : 0.0763145 arcsec, 0.0602736 arcsec, -36.2628 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 238 : 0.0763131 arcsec, 0.0602725 arcsec, -36.2626 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 239 : 0.0763118 arcsec, 0.0602714 arcsec, -36.2627 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 240 : 0.0763104 arcsec, 0.06027 arcsec, -36.2629 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 241 : 0.076309 arcsec, 0.0602689 arcsec, -36.2629 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 242 : 0.0763077 arcsec, 0.0602677 arcsec, -36.2634 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 243 : 0.0763061 arcsec, 0.0602663 arcsec, -36.2634 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 244 : 0.0763049 arcsec, 0.0602651 arcsec, -36.2638 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 245 : 0.0763036 arcsec, 0.0602637 arcsec, -36.264 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 246 : 0.0763022 arcsec, 0.0602624 arcsec, -36.2644 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 247 : 0.0763009 arcsec, 0.0602614 arcsec, -36.2646 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 248 : 0.0762995 arcsec, 0.0602603 arcsec, -36.2648 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 249 : 0.076298 arcsec, 0.0602591 arcsec, -36.2649 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 250 : 0.0762967 arcsec, 0.0602577 arcsec, -36.2655 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 251 : 0.0762952 arcsec, 0.0602565 arcsec, -36.2656 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 252 : 0.0762938 arcsec, 0.0602553 arcsec, -36.2659 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 253 : 0.0762925 arcsec, 0.0602542 arcsec, -36.266 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 254 : 0.0762912 arcsec, 0.0602531 arcsec, -36.2662 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 255 : 0.0762898 arcsec, 0.0602517 arcsec, -36.2664 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 256 : 0.0762884 arcsec, 0.0602506 arcsec, -36.2666 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 257 : 0.0762869 arcsec, 0.0602493 arcsec, -36.2667 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 258 : 0.0762856 arcsec, 0.0602481 arcsec, -36.2669 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 259 : 0.0762842 arcsec, 0.0602467 arcsec, -36.2673 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 260 : 0.076283 arcsec, 0.0602456 arcsec, -36.2676 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 261 : 0.0762816 arcsec, 0.0602445 arcsec, -36.2677 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 262 : 0.0762804 arcsec, 0.060243 arcsec, -36.2682 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 263 : 0.076279 arcsec, 0.060242 arcsec, -36.2684 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 264 : 0.0762776 arcsec, 0.060241 arcsec, -36.2684 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 265 : 0.0762758 arcsec, 0.0602396 arcsec, -36.2686 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 266 : 0.0762745 arcsec, 0.0602384 arcsec, -36.2688 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 267 : 0.0762733 arcsec, 0.0602372 arcsec, -36.2689 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 268 : 0.076272 arcsec, 0.0602361 arcsec, -36.269 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 269 : 0.0762706 arcsec, 0.0602347 arcsec, -36.2693 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 270 : 0.0762693 arcsec, 0.0602335 arcsec, -36.2694 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 271 : 0.076268 arcsec, 0.0602322 arcsec, -36.2695 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 272 : 0.0762666 arcsec, 0.0602307 arcsec, -36.27 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 273 : 0.0762652 arcsec, 0.0602297 arcsec, -36.2699 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 274 : 0.0762637 arcsec, 0.0602283 arcsec, -36.2701 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 275 : 0.0762624 arcsec, 0.0602271 arcsec, -36.2702 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 276 : 0.0762609 arcsec, 0.060226 arcsec, -36.2702 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 277 : 0.0762596 arcsec, 0.0602249 arcsec, -36.2703 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 278 : 0.0762579 arcsec, 0.0602234 arcsec, -36.2702 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 279 : 0.0762565 arcsec, 0.0602222 arcsec, -36.2704 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 280 : 0.0762551 arcsec, 0.060221 arcsec, -36.2705 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 281 : 0.0762535 arcsec, 0.0602196 arcsec, -36.2705 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 282 : 0.076252 arcsec, 0.0602183 arcsec, -36.2704 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 283 : 0.0762506 arcsec, 0.060217 arcsec, -36.2706 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 284 : 0.0762491 arcsec, 0.0602157 arcsec, -36.2704 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 285 : 0.0762474 arcsec, 0.0602144 arcsec, -36.2702 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 286 : 0.0762462 arcsec, 0.0602134 arcsec, -36.2704 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 287 : 0.0762449 arcsec, 0.0602122 arcsec, -36.2704 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 288 : 0.0762437 arcsec, 0.060211 arcsec, -36.2708 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 289 : 0.0762424 arcsec, 0.06021 arcsec, -36.2711 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 290 : 0.0762407 arcsec, 0.0602085 arcsec, -36.2713 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 291 : 0.0762394 arcsec, 0.0602072 arcsec, -36.2715 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 292 : 0.0762377 arcsec, 0.0602059 arcsec, -36.2716 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 293 : 0.0762363 arcsec, 0.0602047 arcsec, -36.2716 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 294 : 0.0762347 arcsec, 0.0602033 arcsec, -36.2718 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 295 : 0.0762334 arcsec, 0.0602018 arcsec, -36.2723 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 296 : 0.0762321 arcsec, 0.0602008 arcsec, -36.2724 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 297 : 0.0762306 arcsec, 0.0601994 arcsec, -36.2727 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 298 : 0.0762291 arcsec, 0.0601981 arcsec, -36.2728 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 299 : 0.0762278 arcsec, 0.0601969 arcsec, -36.2731 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 300 : 0.0762265 arcsec, 0.0601956 arcsec, -36.2734 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 301 : 0.0762252 arcsec, 0.0601942 arcsec, -36.2736 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 302 : 0.0762238 arcsec, 0.060193 arcsec, -36.2739 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 303 : 0.0762222 arcsec, 0.0601918 arcsec, -36.2738 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 304 : 0.0762208 arcsec, 0.0601907 arcsec, -36.274 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 305 : 0.0762194 arcsec, 0.0601893 arcsec, -36.2746 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 306 : 0.076218 arcsec, 0.060188 arcsec, -36.2747 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 307 : 0.0762166 arcsec, 0.0601867 arcsec, -36.2749 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 308 : 0.0762153 arcsec, 0.0601856 arcsec, -36.2751 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 309 : 0.0762141 arcsec, 0.0601845 arcsec, -36.2753 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 310 : 0.0762126 arcsec, 0.0601832 arcsec, -36.2754 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 311 : 0.0762112 arcsec, 0.0601819 arcsec, -36.2757 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 312 : 0.0762098 arcsec, 0.0601806 arcsec, -36.2758 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 313 : 0.0762086 arcsec, 0.0601794 arcsec, -36.2762 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 314 : 0.0762071 arcsec, 0.0601783 arcsec, -36.2763 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 315 : 0.0762057 arcsec, 0.0601771 arcsec, -36.2766 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 316 : 0.0762042 arcsec, 0.060176 arcsec, -36.2767 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 317 : 0.0762028 arcsec, 0.0601748 arcsec, -36.2766 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 318 : 0.0762011 arcsec, 0.0601736 arcsec, -36.2766 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 319 : 0.0761994 arcsec, 0.0601722 arcsec, -36.2765 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 320 : 0.076198 arcsec, 0.0601708 arcsec, -36.2766 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 321 : 0.0761966 arcsec, 0.0601696 arcsec, -36.2766 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 322 : 0.0761954 arcsec, 0.0601686 arcsec, -36.2767 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 323 : 0.0761941 arcsec, 0.0601674 arcsec, -36.2769 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 324 : 0.0761927 arcsec, 0.0601659 arcsec, -36.2772 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 325 : 0.0761914 arcsec, 0.0601648 arcsec, -36.2774 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 326 : 0.0761901 arcsec, 0.0601637 arcsec, -36.2776 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 327 : 0.076189 arcsec, 0.0601626 arcsec, -36.2781 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 328 : 0.0761877 arcsec, 0.0601612 arcsec, -36.2781 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 329 : 0.0761861 arcsec, 0.0601598 arcsec, -36.2781 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 330 : 0.0761846 arcsec, 0.0601585 arcsec, -36.2781 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 331 : 0.076183 arcsec, 0.0601571 arcsec, -36.2782 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 332 : 0.0761818 arcsec, 0.0601561 arcsec, -36.2784 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 333 : 0.0761804 arcsec, 0.060155 arcsec, -36.2786 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 334 : 0.0761789 arcsec, 0.0601538 arcsec, -36.2786 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 335 : 0.0761778 arcsec, 0.0601524 arcsec, -36.2791 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 336 : 0.0761764 arcsec, 0.0601511 arcsec, -36.2792 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 337 : 0.076175 arcsec, 0.0601498 arcsec, -36.2795 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 338 : 0.0761736 arcsec, 0.0601487 arcsec, -36.2798 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 339 : 0.0761722 arcsec, 0.0601475 arcsec, -36.2798 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 340 : 0.0761709 arcsec, 0.0601464 arcsec, -36.28 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 341 : 0.0761696 arcsec, 0.0601451 arcsec, -36.2803 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 342 : 0.0761683 arcsec, 0.0601439 arcsec, -36.2803 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 343 : 0.0761667 arcsec, 0.0601427 arcsec, -36.2804 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 344 : 0.0761653 arcsec, 0.0601415 arcsec, -36.2807 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 345 : 0.0761639 arcsec, 0.0601403 arcsec, -36.2809 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 346 : 0.0761624 arcsec, 0.060139 arcsec, -36.2813 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 347 : 0.076161 arcsec, 0.0601379 arcsec, -36.2815 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 348 : 0.0761597 arcsec, 0.0601366 arcsec, -36.2817 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 349 : 0.0761585 arcsec, 0.0601354 arcsec, -36.282 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 350 : 0.0761572 arcsec, 0.0601343 arcsec, -36.2826 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 351 : 0.0761557 arcsec, 0.0601332 arcsec, -36.2824 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 352 : 0.0761545 arcsec, 0.060132 arcsec, -36.2829 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 353 : 0.0761532 arcsec, 0.0601309 arcsec, -36.2831 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 354 : 0.0761519 arcsec, 0.0601297 arcsec, -36.2835 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 355 : 0.0761504 arcsec, 0.0601287 arcsec, -36.2833 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 356 : 0.0761492 arcsec, 0.0601277 arcsec, -36.2832 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 357 : 0.0761478 arcsec, 0.0601264 arcsec, -36.2834 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 358 : 0.0761464 arcsec, 0.0601254 arcsec, -36.2834 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 359 : 0.0761448 arcsec, 0.0601239 arcsec, -36.2838 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 360 : 0.0761432 arcsec, 0.0601225 arcsec, -36.2839 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 361 : 0.076142 arcsec, 0.0601214 arcsec, -36.2841 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 362 : 0.0761406 arcsec, 0.0601201 arcsec, -36.2846 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 363 : 0.0761391 arcsec, 0.0601187 arcsec, -36.285 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 364 : 0.0761379 arcsec, 0.0601175 arcsec, -36.2853 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 365 : 0.0761366 arcsec, 0.0601164 arcsec, -36.2853 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 366 : 0.076135 arcsec, 0.060115 arcsec, -36.2856 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 367 : 0.0761336 arcsec, 0.0601139 arcsec, -36.2856 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 368 : 0.0761322 arcsec, 0.0601129 arcsec, -36.286 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 369 : 0.0761309 arcsec, 0.0601117 arcsec, -36.2861 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 370 : 0.0761295 arcsec, 0.0601105 arcsec, -36.2864 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 371 : 0.0761282 arcsec, 0.0601093 arcsec, -36.2868 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 372 : 0.0761269 arcsec, 0.0601081 arcsec, -36.2872 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 373 : 0.0761255 arcsec, 0.0601069 arcsec, -36.2875 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 374 : 0.0761242 arcsec, 0.0601058 arcsec, -36.2874 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 375 : 0.0761228 arcsec, 0.0601044 arcsec, -36.2878 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 376 : 0.0761212 arcsec, 0.0601031 arcsec, -36.2878 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 377 : 0.0761196 arcsec, 0.0601017 arcsec, -36.2882 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 378 : 0.0761182 arcsec, 0.0601005 arcsec, -36.2884 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 379 : 0.0761167 arcsec, 0.0600992 arcsec, -36.2884 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 380 : 0.0761152 arcsec, 0.060098 arcsec, -36.2886 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 381 : 0.0761138 arcsec, 0.0600968 arcsec, -36.2889 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 382 : 0.0761123 arcsec, 0.0600957 arcsec, -36.2887 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 383 : 0.0761107 arcsec, 0.0600944 arcsec, -36.2889 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 384 : 0.0761093 arcsec, 0.0600933 arcsec, -36.2891 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 385 : 0.0761081 arcsec, 0.0600922 arcsec, -36.2895 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 386 : 0.0761068 arcsec, 0.0600909 arcsec, -36.2901 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 387 : 0.0761056 arcsec, 0.0600895 arcsec, -36.2907 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 388 : 0.0761042 arcsec, 0.0600882 arcsec, -36.2908 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 389 : 0.0761029 arcsec, 0.060087 arcsec, -36.291 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 390 : 0.0761018 arcsec, 0.0600861 arcsec, -36.2909 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 391 : 0.0761006 arcsec, 0.0600848 arcsec, -36.2912 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 392 : 0.076099 arcsec, 0.0600833 arcsec, -36.2914 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 393 : 0.0760974 arcsec, 0.060082 arcsec, -36.2914 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 394 : 0.076096 arcsec, 0.0600805 arcsec, -36.2917 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 395 : 0.0760947 arcsec, 0.0600793 arcsec, -36.2919 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 396 : 0.0760933 arcsec, 0.060078 arcsec, -36.2921 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 397 : 0.0760918 arcsec, 0.0600767 arcsec, -36.2922 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 398 : 0.0760904 arcsec, 0.0600757 arcsec, -36.2921 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 399 : 0.0760886 arcsec, 0.0600742 arcsec, -36.2923 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 400 : 0.0760872 arcsec, 0.060073 arcsec, -36.2924 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 401 : 0.0760858 arcsec, 0.0600721 arcsec, -36.2924 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 402 : 0.0760845 arcsec, 0.0600709 arcsec, -36.2928 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 403 : 0.076083 arcsec, 0.0600696 arcsec, -36.2928 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 404 : 0.0760816 arcsec, 0.0600683 arcsec, -36.2929 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 405 : 0.0760801 arcsec, 0.060067 arcsec, -36.2932 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 406 : 0.0760788 arcsec, 0.0600659 arcsec, -36.2932 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 407 : 0.0760775 arcsec, 0.0600648 arcsec, -36.2934 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 408 : 0.0760759 arcsec, 0.0600634 arcsec, -36.2935 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 409 : 0.0760743 arcsec, 0.0600619 arcsec, -36.2936 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 410 : 0.0760729 arcsec, 0.0600609 arcsec, -36.2933 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 411 : 0.0760719 arcsec, 0.06006 arcsec, -36.2942 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 412 : 0.0760702 arcsec, 0.0600586 arcsec, -36.2938 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 413 : 0.0760688 arcsec, 0.0600574 arcsec, -36.294 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 414 : 0.0760674 arcsec, 0.0600562 arcsec, -36.2943 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 415 : 0.0760661 arcsec, 0.0600549 arcsec, -36.2944 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 416 : 0.0760647 arcsec, 0.0600539 arcsec, -36.2944 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 417 : 0.0760633 arcsec, 0.0600529 arcsec, -36.2944 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 418 : 0.0760617 arcsec, 0.0600513 arcsec, -36.2946 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 419 : 0.0760604 arcsec, 0.0600501 arcsec, -36.2946 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 420 : 0.0760592 arcsec, 0.0600491 arcsec, -36.2949 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 421 : 0.0760579 arcsec, 0.0600481 arcsec, -36.2951 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 422 : 0.0760564 arcsec, 0.0600469 arcsec, -36.2949 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 423 : 0.0760552 arcsec, 0.0600457 arcsec, -36.2948 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 424 : 0.0760539 arcsec, 0.0600446 arcsec, -36.295 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 425 : 0.0760525 arcsec, 0.0600435 arcsec, -36.2952 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 426 : 0.0760513 arcsec, 0.0600423 arcsec, -36.2956 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 427 : 0.0760499 arcsec, 0.0600412 arcsec, -36.2958 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 428 : 0.0760486 arcsec, 0.0600399 arcsec, -36.2962 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 429 : 0.0760473 arcsec, 0.0600389 arcsec, -36.2962 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 430 : 0.076046 arcsec, 0.0600377 arcsec, -36.2964 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 431 : 0.0760447 arcsec, 0.0600365 arcsec, -36.2968 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 432 : 0.0760434 arcsec, 0.0600353 arcsec, -36.297 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 433 : 0.076042 arcsec, 0.060034 arcsec, -36.2973 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 434 : 0.0760407 arcsec, 0.0600329 arcsec, -36.2974 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 435 : 0.0760393 arcsec, 0.0600318 arcsec, -36.2976 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 436 : 0.076038 arcsec, 0.0600307 arcsec, -36.2978 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 437 : 0.0760367 arcsec, 0.0600295 arcsec, -36.2984 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 438 : 0.0760353 arcsec, 0.0600283 arcsec, -36.2988 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 439 : 0.0760339 arcsec, 0.0600272 arcsec, -36.299 deg
    2019-11-22 02:51:45	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 440 : 0.0760326 arcsec, 0.060026 arcsec, -36.2994 deg
    2019-11-22 02:51:46	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 441 : 0.0760313 arcsec, 0.0600249 arcsec, -36.2996 deg
    2019-11-22 02:51:46	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 442 : 0.0760301 arcsec, 0.0600239 arcsec, -36.3 deg
    2019-11-22 02:51:46	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 443 : 0.0760286 arcsec, 0.0600227 arcsec, -36.3001 deg
    2019-11-22 02:51:46	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 444 : 0.0760269 arcsec, 0.0600214 arcsec, -36.3 deg
    2019-11-22 02:51:46	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 445 : 0.0760255 arcsec, 0.0600202 arcsec, -36.3001 deg
    2019-11-22 02:51:46	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 446 : 0.0760242 arcsec, 0.0600192 arcsec, -36.3 deg
    2019-11-22 02:51:46	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 447 : 0.0760233 arcsec, 0.0600182 arcsec, -36.3008 deg
    2019-11-22 02:51:46	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 448 : 0.0760218 arcsec, 0.0600168 arcsec, -36.3005 deg
    2019-11-22 02:51:46	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 449 : 0.0760203 arcsec, 0.0600156 arcsec, -36.3008 deg
    2019-11-22 02:51:46	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 450 : 0.076019 arcsec, 0.0600143 arcsec, -36.3011 deg
    2019-11-22 02:51:46	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 451 : 0.0760172 arcsec, 0.0600128 arcsec, -36.3012 deg
    2019-11-22 02:51:46	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 452 : 0.0760158 arcsec, 0.0600117 arcsec, -36.3013 deg
    2019-11-22 02:51:46	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 453 : 0.0760143 arcsec, 0.0600104 arcsec, -36.3014 deg
    2019-11-22 02:51:46	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 454 : 0.0760129 arcsec, 0.0600092 arcsec, -36.3013 deg
    2019-11-22 02:51:46	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 455 : 0.0760114 arcsec, 0.0600081 arcsec, -36.3012 deg
    2019-11-22 02:51:46	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 456 : 0.0760101 arcsec, 0.060007 arcsec, -36.3014 deg
    2019-11-22 02:51:46	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 457 : 0.0760088 arcsec, 0.0600059 arcsec, -36.3017 deg
    2019-11-22 02:51:46	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 458 : 0.0760074 arcsec, 0.0600049 arcsec, -36.3018 deg
    2019-11-22 02:51:46	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 459 : 0.0760061 arcsec, 0.0600036 arcsec, -36.302 deg
    2019-11-22 02:51:46	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 460 : 0.0760047 arcsec, 0.0600024 arcsec, -36.302 deg
    2019-11-22 02:51:46	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 461 : 0.0760034 arcsec, 0.0600012 arcsec, -36.3022 deg
    2019-11-22 02:51:46	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 462 : 0.0760021 arcsec, 0.0600001 arcsec, -36.3023 deg
    2019-11-22 02:51:46	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 463 : 0.0760009 arcsec, 0.0599988 arcsec, -36.3026 deg
    2019-11-22 02:51:46	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 464 : 0.0759996 arcsec, 0.0599977 arcsec, -36.3026 deg
    2019-11-22 02:51:46	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 465 : 0.0759983 arcsec, 0.0599966 arcsec, -36.3029 deg
    2019-11-22 02:51:46	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 466 : 0.0759967 arcsec, 0.0599953 arcsec, -36.3033 deg
    2019-11-22 02:51:46	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 467 : 0.0759955 arcsec, 0.059994 arcsec, -36.3038 deg
    2019-11-22 02:51:46	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 468 : 0.0759943 arcsec, 0.0599929 arcsec, -36.3041 deg
    2019-11-22 02:51:46	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 469 : 0.0759929 arcsec, 0.0599919 arcsec, -36.3042 deg
    2019-11-22 02:51:46	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 470 : 0.0759916 arcsec, 0.059991 arcsec, -36.304 deg
    2019-11-22 02:51:46	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 471 : 0.0759903 arcsec, 0.0599896 arcsec, -36.3044 deg
    2019-11-22 02:51:46	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 472 : 0.0759892 arcsec, 0.0599884 arcsec, -36.3047 deg
    2019-11-22 02:51:46	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 473 : 0.0759879 arcsec, 0.0599873 arcsec, -36.3051 deg
    2019-11-22 02:51:46	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 474 : 0.0759865 arcsec, 0.0599862 arcsec, -36.305 deg
    2019-11-22 02:51:46	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 475 : 0.0759852 arcsec, 0.0599849 arcsec, -36.3051 deg
    2019-11-22 02:51:46	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 476 : 0.0759841 arcsec, 0.0599839 arcsec, -36.3047 deg
    2019-11-22 02:51:46	INFO	tclean::::casa	Result tclean: {}
    2019-11-22 02:51:46	INFO	tclean::::casa	Task tclean complete. Start time: 2019-11-21 20:45:26.891530 End time: 2019-11-21 20:51:45.788565
    2019-11-22 02:51:46	INFO	tclean::::casa	##### End Task: tclean               #####
    2019-11-22 02:51:46	INFO	tclean::::casa	##########################################
    2019-11-22 02:51:46	INFO	exportfits::::casa	##########################################
    2019-11-22 02:51:46	INFO	exportfits::::casa	##### Begin Task: exportfits         #####
    2019-11-22 02:51:46	INFO	exportfits::::casa	exportfits( imagename='bb3.ci10/sci.image', fitsimage='bb3.ci10/sci.fits', velocity=False, optical=False, bitpix=-32, minpix=0, maxpix=-1, overwrite=True, dropstokes=False, stokeslast=True, history=True, dropdeg=False )
    2019-11-22 02:51:46	INFO	exportfits::ImageFactory::toFITS	Applying mask of name 'mask0'
    2019-11-22 02:51:46	INFO	exportfits::ImageFitsConverter::ImageHeaderToFITS 	Truncating miscinfo field useweightimage to useweigh
    2019-11-22 02:51:47	INFO	exportfits::::casa	Result exportfits: None
    2019-11-22 02:51:47	INFO	exportfits::::casa	Task exportfits complete. Start time: 2019-11-21 20:51:45.792150 End time: 2019-11-21 20:51:46.627902
    2019-11-22 02:51:47	INFO	exportfits::::casa	##### End Task: exportfits           #####
    2019-11-22 02:51:47	INFO	exportfits::::casa	##########################################
    2019-11-22 02:51:49	INFO	tclean::::casa	##########################################
    2019-11-22 02:51:49	INFO	tclean::::casa	##### Begin Task: tclean             #####
    2019-11-22 02:51:49	INFO	tclean::::casa	tclean( vis=['bb2.ms.mfs', 'bb4.ms.mfs'], selectdata=True, field='', spw='', timerange='', uvrange='', antenna='', scan='', observation='', intent='', datacolumn='data', imagename='bb24.cont/sci', imsize=[256, 256], cell=0.01, phasecenter='', stokes='I', projection='SIN', startmodel='', specmode='mfs', reffreq='', nchan=-1, start=0, width=1, outframe='LSRK', veltype='radio', restfreq=[], interpolation='nearest', perchanweightdensity=True, gridder='standard', facets=1, psfphasecenter='', chanchunks=1, wprojplanes=1, vptable='', mosweight=True, aterm=True, psterm=False, wbawp=True, conjbeams=False, cfcache='', usepointing=False, computepastep=360.0, rotatepastep=360.0, pointingoffsetsigdev=0.0, pblimit=0.2, normtype='flatnoise', deconvolver='hogbom', scales=[], nterms=2, smallscalebias=0.0, restoration=True, restoringbeam='', pbcor=False, outlierfile='', weighting='briggs', robust=1.0, noise='1.0Jy', npixels=0, uvtaper=[''], niter=0, gain=0.1, threshold=0.0, nsigma=0.0, cycleniter=-1, cyclefactor=1.0, minpsffraction=0.05, maxpsffraction=0.8, interactive=False, usemask='user', mask='', pbmask=0.0, sidelobethreshold=3.0, noisethreshold=5.0, lownoisethreshold=1.5, negativethreshold=0.0, smoothfactor=1.0, minbeamfrac=0.3, cutthreshold=0.01, growiterations=75, dogrowprune=True, minpercentchange=-1.0, verbose=False, fastnoise=True, restart=True, savemodel='none', calcres=True, calcpsf=True, parallel=False )
    2019-11-22 02:51:49	INFO	tclean::::casa	Verifying Input Parameters
    2019-11-22 02:51:49	INFO	SynthesisImagerVi2::selectData 	MS : bb2.ms.mfs | [Opened in readonly mode]
    2019-11-22 02:51:49	INFO	SynthesisImagerVi2::selectData 	  NRows selected : 276124
    2019-11-22 02:51:49	INFO	SynthesisImagerVi2::selectData 	MS : bb4.ms.mfs | [Opened in readonly mode]
    2019-11-22 02:51:49	INFO	SynthesisImagerVi2::selectData 	  NRows selected : 276124
    2019-11-22 02:51:49	INFO	SynthesisImagerVi2::defineImage 	Define image coordinates for [bb24.cont/sci] : 
    2019-11-22 02:51:49	INFO	SynthesisImagerVi2::defineImage 	Impars : start 0
    2019-11-22 02:51:49	INFO	SynthesisImagerVi2::defineImage 	Shape : [256, 256, 1, 1]Spectral : [1.4859e+11] at [0] with increment [1.55665e+10]
    2019-11-22 02:51:49	INFO	SynthesisImagerVi2::defineImage 	Set Gridding options for [bb24.cont/sci] with ftmachine : gridft
    2019-11-22 02:51:49	INFO	SynthesisImagerVi2::weight() 	Set imaging weights : Briggs weighting: sidelobes will be suppressed over full image
    2019-11-22 02:51:51	INFO	VisSetUtil::VisImagingWeight() 	Normal robustness, robust = 1
    2019-11-22 02:51:51	INFO	task_tclean::SynthesisDeconvolver::setupDeconvolution 	Set Deconvolution Options for [bb24.cont/sci] : hogbom
    2019-11-22 02:51:51	INFO	SynthesisImager::makePSF 	----------------------------------------------------------- Make PSF ---------------------------------------------
    2019-11-22 02:51:53	INFO	SIImageStore::calcSensitivity 	[bb24.cont/sci] Theoretical sensitivity (Jy/bm):2.07588e-06 
    2019-11-22 02:51:53	INFO	SIImageStore::printBeamSet 	Beam : 0.0722381 arcsec, 0.0574362 arcsec, -34.4769 deg
    2019-11-22 02:51:53	INFO	task_tclean::SynthesisImagerVi2::makePrimaryBeam 	vi2 : Evaluating Primary Beam model onto image grid(s)
    2019-11-22 02:51:54	INFO	task_tclean::SynthesisImager::executeMajorCycle 	----------------------------------------------------------- Run (Last) Major Cycle 1 -------------------------------------
    2019-11-22 02:51:57	INFO	task_tclean::SDAlgorithmBase::restore 	[bb24.cont/sci] : Restoring model image.
    2019-11-22 02:51:57	WARN	task_tclean::SIImageStore::restore (file casa-source/code/synthesis/ImagerObjects/SIImageStore.cc, line 2068)	Restoring with an empty model image. Only residuals will be processed to form the output restored image.
    2019-11-22 02:51:57	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 0 : 0.0722381 arcsec, 0.0574362 arcsec, -34.4769 deg
    2019-11-22 02:51:57	INFO	tclean::::casa	Result tclean: {}
    2019-11-22 02:51:57	INFO	tclean::::casa	Task tclean complete. Start time: 2019-11-21 20:51:48.846634 End time: 2019-11-21 20:51:56.613341
    2019-11-22 02:51:57	INFO	tclean::::casa	##### End Task: tclean               #####
    2019-11-22 02:51:57	INFO	tclean::::casa	##########################################
    2019-11-22 02:51:57	INFO	exportfits::::casa	##########################################
    2019-11-22 02:51:57	INFO	exportfits::::casa	##### Begin Task: exportfits         #####
    2019-11-22 02:51:57	INFO	exportfits::::casa	exportfits( imagename='bb24.cont/sci.image', fitsimage='bb24.cont/sci.fits', velocity=False, optical=False, bitpix=-32, minpix=0, maxpix=-1, overwrite=True, dropstokes=False, stokeslast=True, history=True, dropdeg=False )
    2019-11-22 02:51:57	INFO	exportfits::ImageFactory::toFITS	Applying mask of name 'mask0'
    2019-11-22 02:51:57	INFO	exportfits::ImageFitsConverter::ImageHeaderToFITS 	Truncating miscinfo field useweightimage to useweigh
    2019-11-22 02:51:57	INFO	exportfits::::casa	Result exportfits: None
    2019-11-22 02:51:57	INFO	exportfits::::casa	Task exportfits complete. Start time: 2019-11-21 20:51:56.617581 End time: 2019-11-21 20:51:56.629515
    2019-11-22 02:51:57	INFO	exportfits::::casa	##### End Task: exportfits           #####
    2019-11-22 02:51:57	INFO	exportfits::::casa	##########################################


2013.1.00059.S+2017.1.01045.S
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: ipython3

    demo_dir='/Users/Rui/Documents/Workspace/projects/GMaKE/examples/data/bx610/alma/band4/'
    if  'hypersion' or 'mini' in socket.gethostname() :
        os.chdir(demo_dir)
    setLogfile(demo_dir+'/'+'demo_bx610_imaging.log')
    
    # use the cycle5 phasecenter as the imaging center (closer to the target)
    invert(['../2017.1.01045.S/bb1.ms','../2013.1.00059.S/bb3.ms'],'co43/sci',cell=0.01,imsize=[256,256],datacolumn='data',start=0,nchan=397)
    invert(['../2017.1.01045.S/bb3.ms','../2013.1.00059.S/bb1.ms'],'ci10/sci',cell=0.01,imsize=[256,256],datacolumn='data',start=82)
    ms_cont=['../2017.1.01045.S/bb2.ms.mfs','../2017.1.01045.S/bb4.ms.mfs','../2013.1.00059.S/bb2.ms.mfs','../2013.1.00059.S/bb4.ms.mfs']
    invert(ms_cont,'cont/sci',cell=0.01,imsize=[256,256],datacolumn='data',specmode='mfs')


.. parsed-literal::

    2019-11-19 18:39:13	INFO	tclean::::casa	##########################################
    2019-11-19 18:39:13	INFO	tclean::::casa	##### Begin Task: tclean             #####
    2019-11-19 18:39:13	INFO	tclean::::casa	tclean( vis=['../2017.1.01045.S/bb1.ms', '../2013.1.00059.S/bb3.ms'], selectdata=True, field='', spw='', timerange='', uvrange='', antenna='', scan='', observation='', intent='', datacolumn='data', imagename='co43/sci', imsize=[256, 256], cell=0.01, phasecenter='', stokes='I', projection='SIN', startmodel='', specmode='cube', reffreq='', nchan=397, start=0, width=1, outframe='LSRK', veltype='radio', restfreq=[], interpolation='nearest', perchanweightdensity=True, gridder='standard', facets=1, psfphasecenter='', chanchunks=1, wprojplanes=1, vptable='', mosweight=True, aterm=True, psterm=False, wbawp=True, conjbeams=False, cfcache='', usepointing=False, computepastep=360.0, rotatepastep=360.0, pointingoffsetsigdev=0.0, pblimit=0.2, normtype='flatnoise', deconvolver='hogbom', scales=[], nterms=2, smallscalebias=0.0, restoration=True, restoringbeam='', pbcor=False, outlierfile='', weighting='briggs', robust=1.0, noise='1.0Jy', npixels=0, uvtaper=[''], niter=0, gain=0.1, threshold=0.0, nsigma=0.0, cycleniter=-1, cyclefactor=1.0, minpsffraction=0.05, maxpsffraction=0.8, interactive=False, usemask='user', mask='', pbmask=0.0, sidelobethreshold=3.0, noisethreshold=5.0, lownoisethreshold=1.5, negativethreshold=0.0, smoothfactor=1.0, minbeamfrac=0.3, cutthreshold=0.01, growiterations=75, dogrowprune=True, minpercentchange=-1.0, verbose=False, fastnoise=True, restart=True, savemodel='none', calcres=True, calcpsf=True, parallel=False )
    2019-11-19 18:39:13	INFO	tclean::::casa	Verifying Input Parameters
    2019-11-19 18:39:13	INFO	SynthesisImagerVi2::selectData 	MS : ../2017.1.01045.S/bb1.ms | [Opened in readonly mode]
    2019-11-19 18:39:13	INFO	SynthesisImagerVi2::selectData 	  NRows selected : 275794
    2019-11-19 18:39:13	INFO	SynthesisImagerVi2::selectData 	MS : ../2013.1.00059.S/bb3.ms | [Opened in readonly mode]
    2019-11-19 18:39:13	INFO	SynthesisImagerVi2::selectData 	  NRows selected : 70778
    2019-11-19 18:39:14	INFO	SynthesisImagerVi2::defineImage 	Define image coordinates for [co43/sci] : 
    2019-11-19 18:39:14	INFO	MSTransformRegridder::calcChanFreqs	 phaseCenter='Direction: [0.973286, -0.0588582, 0.221923]'  *** Encountered negative channel widths in input spectral window.
    2019-11-19 18:39:14	INFO	MSTransformRegridder::calcChanFreqs	 Channels equidistant in freq
    2019-11-19 18:39:14	INFO	MSTransformRegridder::calcChanFreqs+	 Central frequency (in output frame) = 1.43723e+11 Hz
    2019-11-19 18:39:14	INFO	MSTransformRegridder::calcChanFreqs+	 Channel central frequency is decreasing with increasing channel number.
    2019-11-19 18:39:14	INFO	MSTransformRegridder::calcChanFreqs+	 Width of central channel (in output frame) = 3.90647e+06 Hz
    2019-11-19 18:39:14	INFO	MSTransformRegridder::calcChanFreqs+	 Number of channels = 397
    2019-11-19 18:39:14	INFO	MSTransformRegridder::calcChanFreqs+	 Total width of SPW (in output frame) = 1.55087e+09 Hz
    2019-11-19 18:39:14	INFO	MSTransformRegridder::calcChanFreqs+	 Lower edge = 1.42947e+11 Hz, upper edge = 1.44498e+11 Hz
    2019-11-19 18:39:14	INFO	SynthesisImagerVi2::defineImage 	Impars : start 0
    2019-11-19 18:39:14	INFO	SynthesisImagerVi2::defineImage 	Shape : [256, 256, 1, 397]Spectral : [1.44496e+11] at [0] with increment [-3.90647e+06]
    2019-11-19 18:39:14	INFO	SynthesisImagerVi2::defineImage 	Set Gridding options for [co43/sci] with ftmachine : gridft
    2019-11-19 18:39:14	INFO	SynthesisImagerVi2::weight() 	Set imaging weights : Briggs weighting: sidelobes will be suppressed over full image
    2019-11-19 18:39:14	INFO	SynthesisImagerVi2::weight() 	Doing spectral cube Briggs weighting formula --  norm
    2019-11-19 18:39:14	INFO	SynthesisImager::tuneSelectData 	Tuning frequency data selection to match image spectral coordinates
    2019-11-19 18:39:14	INFO	SynthesisImagerVi2::selectData 	MS : ../2017.1.01045.S/bb1.ms | [Opened in readonly mode]
    2019-11-19 18:39:14	INFO	SynthesisImagerVi2::selectData 	  NRows selected : 275794
    2019-11-19 18:39:14	INFO	SynthesisImagerVi2::selectData 	MS : ../2013.1.00059.S/bb3.ms | [Opened in readonly mode]
    2019-11-19 18:39:14	INFO	SynthesisImagerVi2::selectData 	  NRows selected : 70778
    2019-11-19 18:39:14	INFO	task_tclean::SynthesisDeconvolver::setupDeconvolution 	Set Deconvolution Options for [co43/sci] : hogbom
    2019-11-19 18:39:14	INFO	SynthesisImager::makePSF 	----------------------------------------------------------- Make PSF ---------------------------------------------
    
    0%....10....20....30....40....50....60....70....80....90....100%
    2019-11-19 18:42:15	INFO	SIImageStore::calcSensitivity 	[co43/sci] Theoretical sensitivity (Jy/bm):c0:5.3686e-05 c1:5.36859e-05 c2:5.36859e-05 c3:5.36859e-05 c4:5.3686e-05 c5:5.3686e-05 c6:5.3686e-05 c7:5.3686e-05 c8:5.3686e-05 c9:5.36861e-05 c10:5.3686e-05 c11:5.3686e-05 c12:5.36861e-05 c13:5.36861e-05 c14:5.36861e-05 c15:5.36861e-05 c16:5.36862e-05 c17:5.36862e-05 c18:5.36864e-05 c19:5.36862e-05 c20:5.36862e-05 c21:5.36862e-05 c22:5.36862e-05 c23:5.36862e-05 c24:5.3686e-05 c25:5.3686e-05 c26:5.3686e-05 c27:5.3686e-05 c28:5.36861e-05 c29:5.36861e-05 c30:5.36862e-05 c31:5.36861e-05 c32:5.36862e-05 c33:5.3686e-05 c34:5.3686e-05 c35:5.3686e-05 c36:5.36861e-05 c37:5.36861e-05 c38:5.36862e-05 c39:5.36861e-05 c40:5.36861e-05 c41:5.36862e-05 c42:5.36861e-05 c43:5.36863e-05 c44:5.36862e-05 c45:5.3686e-05 c46:5.3686e-05 c47:5.3686e-05 c48:5.36861e-05 c49:5.3686e-05 c50:5.36861e-05 c51:5.3686e-05 c52:5.3686e-05 c53:5.3686e-05 c54:5.36859e-05 c55:5.36857e-05 c56:5.36856e-05 c57:5.36856e-05 c58:5.36856e-05 c59:5.36856e-05 c60:5.36854e-05 c61:5.36854e-05 c62:5.36854e-05 c63:5.36855e-05 c64:5.36855e-05 c65:5.36857e-05 c66:5.36857e-05 c67:5.36857e-05 c68:5.36857e-05 c69:5.36857e-05 c70:5.36857e-05 c71:5.36857e-05 c72:5.36857e-05 c73:5.36856e-05 c74:5.36857e-05 c75:5.36857e-05 c76:5.36854e-05 c77:5.36854e-05 c78:5.36853e-05 c79:5.36853e-05 c80:5.06955e-05 c81:5.06955e-05 c82:5.06955e-05 c83:5.06955e-05 c84:5.06955e-05 c85:5.06955e-05 c86:5.06955e-05 c87:5.06955e-05 c88:5.06953e-05 c89:5.06954e-05 c90:5.06953e-05 c91:5.06953e-05 c92:5.06953e-05 c93:5.06953e-05 c94:5.06953e-05 c95:5.06953e-05 c96:5.06953e-05 c97:5.06953e-05 c98:5.06954e-05 c99:5.06953e-05 c100:5.06951e-05 c101:5.06952e-05 c102:5.06951e-05 c103:5.06951e-05 c104:5.06951e-05 c105:5.06951e-05 c106:5.06952e-05 c107:5.06952e-05 c108:5.06951e-05 c109:5.06951e-05 c110:5.06951e-05 c111:5.0695e-05 c112:5.06951e-05 c113:5.06951e-05 c114:5.06951e-05 c115:5.0695e-05 c116:5.06949e-05 c117:5.0695e-05 c118:5.06948e-05 c119:5.06948e-05 c120:5.06948e-05 c121:5.06948e-05 c122:5.06948e-05 c123:5.06947e-05 c124:5.06947e-05 c125:5.06947e-05 c126:5.06947e-05 c127:5.06947e-05 c128:5.06948e-05 c129:5.06948e-05 c130:5.06948e-05 c131:5.06948e-05 c132:5.06948e-05 c133:5.06948e-05 c134:5.06948e-05 c135:5.06948e-05 c136:5.06947e-05 c137:5.06947e-05 c138:5.06947e-05 c139:5.06948e-05 c140:5.06947e-05 c141:5.06946e-05 c142:5.06947e-05 c143:5.06946e-05 c144:5.06945e-05 c145:5.06945e-05 c146:5.06945e-05 c147:5.06946e-05 c148:5.06945e-05 c149:5.06946e-05 c150:5.06946e-05 c151:5.06946e-05 c152:5.06946e-05 c153:5.06946e-05 c154:5.06945e-05 c155:5.06944e-05 c156:5.06945e-05 c157:5.06943e-05 c158:5.06942e-05 c159:5.06942e-05 c160:5.06942e-05 c161:5.06942e-05 c162:5.06942e-05 c163:5.06942e-05 c164:5.06942e-05 c165:5.06942e-05 c166:5.06943e-05 c167:5.06943e-05 c168:5.06944e-05 c169:5.06943e-05 c170:5.06943e-05 c171:5.06943e-05 c172:5.06943e-05 c173:5.06943e-05 c174:5.06942e-05 c175:5.06942e-05 c176:5.06942e-05 c177:5.06941e-05 c178:5.0694e-05 c179:5.06938e-05 c180:5.06939e-05 c181:5.06939e-05 c182:5.06938e-05 c183:5.06938e-05 c184:5.06938e-05 c185:5.06938e-05 c186:5.06938e-05 c187:5.06938e-05 c188:5.06938e-05 c189:5.06938e-05 c190:5.06938e-05 c191:5.06937e-05 c192:5.06938e-05 c193:5.06938e-05 c194:5.06938e-05 c195:5.06937e-05 c196:5.06936e-05 c197:5.06935e-05 c198:5.06935e-05 c199:5.06935e-05 c200:5.06934e-05 c201:5.06933e-05 c202:5.06934e-05 c203:5.06934e-05 c204:5.06934e-05 c205:5.06935e-05 c206:5.06934e-05 c207:5.06934e-05 c208:5.06935e-05 c209:5.06934e-05 c210:5.06935e-05 c211:5.06935e-05 c212:5.06934e-05 c213:5.06934e-05 c214:5.06933e-05 c215:5.06933e-05 c216:5.06933e-05 c217:5.06932e-05 c218:5.06933e-05 c219:5.06933e-05 c220:5.06933e-05 c221:5.06933e-05 c222:5.06933e-05 c223:5.06933e-05 c224:5.06933e-05 c225:5.06933e-05 c226:5.06933e-05 c227:5.06933e-05 c228:5.06933e-05 c229:5.06933e-05 c230:5.06933e-05 c231:5.06933e-05 c232:5.06933e-05 c233:5.06933e-05 c234:5.06932e-05 c235:5.06932e-05 c236:5.06931e-05 c237:5.06932e-05 c238:5.06932e-05 c239:5.06932e-05 c240:5.06932e-05 c241:5.06932e-05 c242:5.06932e-05 c243:5.06932e-05 c244:5.06933e-05 c245:5.06933e-05 c246:5.06932e-05 c247:5.06932e-05 c248:5.06933e-05 c249:5.06933e-05 c250:5.06933e-05 c251:5.06933e-05 c252:5.06933e-05 c253:5.06934e-05 c254:5.06934e-05 c255:5.06934e-05 c256:5.06934e-05 c257:5.06934e-05 c258:5.06933e-05 c259:5.06932e-05 c260:5.06932e-05 c261:5.06932e-05 c262:5.06931e-05 c263:5.06931e-05 c264:5.0693e-05 c265:5.0693e-05 c266:5.0693e-05 c267:5.0693e-05 c268:5.06929e-05 c269:5.06929e-05 c270:5.0693e-05 c271:5.06929e-05 c272:5.06929e-05 c273:5.06927e-05 c274:5.06927e-05 c275:5.06927e-05 c276:5.06927e-05 c277:5.06927e-05 c278:5.06926e-05 c279:5.06926e-05 c280:5.06925e-05 c281:5.06925e-05 c282:5.06925e-05 c283:5.06925e-05 c284:5.06925e-05 c285:5.06925e-05 c286:5.06925e-05 c287:5.06925e-05 c288:5.06925e-05 c289:5.06923e-05 c290:5.06924e-05 c291:5.06924e-05 c292:5.06923e-05 c293:5.06923e-05 c294:5.06923e-05 c295:5.06921e-05 c296:5.06922e-05 c297:5.06921e-05 c298:5.06921e-05 c299:5.06922e-05 c300:5.06922e-05 c301:5.06922e-05 c302:5.06922e-05 c303:5.06921e-05 c304:5.06921e-05 c305:5.06921e-05 c306:5.0692e-05 c307:5.06921e-05 c308:5.06921e-05 c309:5.06921e-05 c310:5.0692e-05 c311:5.0692e-05 c312:5.06919e-05 c313:5.06919e-05 c314:5.06919e-05 c315:5.0692e-05 c316:5.06919e-05 c317:5.06919e-05 c318:5.0692e-05 c319:5.0692e-05 c320:5.06919e-05 c321:5.06919e-05 c322:5.06919e-05 c323:5.06919e-05 c324:5.06918e-05 c325:5.06917e-05 c326:5.06917e-05 c327:5.06918e-05 c328:5.06918e-05 c329:5.06918e-05 c330:5.06917e-05 c331:5.06917e-05 c332:5.06917e-05 c333:5.06917e-05 c334:5.06917e-05 c335:5.06917e-05 c336:5.06917e-05 c337:5.06918e-05 c338:5.06918e-05 c339:5.06918e-05 c340:5.06917e-05 c341:5.06917e-05 c342:5.06916e-05 c343:5.06916e-05 c344:5.06916e-05 c345:5.06916e-05 c346:5.06916e-05 c347:5.06917e-05 c348:5.06916e-05 c349:5.06916e-05 c350:5.06917e-05 c351:5.06917e-05 c352:5.06917e-05 c353:5.06917e-05 c354:5.06917e-05 c355:5.06917e-05 c356:5.06916e-05 c357:5.06916e-05 c358:5.06916e-05 c359:5.06916e-05 c360:5.06916e-05 c361:5.06916e-05 c362:5.06916e-05 c363:5.06916e-05 c364:5.06916e-05 c365:5.06915e-05 c366:5.06916e-05 c367:5.06916e-05 c368:5.06916e-05 c369:5.06916e-05 c370:5.06915e-05 c371:5.06916e-05 c372:5.06915e-05 c373:5.06915e-05 c374:5.06915e-05 c375:5.06915e-05 c376:5.06914e-05 c377:5.06914e-05 c378:5.06913e-05 c379:5.06914e-05 c380:5.06913e-05 c381:5.06913e-05 c382:5.06912e-05 c383:5.06912e-05 c384:5.0691e-05 c385:5.06909e-05 c386:5.06908e-05 c387:5.06907e-05 c388:5.06907e-05 c389:5.06907e-05 c390:5.06907e-05 c391:5.06906e-05 c392:5.06907e-05 c393:5.06905e-05 c394:5.06905e-05 c395:5.06905e-05 c396:5.06905e-05 
    2019-11-19 18:42:17	INFO	SIImageStore::printBeamSet 	Restoring Beams 
    2019-11-19 18:42:17	INFO	SIImageStore::printBeamSet +	Pol   Type Chan         Freq     Vel
    2019-11-19 18:42:17	INFO	SIImageStore::printBeamSet +	  I    Max  396 1.429494e+11 206835.46    0.0861 arcsec x    0.0746 arcsec pa=-26.6055 deg
    2019-11-19 18:42:17	INFO	SIImageStore::printBeamSet +	  I    Min    1 1.444925e+11 205832.04    0.0000 arcsec x    0.0000 arcsec pa=  0.0000 deg
    2019-11-19 18:42:17	INFO	SIImageStore::printBeamSet +	  I Median  198 1.437229e+11 206332.48    0.0858 arcsec x    0.0744 arcsec pa=-26.6658 deg
    2019-11-19 18:42:17	INFO	task_tclean::SynthesisImagerVi2::makePrimaryBeam 	vi2 : Evaluating Primary Beam model onto image grid(s)
    2019-11-19 18:42:20	INFO	task_tclean::SynthesisImager::executeMajorCycle 	----------------------------------------------------------- Run (Last) Major Cycle 1 -------------------------------------
    
    0%....10....20....30....40....50....60....70....80....90....100%
    2019-11-19 18:45:05	INFO	task_tclean::SDAlgorithmBase::restore 	[co43/sci] : Restoring model image.
    2019-11-19 18:45:05	WARN	task_tclean::SIImageStore::restore (file casa-source/code/synthesis/ImagerObjects/SIImageStore.cc, line 2068)	Restoring with an empty model image. Only residuals will be processed to form the output restored image.
    2019-11-19 18:45:05	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 0 : 0.0804214 arcsec, 0.0641638 arcsec, -32.3913 deg
    2019-11-19 18:45:05	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 1 : 0.0804233 arcsec, 0.0641653 arcsec, -32.3911 deg
    2019-11-19 18:45:05	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 2 : 0.0804248 arcsec, 0.0641667 arcsec, -32.3905 deg
    2019-11-19 18:45:05	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 3 : 0.0804264 arcsec, 0.0641682 arcsec, -32.3899 deg
    2019-11-19 18:45:05	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 4 : 0.0804279 arcsec, 0.0641695 arcsec, -32.3898 deg
    2019-11-19 18:45:05	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 5 : 0.0804293 arcsec, 0.0641709 arcsec, -32.3896 deg
    2019-11-19 18:45:05	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 6 : 0.0804309 arcsec, 0.0641724 arcsec, -32.3892 deg
    2019-11-19 18:45:05	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 7 : 0.0804327 arcsec, 0.0641737 arcsec, -32.3889 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 8 : 0.0804343 arcsec, 0.064175 arcsec, -32.3887 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 9 : 0.080436 arcsec, 0.0641762 arcsec, -32.3885 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 10 : 0.0804376 arcsec, 0.0641777 arcsec, -32.388 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 11 : 0.0804393 arcsec, 0.0641791 arcsec, -32.3878 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 12 : 0.080441 arcsec, 0.0641804 arcsec, -32.3874 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 13 : 0.0804427 arcsec, 0.0641817 arcsec, -32.387 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 14 : 0.0804442 arcsec, 0.0641832 arcsec, -32.3868 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 15 : 0.0804457 arcsec, 0.0641844 arcsec, -32.3866 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 16 : 0.0804477 arcsec, 0.0641859 arcsec, -32.3857 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 17 : 0.080449 arcsec, 0.0641872 arcsec, -32.3859 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 18 : 0.0804506 arcsec, 0.0641897 arcsec, -32.3866 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 19 : 0.0804523 arcsec, 0.0641901 arcsec, -32.3852 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 20 : 0.0804539 arcsec, 0.0641917 arcsec, -32.3848 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 21 : 0.0804556 arcsec, 0.0641931 arcsec, -32.3846 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 22 : 0.0804572 arcsec, 0.0641944 arcsec, -32.3844 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 23 : 0.0804588 arcsec, 0.0641957 arcsec, -32.3842 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 24 : 0.0804609 arcsec, 0.0641973 arcsec, -32.384 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 25 : 0.0804624 arcsec, 0.0641987 arcsec, -32.3836 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 26 : 0.080464 arcsec, 0.0642 arcsec, -32.3835 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 27 : 0.0804656 arcsec, 0.0642012 arcsec, -32.3832 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 28 : 0.080467 arcsec, 0.0642026 arcsec, -32.3827 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 29 : 0.0804685 arcsec, 0.0642039 arcsec, -32.3823 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 30 : 0.08047 arcsec, 0.0642053 arcsec, -32.382 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 31 : 0.0804717 arcsec, 0.0642069 arcsec, -32.3815 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 32 : 0.0804733 arcsec, 0.0642083 arcsec, -32.3815 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 33 : 0.0804752 arcsec, 0.0642099 arcsec, -32.381 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 34 : 0.0804769 arcsec, 0.0642112 arcsec, -32.3805 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 35 : 0.0804783 arcsec, 0.0642125 arcsec, -32.3799 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 36 : 0.0804798 arcsec, 0.0642139 arcsec, -32.3794 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 37 : 0.0804814 arcsec, 0.0642152 arcsec, -32.3792 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 38 : 0.080483 arcsec, 0.0642173 arcsec, -32.3791 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 39 : 0.0804844 arcsec, 0.0642181 arcsec, -32.3784 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 40 : 0.0804861 arcsec, 0.0642194 arcsec, -32.378 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 41 : 0.0804876 arcsec, 0.0642208 arcsec, -32.3777 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 42 : 0.0804894 arcsec, 0.0642225 arcsec, -32.3771 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 43 : 0.0804911 arcsec, 0.0642247 arcsec, -32.3764 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 44 : 0.0804926 arcsec, 0.0642251 arcsec, -32.3764 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 45 : 0.0804946 arcsec, 0.0642268 arcsec, -32.3764 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 46 : 0.0804962 arcsec, 0.064228 arcsec, -32.376 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 47 : 0.080498 arcsec, 0.0642296 arcsec, -32.3757 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 48 : 0.0804996 arcsec, 0.0642311 arcsec, -32.3752 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 49 : 0.0805012 arcsec, 0.0642326 arcsec, -32.3746 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 50 : 0.0805028 arcsec, 0.0642341 arcsec, -32.3742 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 51 : 0.0805044 arcsec, 0.0642355 arcsec, -32.3739 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 52 : 0.0805059 arcsec, 0.064237 arcsec, -32.3734 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 53 : 0.0805074 arcsec, 0.0642384 arcsec, -32.3732 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 54 : 0.0805093 arcsec, 0.0642398 arcsec, -32.3731 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 55 : 0.0805112 arcsec, 0.0642414 arcsec, -32.3728 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 56 : 0.0805129 arcsec, 0.0642428 arcsec, -32.3726 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 57 : 0.0805145 arcsec, 0.0642442 arcsec, -32.3724 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 58 : 0.0805161 arcsec, 0.0642456 arcsec, -32.372 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 59 : 0.0805178 arcsec, 0.0642469 arcsec, -32.372 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 60 : 0.0805196 arcsec, 0.0642485 arcsec, -32.3717 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 61 : 0.0805213 arcsec, 0.0642498 arcsec, -32.3716 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 62 : 0.080523 arcsec, 0.0642512 arcsec, -32.3712 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 63 : 0.0805245 arcsec, 0.0642527 arcsec, -32.3709 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 64 : 0.0805261 arcsec, 0.0642541 arcsec, -32.3705 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 65 : 0.0805275 arcsec, 0.0642553 arcsec, -32.3704 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 66 : 0.0805292 arcsec, 0.0642567 arcsec, -32.3702 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 67 : 0.0805308 arcsec, 0.064258 arcsec, -32.37 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 68 : 0.0805325 arcsec, 0.0642595 arcsec, -32.3696 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 69 : 0.080534 arcsec, 0.0642609 arcsec, -32.3691 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 70 : 0.0805356 arcsec, 0.0642624 arcsec, -32.369 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 71 : 0.0805374 arcsec, 0.0642639 arcsec, -32.3687 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 72 : 0.0805389 arcsec, 0.0642652 arcsec, -32.3683 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 73 : 0.0805404 arcsec, 0.0642668 arcsec, -32.3677 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 74 : 0.0805421 arcsec, 0.0642681 arcsec, -32.3675 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 75 : 0.0805437 arcsec, 0.0642694 arcsec, -32.3668 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 76 : 0.0805457 arcsec, 0.0642712 arcsec, -32.3662 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 77 : 0.0805473 arcsec, 0.0642725 arcsec, -32.366 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 78 : 0.0805492 arcsec, 0.064274 arcsec, -32.3655 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 79 : 0.0805509 arcsec, 0.0642753 arcsec, -32.3653 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 80 : 0.0855514 arcsec, 0.0742172 arcsec, -26.699 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 81 : 0.0855531 arcsec, 0.0742185 arcsec, -26.6988 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 82 : 0.0855548 arcsec, 0.0742198 arcsec, -26.6982 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 83 : 0.0855564 arcsec, 0.0742211 arcsec, -26.6979 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 84 : 0.0855581 arcsec, 0.0742223 arcsec, -26.6977 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 85 : 0.0855599 arcsec, 0.0742237 arcsec, -26.6975 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 86 : 0.0855615 arcsec, 0.0742251 arcsec, -26.6972 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 87 : 0.0855632 arcsec, 0.0742264 arcsec, -26.6968 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 88 : 0.0855652 arcsec, 0.074228 arcsec, -26.6965 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 89 : 0.0855668 arcsec, 0.0742294 arcsec, -26.6962 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 90 : 0.0855687 arcsec, 0.0742307 arcsec, -26.696 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 91 : 0.0855705 arcsec, 0.0742321 arcsec, -26.6956 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 92 : 0.0855722 arcsec, 0.0742334 arcsec, -26.6956 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 93 : 0.0855738 arcsec, 0.0742346 arcsec, -26.6953 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 94 : 0.0855755 arcsec, 0.074236 arcsec, -26.6951 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 95 : 0.0855776 arcsec, 0.0742376 arcsec, -26.695 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 96 : 0.0855791 arcsec, 0.0742388 arcsec, -26.6945 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 97 : 0.0855807 arcsec, 0.0742401 arcsec, -26.6944 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 98 : 0.0855823 arcsec, 0.0742414 arcsec, -26.6943 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 99 : 0.0855841 arcsec, 0.0742429 arcsec, -26.6942 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 100 : 0.0855861 arcsec, 0.0742445 arcsec, -26.6937 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 101 : 0.0855879 arcsec, 0.0742458 arcsec, -26.6933 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 102 : 0.0855899 arcsec, 0.0742473 arcsec, -26.6931 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 103 : 0.0855916 arcsec, 0.0742486 arcsec, -26.6928 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 104 : 0.0855932 arcsec, 0.0742499 arcsec, -26.6925 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 105 : 0.085595 arcsec, 0.0742512 arcsec, -26.6922 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 106 : 0.0855966 arcsec, 0.0742525 arcsec, -26.692 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 107 : 0.0855984 arcsec, 0.0742538 arcsec, -26.6916 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 108 : 0.0856002 arcsec, 0.0742554 arcsec, -26.691 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 109 : 0.0856019 arcsec, 0.0742567 arcsec, -26.6906 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 110 : 0.0856037 arcsec, 0.0742581 arcsec, -26.6903 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 111 : 0.0856055 arcsec, 0.0742595 arcsec, -26.6904 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 112 : 0.0856071 arcsec, 0.0742607 arcsec, -26.6902 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 113 : 0.0856089 arcsec, 0.0742619 arcsec, -26.6898 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 114 : 0.0856106 arcsec, 0.0742634 arcsec, -26.6892 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 115 : 0.0856125 arcsec, 0.0742649 arcsec, -26.6888 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 116 : 0.0856142 arcsec, 0.0742662 arcsec, -26.6887 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 117 : 0.0856157 arcsec, 0.0742673 arcsec, -26.6886 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 118 : 0.0856176 arcsec, 0.0742689 arcsec, -26.6881 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 119 : 0.0856194 arcsec, 0.0742704 arcsec, -26.6875 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 120 : 0.085621 arcsec, 0.0742716 arcsec, -26.6875 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 121 : 0.0856227 arcsec, 0.0742729 arcsec, -26.6872 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 122 : 0.0856244 arcsec, 0.0742742 arcsec, -26.687 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 123 : 0.0856263 arcsec, 0.0742757 arcsec, -26.6866 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 124 : 0.085628 arcsec, 0.074277 arcsec, -26.6862 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 125 : 0.0856296 arcsec, 0.0742783 arcsec, -26.6858 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 126 : 0.0856313 arcsec, 0.0742796 arcsec, -26.6853 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 127 : 0.085633 arcsec, 0.074281 arcsec, -26.6849 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 128 : 0.0856345 arcsec, 0.0742823 arcsec, -26.6847 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 129 : 0.0856363 arcsec, 0.0742836 arcsec, -26.6843 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 130 : 0.085638 arcsec, 0.0742851 arcsec, -26.6835 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 131 : 0.0856398 arcsec, 0.0742864 arcsec, -26.6833 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 132 : 0.0856415 arcsec, 0.0742877 arcsec, -26.683 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 133 : 0.0856432 arcsec, 0.074289 arcsec, -26.683 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 134 : 0.0856449 arcsec, 0.0742904 arcsec, -26.6828 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 135 : 0.0856467 arcsec, 0.0742918 arcsec, -26.6826 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 136 : 0.0856484 arcsec, 0.0742931 arcsec, -26.6825 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 137 : 0.0856501 arcsec, 0.0742945 arcsec, -26.6823 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 138 : 0.0856518 arcsec, 0.0742958 arcsec, -26.6822 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 139 : 0.0856537 arcsec, 0.0742972 arcsec, -26.6819 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 140 : 0.0856553 arcsec, 0.0742985 arcsec, -26.6816 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 141 : 0.085657 arcsec, 0.0742998 arcsec, -26.6812 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 142 : 0.0856586 arcsec, 0.0743011 arcsec, -26.681 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 143 : 0.0856604 arcsec, 0.0743025 arcsec, -26.6809 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 144 : 0.0856624 arcsec, 0.074304 arcsec, -26.6804 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 145 : 0.085664 arcsec, 0.0743052 arcsec, -26.6803 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 146 : 0.0856657 arcsec, 0.0743064 arcsec, -26.6798 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 147 : 0.0856673 arcsec, 0.0743079 arcsec, -26.6793 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 148 : 0.085669 arcsec, 0.0743093 arcsec, -26.679 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 149 : 0.0856707 arcsec, 0.0743107 arcsec, -26.6786 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 150 : 0.0856724 arcsec, 0.0743119 arcsec, -26.6783 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 151 : 0.0856741 arcsec, 0.0743132 arcsec, -26.6781 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 152 : 0.0856758 arcsec, 0.0743146 arcsec, -26.6781 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 153 : 0.0856775 arcsec, 0.0743159 arcsec, -26.6781 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 154 : 0.0856795 arcsec, 0.0743175 arcsec, -26.6778 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 155 : 0.0856814 arcsec, 0.0743189 arcsec, -26.6774 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 156 : 0.0856829 arcsec, 0.0743202 arcsec, -26.6771 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 157 : 0.0856849 arcsec, 0.074322 arcsec, -26.6769 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 158 : 0.0856869 arcsec, 0.0743235 arcsec, -26.6766 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 159 : 0.0856886 arcsec, 0.0743248 arcsec, -26.6766 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 160 : 0.0856903 arcsec, 0.0743263 arcsec, -26.6763 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 161 : 0.085692 arcsec, 0.0743276 arcsec, -26.6758 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 162 : 0.0856937 arcsec, 0.074329 arcsec, -26.6756 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 163 : 0.0856954 arcsec, 0.0743303 arcsec, -26.6754 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 164 : 0.0856969 arcsec, 0.0743315 arcsec, -26.6752 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 165 : 0.0856985 arcsec, 0.0743328 arcsec, -26.6749 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 166 : 0.0857002 arcsec, 0.0743341 arcsec, -26.6744 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 167 : 0.085702 arcsec, 0.0743354 arcsec, -26.6741 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 168 : 0.0857034 arcsec, 0.0743365 arcsec, -26.6737 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 169 : 0.0857054 arcsec, 0.074338 arcsec, -26.6735 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 170 : 0.0857071 arcsec, 0.0743392 arcsec, -26.6733 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 171 : 0.0857088 arcsec, 0.0743404 arcsec, -26.6728 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 172 : 0.0857105 arcsec, 0.0743417 arcsec, -26.6729 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 173 : 0.0857121 arcsec, 0.0743429 arcsec, -26.6724 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 174 : 0.085714 arcsec, 0.0743444 arcsec, -26.6724 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 175 : 0.0857156 arcsec, 0.0743457 arcsec, -26.6721 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 176 : 0.0857174 arcsec, 0.0743471 arcsec, -26.6718 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 177 : 0.0857192 arcsec, 0.0743484 arcsec, -26.6719 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 178 : 0.0857212 arcsec, 0.0743501 arcsec, -26.6714 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 179 : 0.0857231 arcsec, 0.0743516 arcsec, -26.6713 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 180 : 0.0857248 arcsec, 0.0743529 arcsec, -26.6709 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 181 : 0.0857265 arcsec, 0.0743542 arcsec, -26.6705 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 182 : 0.0857284 arcsec, 0.0743557 arcsec, -26.6703 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 183 : 0.0857301 arcsec, 0.074357 arcsec, -26.6701 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 184 : 0.0857318 arcsec, 0.0743582 arcsec, -26.6699 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 185 : 0.0857335 arcsec, 0.0743595 arcsec, -26.6697 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 186 : 0.0857353 arcsec, 0.0743609 arcsec, -26.6695 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 187 : 0.0857371 arcsec, 0.0743622 arcsec, -26.6692 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 188 : 0.0857388 arcsec, 0.0743636 arcsec, -26.6685 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 189 : 0.0857405 arcsec, 0.0743648 arcsec, -26.6685 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 190 : 0.0857421 arcsec, 0.0743662 arcsec, -26.6683 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 191 : 0.0857439 arcsec, 0.0743678 arcsec, -26.6679 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 192 : 0.0857454 arcsec, 0.074369 arcsec, -26.6676 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 193 : 0.0857471 arcsec, 0.0743703 arcsec, -26.6674 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 194 : 0.0857489 arcsec, 0.0743717 arcsec, -26.667 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 195 : 0.0857507 arcsec, 0.0743732 arcsec, -26.6668 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 196 : 0.0857526 arcsec, 0.0743747 arcsec, -26.6664 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 197 : 0.0857545 arcsec, 0.074376 arcsec, -26.666 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 198 : 0.0857562 arcsec, 0.0743773 arcsec, -26.6658 deg
    2019-11-19 18:45:06	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 199 : 0.085758 arcsec, 0.0743787 arcsec, -26.6654 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 200 : 0.0857597 arcsec, 0.0743801 arcsec, -26.6651 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 201 : 0.0857616 arcsec, 0.0743816 arcsec, -26.6647 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 202 : 0.0857633 arcsec, 0.0743829 arcsec, -26.6643 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 203 : 0.0857649 arcsec, 0.0743842 arcsec, -26.664 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 204 : 0.0857665 arcsec, 0.0743855 arcsec, -26.6637 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 205 : 0.085768 arcsec, 0.0743867 arcsec, -26.6632 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 206 : 0.0857698 arcsec, 0.074388 arcsec, -26.6628 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 207 : 0.0857715 arcsec, 0.0743893 arcsec, -26.6625 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 208 : 0.0857733 arcsec, 0.0743906 arcsec, -26.6624 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 209 : 0.0857752 arcsec, 0.074392 arcsec, -26.6622 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 210 : 0.0857767 arcsec, 0.0743934 arcsec, -26.6615 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 211 : 0.0857783 arcsec, 0.0743946 arcsec, -26.6614 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 212 : 0.0857801 arcsec, 0.074396 arcsec, -26.661 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 213 : 0.0857819 arcsec, 0.0743973 arcsec, -26.6608 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 214 : 0.0857837 arcsec, 0.0743988 arcsec, -26.661 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 215 : 0.0857855 arcsec, 0.0744001 arcsec, -26.6605 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 216 : 0.0857873 arcsec, 0.0744015 arcsec, -26.6606 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 217 : 0.085789 arcsec, 0.0744028 arcsec, -26.6603 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 218 : 0.0857907 arcsec, 0.0744042 arcsec, -26.6599 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 219 : 0.0857924 arcsec, 0.0744055 arcsec, -26.6595 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 220 : 0.085794 arcsec, 0.0744068 arcsec, -26.659 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 221 : 0.0857958 arcsec, 0.0744083 arcsec, -26.6586 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 222 : 0.0857974 arcsec, 0.0744097 arcsec, -26.6583 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 223 : 0.0857991 arcsec, 0.074411 arcsec, -26.6577 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 224 : 0.0858008 arcsec, 0.0744123 arcsec, -26.6574 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 225 : 0.0858026 arcsec, 0.0744137 arcsec, -26.6572 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 226 : 0.0858043 arcsec, 0.0744149 arcsec, -26.6568 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 227 : 0.0858059 arcsec, 0.0744163 arcsec, -26.6564 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 228 : 0.0858076 arcsec, 0.0744175 arcsec, -26.6563 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 229 : 0.0858093 arcsec, 0.0744189 arcsec, -26.6562 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 230 : 0.0858111 arcsec, 0.0744203 arcsec, -26.656 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 231 : 0.0858128 arcsec, 0.0744216 arcsec, -26.6558 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 232 : 0.0858146 arcsec, 0.0744229 arcsec, -26.6556 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 233 : 0.0858162 arcsec, 0.0744242 arcsec, -26.6554 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 234 : 0.085818 arcsec, 0.0744256 arcsec, -26.6551 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 235 : 0.0858196 arcsec, 0.074427 arcsec, -26.6546 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 236 : 0.0858214 arcsec, 0.0744283 arcsec, -26.654 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 237 : 0.085823 arcsec, 0.0744296 arcsec, -26.6536 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 238 : 0.0858248 arcsec, 0.074431 arcsec, -26.6535 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 239 : 0.0858265 arcsec, 0.0744322 arcsec, -26.6533 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 240 : 0.0858282 arcsec, 0.0744335 arcsec, -26.6531 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 241 : 0.0858301 arcsec, 0.074435 arcsec, -26.653 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 242 : 0.0858316 arcsec, 0.0744363 arcsec, -26.6529 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 243 : 0.0858333 arcsec, 0.0744377 arcsec, -26.6526 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 244 : 0.0858349 arcsec, 0.074439 arcsec, -26.6521 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 245 : 0.0858366 arcsec, 0.0744402 arcsec, -26.6519 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 246 : 0.0858383 arcsec, 0.0744416 arcsec, -26.6515 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 247 : 0.0858399 arcsec, 0.0744429 arcsec, -26.6511 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 248 : 0.0858416 arcsec, 0.0744443 arcsec, -26.6506 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 249 : 0.0858433 arcsec, 0.0744456 arcsec, -26.6502 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 250 : 0.0858449 arcsec, 0.074447 arcsec, -26.65 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 251 : 0.0858467 arcsec, 0.0744483 arcsec, -26.6497 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 252 : 0.0858485 arcsec, 0.0744496 arcsec, -26.6494 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 253 : 0.0858501 arcsec, 0.0744509 arcsec, -26.6491 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 254 : 0.0858517 arcsec, 0.0744522 arcsec, -26.6486 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 255 : 0.0858535 arcsec, 0.0744536 arcsec, -26.6485 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 256 : 0.0858552 arcsec, 0.0744549 arcsec, -26.6484 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 257 : 0.0858569 arcsec, 0.0744562 arcsec, -26.6482 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 258 : 0.0858589 arcsec, 0.0744577 arcsec, -26.648 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 259 : 0.0858607 arcsec, 0.0744592 arcsec, -26.6476 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 260 : 0.0858625 arcsec, 0.0744604 arcsec, -26.6472 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 261 : 0.0858642 arcsec, 0.0744618 arcsec, -26.6467 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 262 : 0.085866 arcsec, 0.0744632 arcsec, -26.6463 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 263 : 0.0858678 arcsec, 0.0744645 arcsec, -26.6459 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 264 : 0.0858698 arcsec, 0.074466 arcsec, -26.6457 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 265 : 0.0858715 arcsec, 0.0744673 arcsec, -26.6452 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 266 : 0.0858732 arcsec, 0.0744687 arcsec, -26.6451 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 267 : 0.085875 arcsec, 0.0744701 arcsec, -26.6449 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 268 : 0.0858767 arcsec, 0.0744715 arcsec, -26.6444 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 269 : 0.0858785 arcsec, 0.0744728 arcsec, -26.6442 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 270 : 0.0858801 arcsec, 0.0744741 arcsec, -26.6439 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 271 : 0.0858818 arcsec, 0.0744754 arcsec, -26.6439 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 272 : 0.0858834 arcsec, 0.0744766 arcsec, -26.6435 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 273 : 0.0858856 arcsec, 0.0744783 arcsec, -26.6431 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 274 : 0.0858874 arcsec, 0.0744797 arcsec, -26.6427 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 275 : 0.0858892 arcsec, 0.074481 arcsec, -26.6426 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 276 : 0.0858909 arcsec, 0.0744824 arcsec, -26.6424 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 277 : 0.0858926 arcsec, 0.0744837 arcsec, -26.642 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 278 : 0.0858952 arcsec, 0.0744855 arcsec, -26.6413 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 279 : 0.0858962 arcsec, 0.0744867 arcsec, -26.6411 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 280 : 0.0858981 arcsec, 0.0744881 arcsec, -26.641 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 281 : 0.0858997 arcsec, 0.0744894 arcsec, -26.641 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 282 : 0.0859014 arcsec, 0.0744908 arcsec, -26.6404 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 283 : 0.0859031 arcsec, 0.0744922 arcsec, -26.6402 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 284 : 0.0859047 arcsec, 0.0744934 arcsec, -26.6397 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 285 : 0.0859065 arcsec, 0.0744948 arcsec, -26.6396 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 286 : 0.0859082 arcsec, 0.0744961 arcsec, -26.6393 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 287 : 0.08591 arcsec, 0.0744977 arcsec, -26.6389 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 288 : 0.0859117 arcsec, 0.074499 arcsec, -26.6387 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 289 : 0.0859137 arcsec, 0.0745005 arcsec, -26.6383 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 290 : 0.0859154 arcsec, 0.0745019 arcsec, -26.6377 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 291 : 0.085917 arcsec, 0.0745031 arcsec, -26.6375 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 292 : 0.0859189 arcsec, 0.0745046 arcsec, -26.6371 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 293 : 0.0859208 arcsec, 0.0745062 arcsec, -26.6369 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 294 : 0.0859225 arcsec, 0.0745075 arcsec, -26.6368 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 295 : 0.0859244 arcsec, 0.0745091 arcsec, -26.6363 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 296 : 0.0859261 arcsec, 0.0745104 arcsec, -26.6363 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 297 : 0.0859279 arcsec, 0.0745119 arcsec, -26.6365 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 298 : 0.0859296 arcsec, 0.0745132 arcsec, -26.6362 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 299 : 0.0859313 arcsec, 0.0745146 arcsec, -26.6358 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 300 : 0.0859329 arcsec, 0.0745159 arcsec, -26.6355 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 301 : 0.0859346 arcsec, 0.0745174 arcsec, -26.6351 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 302 : 0.0859363 arcsec, 0.0745187 arcsec, -26.6349 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 303 : 0.0859382 arcsec, 0.0745202 arcsec, -26.6345 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 304 : 0.0859399 arcsec, 0.0745215 arcsec, -26.6342 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 305 : 0.0859417 arcsec, 0.0745229 arcsec, -26.6337 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 306 : 0.0859437 arcsec, 0.0745245 arcsec, -26.6335 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 307 : 0.0859452 arcsec, 0.0745257 arcsec, -26.6332 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 308 : 0.0859469 arcsec, 0.0745272 arcsec, -26.6327 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 309 : 0.0859485 arcsec, 0.0745285 arcsec, -26.6323 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 310 : 0.0859502 arcsec, 0.0745299 arcsec, -26.632 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 311 : 0.085952 arcsec, 0.0745313 arcsec, -26.6315 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 312 : 0.0859538 arcsec, 0.0745327 arcsec, -26.6314 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 313 : 0.0859555 arcsec, 0.074534 arcsec, -26.6311 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 314 : 0.0859572 arcsec, 0.0745354 arcsec, -26.6307 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 315 : 0.085959 arcsec, 0.0745368 arcsec, -26.6303 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 316 : 0.0859606 arcsec, 0.0745381 arcsec, -26.6299 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 317 : 0.0859623 arcsec, 0.0745395 arcsec, -26.6296 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 318 : 0.085964 arcsec, 0.0745407 arcsec, -26.6292 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 319 : 0.0859656 arcsec, 0.074542 arcsec, -26.6291 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 320 : 0.0859675 arcsec, 0.0745436 arcsec, -26.6286 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 321 : 0.0859692 arcsec, 0.0745449 arcsec, -26.6283 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 322 : 0.085971 arcsec, 0.0745462 arcsec, -26.6281 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 323 : 0.0859727 arcsec, 0.0745475 arcsec, -26.6279 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 324 : 0.0859746 arcsec, 0.074549 arcsec, -26.6275 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 325 : 0.0859764 arcsec, 0.0745504 arcsec, -26.6274 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 326 : 0.0859782 arcsec, 0.0745517 arcsec, -26.627 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 327 : 0.0859798 arcsec, 0.0745532 arcsec, -26.6265 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 328 : 0.0859815 arcsec, 0.0745545 arcsec, -26.6262 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 329 : 0.0859832 arcsec, 0.0745559 arcsec, -26.6257 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 330 : 0.085985 arcsec, 0.0745574 arcsec, -26.625 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 331 : 0.0859868 arcsec, 0.0745587 arcsec, -26.625 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 332 : 0.0859884 arcsec, 0.0745601 arcsec, -26.6246 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 333 : 0.0859901 arcsec, 0.0745615 arcsec, -26.6245 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 334 : 0.0859917 arcsec, 0.0745628 arcsec, -26.6243 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 335 : 0.0859933 arcsec, 0.0745641 arcsec, -26.6238 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 336 : 0.085995 arcsec, 0.0745653 arcsec, -26.6236 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 337 : 0.0859967 arcsec, 0.0745666 arcsec, -26.623 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 338 : 0.0859984 arcsec, 0.074568 arcsec, -26.6225 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 339 : 0.0860001 arcsec, 0.0745692 arcsec, -26.6223 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 340 : 0.086002 arcsec, 0.0745708 arcsec, -26.6216 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 341 : 0.0860037 arcsec, 0.074572 arcsec, -26.6213 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 342 : 0.0860056 arcsec, 0.0745737 arcsec, -26.6208 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 343 : 0.0860074 arcsec, 0.0745751 arcsec, -26.6206 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 344 : 0.086009 arcsec, 0.0745764 arcsec, -26.6204 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 345 : 0.0860107 arcsec, 0.0745777 arcsec, -26.6202 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 346 : 0.0860125 arcsec, 0.0745791 arcsec, -26.6199 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 347 : 0.0860144 arcsec, 0.0745809 arcsec, -26.619 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 348 : 0.086016 arcsec, 0.0745817 arcsec, -26.6199 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 349 : 0.0860176 arcsec, 0.0745831 arcsec, -26.6196 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 350 : 0.0860193 arcsec, 0.0745843 arcsec, -26.6195 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 351 : 0.086021 arcsec, 0.0745856 arcsec, -26.619 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 352 : 0.0860227 arcsec, 0.074587 arcsec, -26.6189 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 353 : 0.0860244 arcsec, 0.0745884 arcsec, -26.6186 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 354 : 0.086026 arcsec, 0.0745897 arcsec, -26.618 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 355 : 0.0860278 arcsec, 0.0745912 arcsec, -26.6174 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 356 : 0.0860295 arcsec, 0.0745925 arcsec, -26.617 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 357 : 0.0860314 arcsec, 0.074594 arcsec, -26.6169 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 358 : 0.0860331 arcsec, 0.0745953 arcsec, -26.6167 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 359 : 0.0860349 arcsec, 0.0745966 arcsec, -26.6165 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 360 : 0.0860366 arcsec, 0.074598 arcsec, -26.6162 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 361 : 0.0860384 arcsec, 0.0745992 arcsec, -26.6159 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 362 : 0.0860401 arcsec, 0.0746004 arcsec, -26.616 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 363 : 0.0860418 arcsec, 0.0746018 arcsec, -26.6158 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 364 : 0.0860436 arcsec, 0.0746031 arcsec, -26.6155 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 365 : 0.0860455 arcsec, 0.0746045 arcsec, -26.6151 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 366 : 0.0860472 arcsec, 0.0746057 arcsec, -26.6147 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 367 : 0.0860489 arcsec, 0.074607 arcsec, -26.6144 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 368 : 0.0860507 arcsec, 0.0746084 arcsec, -26.6141 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 369 : 0.0860523 arcsec, 0.0746097 arcsec, -26.6137 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 370 : 0.0860542 arcsec, 0.0746112 arcsec, -26.6138 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 371 : 0.0860559 arcsec, 0.0746124 arcsec, -26.6134 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 372 : 0.0860576 arcsec, 0.0746138 arcsec, -26.6131 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 373 : 0.0860596 arcsec, 0.0746153 arcsec, -26.6127 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 374 : 0.0860614 arcsec, 0.0746168 arcsec, -26.6127 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 375 : 0.0860632 arcsec, 0.0746182 arcsec, -26.6124 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 376 : 0.086065 arcsec, 0.0746197 arcsec, -26.6119 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 377 : 0.0860668 arcsec, 0.0746211 arcsec, -26.6113 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 378 : 0.0860686 arcsec, 0.0746226 arcsec, -26.6108 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 379 : 0.0860702 arcsec, 0.0746238 arcsec, -26.6105 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 380 : 0.0860721 arcsec, 0.0746253 arcsec, -26.6102 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 381 : 0.0860738 arcsec, 0.0746266 arcsec, -26.61 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 382 : 0.0860758 arcsec, 0.074628 arcsec, -26.6097 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 383 : 0.0860775 arcsec, 0.0746294 arcsec, -26.6098 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 384 : 0.0860797 arcsec, 0.0746311 arcsec, -26.6095 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 385 : 0.0860816 arcsec, 0.0746328 arcsec, -26.609 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 386 : 0.0860833 arcsec, 0.0746341 arcsec, -26.609 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 387 : 0.0860853 arcsec, 0.0746358 arcsec, -26.6088 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 388 : 0.0860871 arcsec, 0.074637 arcsec, -26.6086 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 389 : 0.0860887 arcsec, 0.0746384 arcsec, -26.6082 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 390 : 0.0860904 arcsec, 0.0746397 arcsec, -26.6078 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 391 : 0.0860924 arcsec, 0.0746413 arcsec, -26.6074 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 392 : 0.0860939 arcsec, 0.0746425 arcsec, -26.6068 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 393 : 0.086096 arcsec, 0.0746441 arcsec, -26.6068 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 394 : 0.0860978 arcsec, 0.0746456 arcsec, -26.6062 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 395 : 0.0860994 arcsec, 0.0746469 arcsec, -26.6061 deg
    2019-11-19 18:45:07	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 396 : 0.0861013 arcsec, 0.0746484 arcsec, -26.6055 deg
    2019-11-19 18:45:08	INFO	tclean::::casa	Result tclean: {}
    2019-11-19 18:45:08	INFO	tclean::::casa	Task tclean complete. Start time: 2019-11-19 12:39:13.237733 End time: 2019-11-19 12:45:07.563565
    2019-11-19 18:45:08	INFO	tclean::::casa	##### End Task: tclean               #####
    2019-11-19 18:45:08	INFO	tclean::::casa	##########################################
    2019-11-19 18:45:08	INFO	exportfits::::casa	##########################################
    2019-11-19 18:45:08	INFO	exportfits::::casa	##### Begin Task: exportfits         #####
    2019-11-19 18:45:08	INFO	exportfits::::casa	exportfits( imagename='co43/sci.image', fitsimage='co43/sci.fits', velocity=False, optical=False, bitpix=-32, minpix=0, maxpix=-1, overwrite=True, dropstokes=False, stokeslast=True, history=True, dropdeg=False )
    2019-11-19 18:45:08	INFO	exportfits::ImageFactory::toFITS	Applying mask of name 'mask0'
    2019-11-19 18:45:08	INFO	exportfits::ImageFitsConverter::ImageHeaderToFITS 	Truncating miscinfo field useweightimage to useweigh
    2019-11-19 18:45:08	INFO	exportfits::::casa	Result exportfits: None
    2019-11-19 18:45:08	INFO	exportfits::::casa	Task exportfits complete. Start time: 2019-11-19 12:45:07.567373 End time: 2019-11-19 12:45:08.229071
    2019-11-19 18:45:08	INFO	exportfits::::casa	##### End Task: exportfits           #####
    2019-11-19 18:45:08	INFO	exportfits::::casa	##########################################
    2019-11-19 18:45:11	INFO	tclean::::casa	##########################################
    2019-11-19 18:45:11	INFO	tclean::::casa	##### Begin Task: tclean             #####
    2019-11-19 18:45:11	INFO	tclean::::casa	tclean( vis=['../2017.1.01045.S/bb3.ms', '../2013.1.00059.S/bb1.ms'], selectdata=True, field='', spw='', timerange='', uvrange='', antenna='', scan='', observation='', intent='', datacolumn='data', imagename='ci10/sci', imsize=[256, 256], cell=0.01, phasecenter='', stokes='I', projection='SIN', startmodel='', specmode='cube', reffreq='', nchan=-1, start=82, width=1, outframe='LSRK', veltype='radio', restfreq=[], interpolation='nearest', perchanweightdensity=True, gridder='standard', facets=1, psfphasecenter='', chanchunks=1, wprojplanes=1, vptable='', mosweight=True, aterm=True, psterm=False, wbawp=True, conjbeams=False, cfcache='', usepointing=False, computepastep=360.0, rotatepastep=360.0, pointingoffsetsigdev=0.0, pblimit=0.2, normtype='flatnoise', deconvolver='hogbom', scales=[], nterms=2, smallscalebias=0.0, restoration=True, restoringbeam='', pbcor=False, outlierfile='', weighting='briggs', robust=1.0, noise='1.0Jy', npixels=0, uvtaper=[''], niter=0, gain=0.1, threshold=0.0, nsigma=0.0, cycleniter=-1, cyclefactor=1.0, minpsffraction=0.05, maxpsffraction=0.8, interactive=False, usemask='user', mask='', pbmask=0.0, sidelobethreshold=3.0, noisethreshold=5.0, lownoisethreshold=1.5, negativethreshold=0.0, smoothfactor=1.0, minbeamfrac=0.3, cutthreshold=0.01, growiterations=75, dogrowprune=True, minpercentchange=-1.0, verbose=False, fastnoise=True, restart=True, savemodel='none', calcres=True, calcpsf=True, parallel=False )
    2019-11-19 18:45:11	INFO	tclean::::casa	Verifying Input Parameters
    2019-11-19 18:45:11	INFO	SynthesisImagerVi2::selectData 	MS : ../2017.1.01045.S/bb3.ms | [Opened in readonly mode]
    2019-11-19 18:45:11	INFO	SynthesisImagerVi2::selectData 	  NRows selected : 276124
    2019-11-19 18:45:11	INFO	SynthesisImagerVi2::selectData 	MS : ../2013.1.00059.S/bb1.ms | [Opened in readonly mode]
    2019-11-19 18:45:11	INFO	SynthesisImagerVi2::selectData 	  NRows selected : 69446
    2019-11-19 18:45:11	INFO	SynthesisImagerVi2::defineImage 	Define image coordinates for [ci10/sci] : 
    2019-11-19 18:45:11	INFO	MSTransformRegridder::calcChanFreqs	 phaseCenter='Direction: [0.973286, -0.0588582, 0.221923]'  Channels equidistant in freq
    2019-11-19 18:45:11	INFO	MSTransformRegridder::calcChanFreqs+	 Central frequency (in output frame) = 1.53769e+11 Hz
    2019-11-19 18:45:11	INFO	MSTransformRegridder::calcChanFreqs+	 Width of central channel (in output frame) = 3.90647e+06 Hz
    2019-11-19 18:45:11	INFO	MSTransformRegridder::calcChanFreqs+	 Number of channels = 395
    2019-11-19 18:45:11	INFO	MSTransformRegridder::calcChanFreqs+	 Total width of SPW (in output frame) = 1.54305e+09 Hz
    2019-11-19 18:45:11	INFO	MSTransformRegridder::calcChanFreqs+	 Lower edge = 1.52998e+11 Hz, upper edge = 1.54541e+11 Hz
    2019-11-19 18:45:11	INFO	SynthesisImagerVi2::defineImage 	Impars : start 82
    2019-11-19 18:45:11	INFO	SynthesisImagerVi2::defineImage 	Shape : [256, 256, 1, 395]Spectral : [1.53e+11] at [0] with increment [3.90647e+06]
    2019-11-19 18:45:11	INFO	SynthesisImagerVi2::defineImage 	Set Gridding options for [ci10/sci] with ftmachine : gridft
    2019-11-19 18:45:11	INFO	SynthesisImagerVi2::weight() 	Set imaging weights : Briggs weighting: sidelobes will be suppressed over full image
    2019-11-19 18:45:11	INFO	SynthesisImagerVi2::weight() 	Doing spectral cube Briggs weighting formula --  norm
    2019-11-19 18:45:11	INFO	SynthesisImager::tuneSelectData 	Tuning frequency data selection to match image spectral coordinates
    2019-11-19 18:45:11	INFO	SynthesisImagerVi2::selectData 	MS : ../2017.1.01045.S/bb3.ms | [Opened in readonly mode]
    2019-11-19 18:45:11	INFO	SynthesisImagerVi2::selectData 	  NRows selected : 276124
    2019-11-19 18:45:11	INFO	SynthesisImagerVi2::selectData 	MS : ../2013.1.00059.S/bb1.ms | [Opened in readonly mode]
    2019-11-19 18:45:11	INFO	SynthesisImagerVi2::selectData 	  NRows selected : 69446
    2019-11-19 18:45:11	INFO	task_tclean::SynthesisDeconvolver::setupDeconvolution 	Set Deconvolution Options for [ci10/sci] : hogbom
    2019-11-19 18:45:11	INFO	SynthesisImager::makePSF 	----------------------------------------------------------- Make PSF ---------------------------------------------
    
    0%....10....20....30....40....50....60....70....80....90....100%
    2019-11-19 18:48:01	INFO	SIImageStore::calcSensitivity 	[ci10/sci] Theoretical sensitivity (Jy/bm):c0:5.47664e-05 c1:5.47664e-05 c2:5.47665e-05 c3:5.47665e-05 c4:5.47665e-05 c5:5.47665e-05 c6:5.47666e-05 c7:5.47666e-05 c8:5.47666e-05 c9:5.47666e-05 c10:5.47665e-05 c11:5.47665e-05 c12:5.47665e-05 c13:5.47665e-05 c14:5.47665e-05 c15:5.47664e-05 c16:5.47665e-05 c17:5.47665e-05 c18:5.47667e-05 c19:5.47668e-05 c20:5.47668e-05 c21:5.47669e-05 c22:5.47669e-05 c23:5.4767e-05 c24:5.47671e-05 c25:5.47672e-05 c26:5.47672e-05 c27:5.47672e-05 c28:5.47672e-05 c29:5.47671e-05 c30:5.47672e-05 c31:5.47672e-05 c32:5.47671e-05 c33:5.47671e-05 c34:5.47672e-05 c35:5.47672e-05 c36:5.47671e-05 c37:5.47672e-05 c38:5.47672e-05 c39:5.47674e-05 c40:5.47675e-05 c41:5.47678e-05 c42:5.47678e-05 c43:5.47678e-05 c44:5.47678e-05 c45:5.47678e-05 c46:5.47678e-05 c47:5.4768e-05 c48:5.47682e-05 c49:5.47682e-05 c50:5.47682e-05 c51:5.47683e-05 c52:5.47685e-05 c53:5.47685e-05 c54:5.47686e-05 c55:5.47687e-05 c56:5.47687e-05 c57:5.47687e-05 c58:5.47687e-05 c59:5.47687e-05 c60:5.47688e-05 c61:5.47689e-05 c62:5.47689e-05 c63:5.4769e-05 c64:5.4769e-05 c65:5.4769e-05 c66:5.4769e-05 c67:5.4769e-05 c68:5.4769e-05 c69:5.4769e-05 c70:5.4769e-05 c71:5.4769e-05 c72:5.47689e-05 c73:5.4769e-05 c74:5.47689e-05 c75:5.4769e-05 c76:5.4769e-05 c77:5.4769e-05 c78:5.4769e-05 c79:5.4769e-05 c80:5.4769e-05 c81:5.4769e-05 c82:5.4769e-05 c83:5.4769e-05 c84:5.47691e-05 c85:5.47691e-05 c86:5.47692e-05 c87:5.47691e-05 c88:5.47692e-05 c89:5.47692e-05 c90:5.47692e-05 c91:5.47692e-05 c92:5.47692e-05 c93:5.47693e-05 c94:5.47695e-05 c95:5.47695e-05 c96:5.47695e-05 c97:5.47696e-05 c98:5.47696e-05 c99:5.47696e-05 c100:5.47696e-05 c101:5.47697e-05 c102:5.47697e-05 c103:5.47697e-05 c104:5.47697e-05 c105:5.47697e-05 c106:5.47697e-05 c107:5.47698e-05 c108:5.47698e-05 c109:5.47698e-05 c110:5.47698e-05 c111:5.47698e-05 c112:5.47698e-05 c113:5.47698e-05 c114:5.477e-05 c115:5.47699e-05 c116:5.47698e-05 c117:5.47698e-05 c118:5.47699e-05 c119:5.477e-05 c120:5.477e-05 c121:5.47701e-05 c122:5.47701e-05 c123:5.47701e-05 c124:5.47702e-05 c125:5.47701e-05 c126:5.47702e-05 c127:5.47702e-05 c128:5.47702e-05 c129:5.47702e-05 c130:5.47702e-05 c131:5.47702e-05 c132:5.47702e-05 c133:5.47703e-05 c134:5.47705e-05 c135:5.47706e-05 c136:5.47708e-05 c137:5.47709e-05 c138:5.4771e-05 c139:5.4771e-05 c140:5.47711e-05 c141:5.47711e-05 c142:5.47711e-05 c143:5.47711e-05 c144:5.47711e-05 c145:5.47712e-05 c146:5.47712e-05 c147:5.47712e-05 c148:5.47713e-05 c149:5.47713e-05 c150:5.47714e-05 c151:5.47714e-05 c152:5.47714e-05 c153:5.47715e-05 c154:5.47715e-05 c155:5.47715e-05 c156:5.47715e-05 c157:5.47715e-05 c158:5.47715e-05 c159:5.47715e-05 c160:5.47715e-05 c161:5.47716e-05 c162:5.47717e-05 c163:5.47717e-05 c164:5.47717e-05 c165:5.47717e-05 c166:5.47717e-05 c167:5.47718e-05 c168:5.47718e-05 c169:5.47718e-05 c170:5.47718e-05 c171:5.47717e-05 c172:5.47717e-05 c173:5.47717e-05 c174:5.47717e-05 c175:5.47717e-05 c176:5.47716e-05 c177:5.47717e-05 c178:5.47716e-05 c179:5.47716e-05 c180:5.47716e-05 c181:5.47717e-05 c182:5.47717e-05 c183:5.47719e-05 c184:5.47718e-05 c185:5.47719e-05 c186:5.47718e-05 c187:5.47719e-05 c188:5.4772e-05 c189:5.4772e-05 c190:5.4772e-05 c191:5.4772e-05 c192:5.47721e-05 c193:5.47721e-05 c194:5.47721e-05 c195:5.47722e-05 c196:5.47723e-05 c197:5.47723e-05 c198:5.47723e-05 c199:5.47723e-05 c200:5.47723e-05 c201:5.47724e-05 c202:5.47725e-05 c203:5.47726e-05 c204:5.47727e-05 c205:5.47727e-05 c206:5.47726e-05 c207:5.47727e-05 c208:5.47728e-05 c209:5.47727e-05 c210:5.47728e-05 c211:5.47728e-05 c212:5.4773e-05 c213:5.47731e-05 c214:5.47731e-05 c215:5.47732e-05 c216:5.47732e-05 c217:5.47732e-05 c218:5.47732e-05 c219:5.47733e-05 c220:5.47733e-05 c221:5.47733e-05 c222:5.47732e-05 c223:5.47732e-05 c224:5.47732e-05 c225:5.47733e-05 c226:5.47732e-05 c227:5.47732e-05 c228:5.47733e-05 c229:5.47733e-05 c230:5.47733e-05 c231:5.47732e-05 c232:5.47733e-05 c233:5.47734e-05 c234:5.47734e-05 c235:5.47734e-05 c236:5.47736e-05 c237:5.47737e-05 c238:5.47738e-05 c239:5.47738e-05 c240:5.47737e-05 c241:5.47737e-05 c242:5.47739e-05 c243:5.47739e-05 c244:5.47739e-05 c245:5.47739e-05 c246:5.47739e-05 c247:5.47739e-05 c248:5.47739e-05 c249:5.47739e-05 c250:5.47739e-05 c251:5.47739e-05 c252:5.4774e-05 c253:5.47739e-05 c254:5.4774e-05 c255:5.4774e-05 c256:5.4774e-05 c257:5.47739e-05 c258:5.47738e-05 c259:5.47738e-05 c260:5.47739e-05 c261:5.47739e-05 c262:5.47739e-05 c263:5.47739e-05 c264:5.47739e-05 c265:5.47739e-05 c266:5.47739e-05 c267:5.47739e-05 c268:5.47738e-05 c269:5.47738e-05 c270:5.47738e-05 c271:5.47737e-05 c272:5.47738e-05 c273:5.47738e-05 c274:5.47738e-05 c275:5.47738e-05 c276:5.47738e-05 c277:5.4774e-05 c278:5.47741e-05 c279:5.4774e-05 c280:5.4774e-05 c281:5.47743e-05 c282:5.47742e-05 c283:5.47742e-05 c284:5.47743e-05 c285:5.47743e-05 c286:5.47742e-05 c287:5.47743e-05 c288:5.47742e-05 c289:5.47742e-05 c290:5.47741e-05 c291:5.47741e-05 c292:5.47741e-05 c293:5.47741e-05 c294:5.4774e-05 c295:5.47741e-05 c296:5.47741e-05 c297:5.47741e-05 c298:5.47741e-05 c299:5.47743e-05 c300:5.47742e-05 c301:5.47742e-05 c302:5.47742e-05 c303:5.47744e-05 c304:5.47744e-05 c305:5.47744e-05 c306:5.47743e-05 c307:5.47743e-05 c308:5.47742e-05 c309:5.47744e-05 c310:5.47744e-05 c311:5.47745e-05 c312:5.47746e-05 c313:5.47746e-05 c314:5.78772e-05 c315:5.78771e-05 c316:5.78771e-05 c317:5.78773e-05 c318:5.78774e-05 c319:5.78773e-05 c320:5.78773e-05 c321:5.78773e-05 c322:5.78773e-05 c323:5.78774e-05 c324:5.78774e-05 c325:5.78774e-05 c326:5.78775e-05 c327:5.78777e-05 c328:5.78777e-05 c329:5.78777e-05 c330:5.78776e-05 c331:5.78776e-05 c332:5.78776e-05 c333:5.78776e-05 c334:5.78776e-05 c335:5.78776e-05 c336:5.78777e-05 c337:5.78777e-05 c338:5.78776e-05 c339:5.78776e-05 c340:5.78776e-05 c341:5.78776e-05 c342:5.78776e-05 c343:5.78775e-05 c344:5.78774e-05 c345:5.78775e-05 c346:5.78775e-05 c347:5.78774e-05 c348:5.78774e-05 c349:5.78774e-05 c350:5.78773e-05 c351:5.78773e-05 c352:5.78772e-05 c353:5.78773e-05 c354:5.78773e-05 c355:5.78772e-05 c356:5.78773e-05 c357:5.78772e-05 c358:5.78773e-05 c359:5.78772e-05 c360:5.78773e-05 c361:5.78773e-05 c362:5.78775e-05 c363:5.78775e-05 c364:5.78776e-05 c365:5.78777e-05 c366:5.78776e-05 c367:5.78776e-05 c368:5.78776e-05 c369:5.78779e-05 c370:5.78779e-05 c371:5.7878e-05 c372:5.78781e-05 c373:5.78781e-05 c374:5.78781e-05 c375:5.78781e-05 c376:5.7878e-05 c377:5.7878e-05 c378:5.7878e-05 c379:5.78779e-05 c380:5.78779e-05 c381:5.78779e-05 c382:5.78779e-05 c383:5.78778e-05 c384:5.7878e-05 c385:5.7878e-05 c386:5.78781e-05 c387:5.78781e-05 c388:5.7878e-05 c389:5.7878e-05 c390:5.7878e-05 c391:5.7878e-05 c392:5.7878e-05 c393:5.7878e-05 c394:5.7878e-05 
    2019-11-19 18:48:03	INFO	SIImageStore::printBeamSet 	Restoring Beams 
    2019-11-19 18:48:03	INFO	SIImageStore::printBeamSet +	Pol   Type Chan        Freq     Vel
    2019-11-19 18:48:03	INFO	SIImageStore::printBeamSet +	  I    Max    0 1.53000e+11 206783.05    0.0809 arcsec x    0.0700 arcsec pa=-30.0501 deg
    2019-11-19 18:48:03	INFO	SIImageStore::printBeamSet +	  I    Min  394 1.54539e+11 205847.40    0.0760 arcsec x    0.0600 arcsec pa=-36.3047 deg
    2019-11-19 18:48:03	INFO	SIImageStore::printBeamSet +	  I Median  197 1.53769e+11 206315.22    0.0806 arcsec x    0.0698 arcsec pa=-30.1034 deg
    2019-11-19 18:48:03	INFO	task_tclean::SynthesisImagerVi2::makePrimaryBeam 	vi2 : Evaluating Primary Beam model onto image grid(s)
    2019-11-19 18:48:06	INFO	task_tclean::SynthesisImager::executeMajorCycle 	----------------------------------------------------------- Run (Last) Major Cycle 1 -------------------------------------
    
    0%....10....20....30....40....50....60....70....80....90....100%
    2019-11-19 18:51:20	INFO	task_tclean::SDAlgorithmBase::restore 	[ci10/sci] : Restoring model image.
    2019-11-19 18:51:20	WARN	task_tclean::SIImageStore::restore (file casa-source/code/synthesis/ImagerObjects/SIImageStore.cc, line 2068)	Restoring with an empty model image. Only residuals will be processed to form the output restored image.
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 0 : 0.0808671 arcsec, 0.0700303 arcsec, -30.0501 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 1 : 0.0808657 arcsec, 0.0700292 arcsec, -30.05 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 2 : 0.0808641 arcsec, 0.0700281 arcsec, -30.0503 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 3 : 0.0808627 arcsec, 0.0700269 arcsec, -30.0506 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 4 : 0.0808612 arcsec, 0.0700256 arcsec, -30.0511 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 5 : 0.0808596 arcsec, 0.0700243 arcsec, -30.0512 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 6 : 0.0808581 arcsec, 0.0700231 arcsec, -30.0514 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 7 : 0.0808565 arcsec, 0.0700218 arcsec, -30.0522 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 8 : 0.0808552 arcsec, 0.0700207 arcsec, -30.0526 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 9 : 0.0808537 arcsec, 0.0700197 arcsec, -30.0527 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 10 : 0.0808523 arcsec, 0.0700185 arcsec, -30.053 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 11 : 0.0808509 arcsec, 0.0700175 arcsec, -30.053 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 12 : 0.0808495 arcsec, 0.0700164 arcsec, -30.0533 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 13 : 0.080848 arcsec, 0.0700152 arcsec, -30.0533 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 14 : 0.0808465 arcsec, 0.0700141 arcsec, -30.0533 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 15 : 0.0808452 arcsec, 0.0700132 arcsec, -30.0536 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 16 : 0.0808436 arcsec, 0.0700122 arcsec, -30.054 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 17 : 0.080842 arcsec, 0.0700109 arcsec, -30.0539 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 18 : 0.0808403 arcsec, 0.0700096 arcsec, -30.0542 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 19 : 0.0808387 arcsec, 0.0700081 arcsec, -30.055 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 20 : 0.0808371 arcsec, 0.0700069 arcsec, -30.0549 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 21 : 0.0808356 arcsec, 0.0700056 arcsec, -30.0551 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 22 : 0.0808341 arcsec, 0.0700045 arcsec, -30.0554 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 23 : 0.0808326 arcsec, 0.0700034 arcsec, -30.0556 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 24 : 0.080831 arcsec, 0.070002 arcsec, -30.056 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 25 : 0.0808295 arcsec, 0.0700008 arcsec, -30.0563 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 26 : 0.080828 arcsec, 0.0699997 arcsec, -30.0565 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 27 : 0.0808265 arcsec, 0.0699985 arcsec, -30.0567 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 28 : 0.0808251 arcsec, 0.0699975 arcsec, -30.057 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 29 : 0.0808237 arcsec, 0.0699964 arcsec, -30.0571 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 30 : 0.0808221 arcsec, 0.0699952 arcsec, -30.0577 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 31 : 0.0808206 arcsec, 0.069994 arcsec, -30.0579 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 32 : 0.0808193 arcsec, 0.069993 arcsec, -30.0582 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 33 : 0.0808176 arcsec, 0.0699917 arcsec, -30.0583 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 34 : 0.080816 arcsec, 0.0699905 arcsec, -30.0585 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 35 : 0.0808147 arcsec, 0.0699892 arcsec, -30.0592 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 36 : 0.0808132 arcsec, 0.0699881 arcsec, -30.0595 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 37 : 0.0808116 arcsec, 0.0699866 arcsec, -30.0597 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 38 : 0.0808101 arcsec, 0.0699854 arcsec, -30.06 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 39 : 0.0808081 arcsec, 0.0699839 arcsec, -30.06 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 40 : 0.0808066 arcsec, 0.0699826 arcsec, -30.0605 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 41 : 0.0808044 arcsec, 0.0699809 arcsec, -30.0608 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 42 : 0.0808032 arcsec, 0.0699801 arcsec, -30.0609 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 43 : 0.0808017 arcsec, 0.069979 arcsec, -30.0609 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 44 : 0.0808002 arcsec, 0.0699777 arcsec, -30.0612 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 45 : 0.0807988 arcsec, 0.0699765 arcsec, -30.0615 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 46 : 0.0807973 arcsec, 0.0699754 arcsec, -30.0615 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 47 : 0.0807955 arcsec, 0.069974 arcsec, -30.0616 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 48 : 0.0807939 arcsec, 0.0699726 arcsec, -30.062 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 49 : 0.0807925 arcsec, 0.0699714 arcsec, -30.0626 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 50 : 0.080791 arcsec, 0.0699704 arcsec, -30.0628 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 51 : 0.0807895 arcsec, 0.0699693 arcsec, -30.0631 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 52 : 0.0807881 arcsec, 0.0699679 arcsec, -30.0635 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 53 : 0.0807862 arcsec, 0.0699667 arcsec, -30.0636 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 54 : 0.0807846 arcsec, 0.0699655 arcsec, -30.0638 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 55 : 0.0807831 arcsec, 0.0699643 arcsec, -30.0641 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 56 : 0.0807815 arcsec, 0.0699631 arcsec, -30.0643 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 57 : 0.08078 arcsec, 0.069962 arcsec, -30.0646 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 58 : 0.0807785 arcsec, 0.0699609 arcsec, -30.0649 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 59 : 0.0807771 arcsec, 0.0699599 arcsec, -30.065 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 60 : 0.0807755 arcsec, 0.0699587 arcsec, -30.0653 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 61 : 0.0807739 arcsec, 0.0699576 arcsec, -30.0656 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 62 : 0.0807723 arcsec, 0.0699562 arcsec, -30.066 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 63 : 0.0807709 arcsec, 0.069955 arcsec, -30.0665 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 64 : 0.0807694 arcsec, 0.0699538 arcsec, -30.0668 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 65 : 0.0807679 arcsec, 0.0699527 arcsec, -30.0668 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 66 : 0.0807665 arcsec, 0.0699516 arcsec, -30.0672 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 67 : 0.080765 arcsec, 0.0699504 arcsec, -30.0675 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 68 : 0.0807636 arcsec, 0.0699492 arcsec, -30.068 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 69 : 0.0807622 arcsec, 0.0699481 arcsec, -30.0682 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 70 : 0.0807607 arcsec, 0.0699468 arcsec, -30.0685 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 71 : 0.0807593 arcsec, 0.0699458 arcsec, -30.0688 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 72 : 0.0807578 arcsec, 0.0699448 arcsec, -30.0689 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 73 : 0.0807563 arcsec, 0.0699435 arcsec, -30.0696 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 74 : 0.080755 arcsec, 0.0699422 arcsec, -30.0703 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 75 : 0.0807535 arcsec, 0.069941 arcsec, -30.0707 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 76 : 0.0807521 arcsec, 0.0699399 arcsec, -30.0712 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 77 : 0.0807505 arcsec, 0.0699387 arcsec, -30.0715 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 78 : 0.080749 arcsec, 0.0699375 arcsec, -30.0715 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 79 : 0.0807476 arcsec, 0.0699362 arcsec, -30.0721 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 80 : 0.0807461 arcsec, 0.0699351 arcsec, -30.0721 deg
    2019-11-19 18:51:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 81 : 0.0807447 arcsec, 0.069934 arcsec, -30.0722 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 82 : 0.0807432 arcsec, 0.0699329 arcsec, -30.0725 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 83 : 0.0807417 arcsec, 0.0699317 arcsec, -30.0727 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 84 : 0.0807401 arcsec, 0.0699305 arcsec, -30.0729 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 85 : 0.0807386 arcsec, 0.0699294 arcsec, -30.0732 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 86 : 0.0807371 arcsec, 0.0699282 arcsec, -30.0736 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 87 : 0.0807356 arcsec, 0.0699271 arcsec, -30.0737 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 88 : 0.0807341 arcsec, 0.069926 arcsec, -30.074 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 89 : 0.0807326 arcsec, 0.0699248 arcsec, -30.0744 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 90 : 0.080731 arcsec, 0.0699235 arcsec, -30.0745 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 91 : 0.0807297 arcsec, 0.0699225 arcsec, -30.0746 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 92 : 0.0807282 arcsec, 0.0699214 arcsec, -30.0746 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 93 : 0.0807266 arcsec, 0.06992 arcsec, -30.075 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 94 : 0.0807249 arcsec, 0.0699186 arcsec, -30.0753 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 95 : 0.0807235 arcsec, 0.0699174 arcsec, -30.0755 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 96 : 0.0807221 arcsec, 0.0699163 arcsec, -30.0758 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 97 : 0.0807205 arcsec, 0.069915 arcsec, -30.0761 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 98 : 0.080719 arcsec, 0.0699139 arcsec, -30.0763 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 99 : 0.0807176 arcsec, 0.0699128 arcsec, -30.0765 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 100 : 0.080716 arcsec, 0.0699118 arcsec, -30.0767 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 101 : 0.0807144 arcsec, 0.0699104 arcsec, -30.0771 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 102 : 0.080713 arcsec, 0.0699092 arcsec, -30.0774 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 103 : 0.0807115 arcsec, 0.0699082 arcsec, -30.0775 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 104 : 0.0807101 arcsec, 0.069907 arcsec, -30.0777 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 105 : 0.0807085 arcsec, 0.0699058 arcsec, -30.0779 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 106 : 0.0807071 arcsec, 0.0699047 arcsec, -30.0782 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 107 : 0.0807055 arcsec, 0.0699034 arcsec, -30.0785 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 108 : 0.0807041 arcsec, 0.0699021 arcsec, -30.0789 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 109 : 0.0807026 arcsec, 0.069901 arcsec, -30.0787 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 110 : 0.0807012 arcsec, 0.0698999 arcsec, -30.0786 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 111 : 0.0806998 arcsec, 0.0698989 arcsec, -30.0786 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 112 : 0.0806984 arcsec, 0.0698976 arcsec, -30.0786 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 113 : 0.0806968 arcsec, 0.0698965 arcsec, -30.0787 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 114 : 0.080695 arcsec, 0.0698952 arcsec, -30.0785 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 115 : 0.0806937 arcsec, 0.0698941 arcsec, -30.079 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 116 : 0.0806923 arcsec, 0.0698931 arcsec, -30.0792 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 117 : 0.0806909 arcsec, 0.0698919 arcsec, -30.0794 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 118 : 0.0806892 arcsec, 0.0698907 arcsec, -30.0796 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 119 : 0.0806876 arcsec, 0.0698895 arcsec, -30.08 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 120 : 0.0806861 arcsec, 0.0698884 arcsec, -30.0801 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 121 : 0.0806846 arcsec, 0.0698872 arcsec, -30.0803 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 122 : 0.0806832 arcsec, 0.0698861 arcsec, -30.0805 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 123 : 0.0806817 arcsec, 0.0698848 arcsec, -30.0812 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 124 : 0.0806801 arcsec, 0.0698835 arcsec, -30.0817 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 125 : 0.0806786 arcsec, 0.0698826 arcsec, -30.0817 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 126 : 0.0806771 arcsec, 0.0698813 arcsec, -30.0822 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 127 : 0.0806757 arcsec, 0.0698802 arcsec, -30.0825 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 128 : 0.0806742 arcsec, 0.069879 arcsec, -30.0828 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 129 : 0.0806727 arcsec, 0.0698779 arcsec, -30.0829 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 130 : 0.0806712 arcsec, 0.0698768 arcsec, -30.0831 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 131 : 0.0806698 arcsec, 0.0698757 arcsec, -30.0838 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 132 : 0.0806683 arcsec, 0.0698744 arcsec, -30.084 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 133 : 0.0806668 arcsec, 0.0698734 arcsec, -30.0842 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 134 : 0.0806649 arcsec, 0.0698718 arcsec, -30.0845 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 135 : 0.0806632 arcsec, 0.0698705 arcsec, -30.0845 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 136 : 0.0806615 arcsec, 0.0698691 arcsec, -30.0846 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 137 : 0.0806599 arcsec, 0.0698679 arcsec, -30.0845 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 138 : 0.0806582 arcsec, 0.0698665 arcsec, -30.0847 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 139 : 0.0806568 arcsec, 0.0698653 arcsec, -30.0849 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 140 : 0.0806551 arcsec, 0.069864 arcsec, -30.0852 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 141 : 0.0806537 arcsec, 0.0698628 arcsec, -30.0857 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 142 : 0.0806523 arcsec, 0.0698615 arcsec, -30.0862 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 143 : 0.0806508 arcsec, 0.0698603 arcsec, -30.0868 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 144 : 0.0806493 arcsec, 0.069859 arcsec, -30.0874 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 145 : 0.0806479 arcsec, 0.0698578 arcsec, -30.0877 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 146 : 0.0806464 arcsec, 0.0698567 arcsec, -30.0877 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 147 : 0.0806449 arcsec, 0.0698556 arcsec, -30.088 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 148 : 0.0806434 arcsec, 0.0698544 arcsec, -30.0885 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 149 : 0.0806419 arcsec, 0.0698531 arcsec, -30.0885 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 150 : 0.0806402 arcsec, 0.069852 arcsec, -30.0886 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 151 : 0.0806387 arcsec, 0.0698507 arcsec, -30.0888 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 152 : 0.0806373 arcsec, 0.0698495 arcsec, -30.0892 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 153 : 0.0806359 arcsec, 0.0698484 arcsec, -30.0896 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 154 : 0.0806344 arcsec, 0.0698472 arcsec, -30.09 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 155 : 0.0806329 arcsec, 0.0698458 arcsec, -30.0906 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 156 : 0.0806315 arcsec, 0.0698448 arcsec, -30.0905 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 157 : 0.0806302 arcsec, 0.0698438 arcsec, -30.0907 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 158 : 0.0806287 arcsec, 0.0698426 arcsec, -30.091 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 159 : 0.0806272 arcsec, 0.0698414 arcsec, -30.0912 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 160 : 0.0806259 arcsec, 0.0698404 arcsec, -30.0917 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 161 : 0.0806243 arcsec, 0.0698391 arcsec, -30.0919 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 162 : 0.0806226 arcsec, 0.0698378 arcsec, -30.0923 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 163 : 0.0806212 arcsec, 0.0698365 arcsec, -30.0928 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 164 : 0.0806198 arcsec, 0.0698353 arcsec, -30.0933 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 165 : 0.0806184 arcsec, 0.0698344 arcsec, -30.0935 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 166 : 0.0806169 arcsec, 0.0698333 arcsec, -30.0938 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 167 : 0.0806153 arcsec, 0.0698321 arcsec, -30.0941 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 168 : 0.0806138 arcsec, 0.0698308 arcsec, -30.0947 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 169 : 0.0806123 arcsec, 0.0698297 arcsec, -30.0949 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 170 : 0.0806108 arcsec, 0.0698286 arcsec, -30.0953 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 171 : 0.0806094 arcsec, 0.0698275 arcsec, -30.0955 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 172 : 0.080608 arcsec, 0.0698265 arcsec, -30.0959 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 173 : 0.0806066 arcsec, 0.0698253 arcsec, -30.0962 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 174 : 0.0806051 arcsec, 0.0698242 arcsec, -30.0964 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 175 : 0.0806036 arcsec, 0.069823 arcsec, -30.0967 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 176 : 0.0806022 arcsec, 0.0698219 arcsec, -30.097 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 177 : 0.0806007 arcsec, 0.0698207 arcsec, -30.0975 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 178 : 0.0805993 arcsec, 0.0698196 arcsec, -30.098 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 179 : 0.0805979 arcsec, 0.0698186 arcsec, -30.0982 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 180 : 0.0805965 arcsec, 0.0698173 arcsec, -30.0989 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 181 : 0.0805951 arcsec, 0.0698163 arcsec, -30.0991 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 182 : 0.0805936 arcsec, 0.0698153 arcsec, -30.0992 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 183 : 0.0805918 arcsec, 0.0698138 arcsec, -30.0995 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 184 : 0.0805904 arcsec, 0.0698128 arcsec, -30.0998 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 185 : 0.0805889 arcsec, 0.0698115 arcsec, -30.1001 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 186 : 0.0805877 arcsec, 0.0698105 arcsec, -30.1004 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 187 : 0.0805861 arcsec, 0.0698092 arcsec, -30.1009 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 188 : 0.0805845 arcsec, 0.0698078 arcsec, -30.1012 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 189 : 0.0805831 arcsec, 0.0698067 arcsec, -30.1014 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 190 : 0.0805815 arcsec, 0.0698052 arcsec, -30.102 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 191 : 0.0805801 arcsec, 0.0698043 arcsec, -30.1021 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 192 : 0.0805785 arcsec, 0.0698029 arcsec, -30.1025 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 193 : 0.0805771 arcsec, 0.0698018 arcsec, -30.1028 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 194 : 0.0805756 arcsec, 0.0698007 arcsec, -30.1028 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 195 : 0.0805741 arcsec, 0.0697995 arcsec, -30.103 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 196 : 0.0805724 arcsec, 0.0697981 arcsec, -30.1032 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 197 : 0.080571 arcsec, 0.069797 arcsec, -30.1034 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 198 : 0.0805695 arcsec, 0.0697959 arcsec, -30.1037 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 199 : 0.080568 arcsec, 0.0697947 arcsec, -30.104 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 200 : 0.0805665 arcsec, 0.0697934 arcsec, -30.1041 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 201 : 0.080565 arcsec, 0.0697922 arcsec, -30.1045 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 202 : 0.0805633 arcsec, 0.0697908 arcsec, -30.1045 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 203 : 0.0805616 arcsec, 0.0697896 arcsec, -30.1044 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 204 : 0.08056 arcsec, 0.0697884 arcsec, -30.1046 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 205 : 0.0805587 arcsec, 0.0697872 arcsec, -30.1048 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 206 : 0.0805573 arcsec, 0.0697862 arcsec, -30.1053 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 207 : 0.0805558 arcsec, 0.0697851 arcsec, -30.1057 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 208 : 0.0805542 arcsec, 0.0697838 arcsec, -30.106 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 209 : 0.0805528 arcsec, 0.0697826 arcsec, -30.1064 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 210 : 0.0805511 arcsec, 0.0697813 arcsec, -30.1066 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 211 : 0.0805497 arcsec, 0.0697802 arcsec, -30.1068 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 212 : 0.0805479 arcsec, 0.0697787 arcsec, -30.107 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 213 : 0.0805464 arcsec, 0.0697773 arcsec, -30.1078 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 214 : 0.0805449 arcsec, 0.0697763 arcsec, -30.108 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 215 : 0.0805433 arcsec, 0.0697749 arcsec, -30.1084 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 216 : 0.0805418 arcsec, 0.0697737 arcsec, -30.1087 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 217 : 0.0805404 arcsec, 0.0697726 arcsec, -30.1091 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 218 : 0.080539 arcsec, 0.0697714 arcsec, -30.1095 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 219 : 0.0805374 arcsec, 0.0697701 arcsec, -30.11 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 220 : 0.0805359 arcsec, 0.0697689 arcsec, -30.1104 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 221 : 0.0805345 arcsec, 0.0697678 arcsec, -30.1103 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 222 : 0.0805331 arcsec, 0.0697668 arcsec, -30.1106 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 223 : 0.0805316 arcsec, 0.0697656 arcsec, -30.1114 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 224 : 0.0805302 arcsec, 0.0697644 arcsec, -30.1117 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 225 : 0.0805287 arcsec, 0.0697631 arcsec, -30.112 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 226 : 0.0805273 arcsec, 0.0697621 arcsec, -30.1123 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 227 : 0.0805259 arcsec, 0.069761 arcsec, -30.1126 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 228 : 0.0805244 arcsec, 0.0697598 arcsec, -30.1128 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 229 : 0.0805229 arcsec, 0.0697586 arcsec, -30.1133 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 230 : 0.0805214 arcsec, 0.0697574 arcsec, -30.1136 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 231 : 0.08052 arcsec, 0.0697563 arcsec, -30.1141 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 232 : 0.0805185 arcsec, 0.0697551 arcsec, -30.1141 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 233 : 0.0805169 arcsec, 0.0697539 arcsec, -30.1145 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 234 : 0.0805154 arcsec, 0.0697528 arcsec, -30.1147 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 235 : 0.0805139 arcsec, 0.0697517 arcsec, -30.1148 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 236 : 0.0805123 arcsec, 0.0697504 arcsec, -30.1149 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 237 : 0.0805105 arcsec, 0.0697491 arcsec, -30.1149 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 238 : 0.080509 arcsec, 0.0697478 arcsec, -30.1151 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 239 : 0.0805076 arcsec, 0.0697467 arcsec, -30.1152 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 240 : 0.0805063 arcsec, 0.0697457 arcsec, -30.1154 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 241 : 0.0805049 arcsec, 0.0697446 arcsec, -30.1158 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 242 : 0.0805032 arcsec, 0.0697431 arcsec, -30.1164 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 243 : 0.0805019 arcsec, 0.0697421 arcsec, -30.1167 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 244 : 0.0805004 arcsec, 0.0697409 arcsec, -30.1171 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 245 : 0.0804991 arcsec, 0.0697399 arcsec, -30.1177 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 246 : 0.0804977 arcsec, 0.0697386 arcsec, -30.1179 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 247 : 0.0804962 arcsec, 0.0697373 arcsec, -30.1181 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 248 : 0.0804947 arcsec, 0.0697362 arcsec, -30.1183 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 249 : 0.0804931 arcsec, 0.069735 arcsec, -30.1186 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 250 : 0.0804917 arcsec, 0.069734 arcsec, -30.1189 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 251 : 0.0804902 arcsec, 0.0697329 arcsec, -30.1192 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 252 : 0.0804887 arcsec, 0.0697317 arcsec, -30.1194 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 253 : 0.0804874 arcsec, 0.0697305 arcsec, -30.12 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 254 : 0.0804859 arcsec, 0.0697293 arcsec, -30.1204 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 255 : 0.0804845 arcsec, 0.0697282 arcsec, -30.1208 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 256 : 0.080483 arcsec, 0.069727 arcsec, -30.1211 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 257 : 0.0804816 arcsec, 0.069726 arcsec, -30.1212 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 258 : 0.0804802 arcsec, 0.0697249 arcsec, -30.1215 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 259 : 0.0804788 arcsec, 0.0697238 arcsec, -30.1219 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 260 : 0.0804773 arcsec, 0.0697225 arcsec, -30.1219 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 261 : 0.0804758 arcsec, 0.0697214 arcsec, -30.1221 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 262 : 0.0804742 arcsec, 0.0697202 arcsec, -30.1225 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 263 : 0.0804728 arcsec, 0.0697191 arcsec, -30.1228 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 264 : 0.0804712 arcsec, 0.0697179 arcsec, -30.1232 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 265 : 0.0804697 arcsec, 0.0697169 arcsec, -30.1235 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 266 : 0.0804683 arcsec, 0.0697157 arcsec, -30.1239 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 267 : 0.080467 arcsec, 0.0697146 arcsec, -30.1243 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 268 : 0.0804656 arcsec, 0.0697135 arcsec, -30.1249 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 269 : 0.0804642 arcsec, 0.0697125 arcsec, -30.1247 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 270 : 0.0804629 arcsec, 0.0697115 arcsec, -30.1254 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 271 : 0.0804615 arcsec, 0.0697105 arcsec, -30.1257 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 272 : 0.08046 arcsec, 0.0697093 arcsec, -30.1263 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 273 : 0.0804585 arcsec, 0.0697082 arcsec, -30.1262 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 274 : 0.0804571 arcsec, 0.0697072 arcsec, -30.1262 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 275 : 0.0804556 arcsec, 0.069706 arcsec, -30.1264 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 276 : 0.0804542 arcsec, 0.0697051 arcsec, -30.1265 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 277 : 0.0804526 arcsec, 0.0697038 arcsec, -30.1271 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 278 : 0.080451 arcsec, 0.0697024 arcsec, -30.1274 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 279 : 0.0804496 arcsec, 0.0697013 arcsec, -30.1277 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 280 : 0.0804482 arcsec, 0.0697002 arcsec, -30.1283 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 281 : 0.0804463 arcsec, 0.0696986 arcsec, -30.1289 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 282 : 0.0804451 arcsec, 0.0696976 arcsec, -30.1293 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 283 : 0.0804437 arcsec, 0.0696965 arcsec, -30.1295 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 284 : 0.0804421 arcsec, 0.0696952 arcsec, -30.1299 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 285 : 0.0804406 arcsec, 0.0696942 arcsec, -30.13 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 286 : 0.0804393 arcsec, 0.0696932 arcsec, -30.1304 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 287 : 0.0804379 arcsec, 0.0696921 arcsec, -30.1306 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 288 : 0.0804364 arcsec, 0.069691 arcsec, -30.131 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 289 : 0.080435 arcsec, 0.06969 arcsec, -30.1316 deg
    2019-11-19 18:51:21	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 290 : 0.0804337 arcsec, 0.069689 arcsec, -30.1319 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 291 : 0.0804323 arcsec, 0.0696878 arcsec, -30.1323 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 292 : 0.080431 arcsec, 0.0696868 arcsec, -30.1323 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 293 : 0.0804294 arcsec, 0.0696855 arcsec, -30.133 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 294 : 0.0804281 arcsec, 0.0696845 arcsec, -30.1331 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 295 : 0.0804263 arcsec, 0.0696831 arcsec, -30.1336 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 296 : 0.080425 arcsec, 0.0696822 arcsec, -30.1339 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 297 : 0.0804235 arcsec, 0.069681 arcsec, -30.134 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 298 : 0.080422 arcsec, 0.0696798 arcsec, -30.1342 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 299 : 0.0804203 arcsec, 0.0696784 arcsec, -30.1347 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 300 : 0.0804189 arcsec, 0.0696774 arcsec, -30.1346 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 301 : 0.0804174 arcsec, 0.0696763 arcsec, -30.1348 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 302 : 0.0804159 arcsec, 0.0696752 arcsec, -30.135 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 303 : 0.0804143 arcsec, 0.069674 arcsec, -30.1355 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 304 : 0.0804129 arcsec, 0.0696729 arcsec, -30.1361 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 305 : 0.0804115 arcsec, 0.0696717 arcsec, -30.137 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 306 : 0.08041 arcsec, 0.0696705 arcsec, -30.1372 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 307 : 0.0804087 arcsec, 0.0696694 arcsec, -30.1375 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 308 : 0.0804073 arcsec, 0.0696683 arcsec, -30.1377 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 309 : 0.0804058 arcsec, 0.069667 arcsec, -30.1382 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 310 : 0.0804043 arcsec, 0.0696656 arcsec, -30.1386 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 311 : 0.0804026 arcsec, 0.0696644 arcsec, -30.1386 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 312 : 0.0804011 arcsec, 0.069663 arcsec, -30.1391 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 313 : 0.0803997 arcsec, 0.0696619 arcsec, -30.1394 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 314 : 0.0760933 arcsec, 0.060078 arcsec, -36.2921 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 315 : 0.0760918 arcsec, 0.0600767 arcsec, -36.2922 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 316 : 0.0760904 arcsec, 0.0600757 arcsec, -36.2921 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 317 : 0.0760886 arcsec, 0.0600742 arcsec, -36.2923 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 318 : 0.0760872 arcsec, 0.060073 arcsec, -36.2924 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 319 : 0.0760858 arcsec, 0.0600721 arcsec, -36.2924 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 320 : 0.0760845 arcsec, 0.0600709 arcsec, -36.2928 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 321 : 0.076083 arcsec, 0.0600696 arcsec, -36.2928 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 322 : 0.0760816 arcsec, 0.0600683 arcsec, -36.2929 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 323 : 0.0760801 arcsec, 0.060067 arcsec, -36.2932 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 324 : 0.0760788 arcsec, 0.0600659 arcsec, -36.2932 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 325 : 0.0760775 arcsec, 0.0600648 arcsec, -36.2934 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 326 : 0.0760759 arcsec, 0.0600634 arcsec, -36.2935 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 327 : 0.0760743 arcsec, 0.0600619 arcsec, -36.2936 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 328 : 0.0760729 arcsec, 0.0600609 arcsec, -36.2933 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 329 : 0.0760719 arcsec, 0.06006 arcsec, -36.2942 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 330 : 0.0760702 arcsec, 0.0600586 arcsec, -36.2938 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 331 : 0.0760688 arcsec, 0.0600574 arcsec, -36.294 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 332 : 0.0760674 arcsec, 0.0600562 arcsec, -36.2943 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 333 : 0.0760661 arcsec, 0.0600549 arcsec, -36.2944 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 334 : 0.0760647 arcsec, 0.0600539 arcsec, -36.2944 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 335 : 0.0760633 arcsec, 0.0600529 arcsec, -36.2944 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 336 : 0.0760617 arcsec, 0.0600513 arcsec, -36.2946 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 337 : 0.0760604 arcsec, 0.0600501 arcsec, -36.2946 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 338 : 0.0760592 arcsec, 0.0600491 arcsec, -36.2949 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 339 : 0.0760579 arcsec, 0.0600481 arcsec, -36.2951 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 340 : 0.0760564 arcsec, 0.0600469 arcsec, -36.2949 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 341 : 0.0760552 arcsec, 0.0600457 arcsec, -36.2948 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 342 : 0.0760539 arcsec, 0.0600446 arcsec, -36.295 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 343 : 0.0760525 arcsec, 0.0600435 arcsec, -36.2952 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 344 : 0.0760513 arcsec, 0.0600423 arcsec, -36.2956 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 345 : 0.0760499 arcsec, 0.0600412 arcsec, -36.2958 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 346 : 0.0760486 arcsec, 0.0600399 arcsec, -36.2962 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 347 : 0.0760473 arcsec, 0.0600389 arcsec, -36.2962 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 348 : 0.076046 arcsec, 0.0600377 arcsec, -36.2964 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 349 : 0.0760447 arcsec, 0.0600365 arcsec, -36.2968 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 350 : 0.0760434 arcsec, 0.0600353 arcsec, -36.297 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 351 : 0.076042 arcsec, 0.060034 arcsec, -36.2973 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 352 : 0.0760407 arcsec, 0.0600329 arcsec, -36.2974 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 353 : 0.0760393 arcsec, 0.0600318 arcsec, -36.2976 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 354 : 0.076038 arcsec, 0.0600307 arcsec, -36.2978 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 355 : 0.0760367 arcsec, 0.0600295 arcsec, -36.2984 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 356 : 0.0760353 arcsec, 0.0600283 arcsec, -36.2988 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 357 : 0.0760339 arcsec, 0.0600272 arcsec, -36.299 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 358 : 0.0760326 arcsec, 0.060026 arcsec, -36.2994 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 359 : 0.0760313 arcsec, 0.0600249 arcsec, -36.2996 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 360 : 0.0760301 arcsec, 0.0600239 arcsec, -36.3 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 361 : 0.0760286 arcsec, 0.0600227 arcsec, -36.3001 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 362 : 0.0760269 arcsec, 0.0600214 arcsec, -36.3 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 363 : 0.0760255 arcsec, 0.0600202 arcsec, -36.3001 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 364 : 0.0760242 arcsec, 0.0600192 arcsec, -36.3 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 365 : 0.0760233 arcsec, 0.0600182 arcsec, -36.3008 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 366 : 0.0760218 arcsec, 0.0600168 arcsec, -36.3005 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 367 : 0.0760203 arcsec, 0.0600156 arcsec, -36.3008 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 368 : 0.076019 arcsec, 0.0600143 arcsec, -36.3011 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 369 : 0.0760172 arcsec, 0.0600128 arcsec, -36.3012 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 370 : 0.0760158 arcsec, 0.0600117 arcsec, -36.3013 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 371 : 0.0760143 arcsec, 0.0600104 arcsec, -36.3014 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 372 : 0.0760129 arcsec, 0.0600092 arcsec, -36.3013 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 373 : 0.0760114 arcsec, 0.0600081 arcsec, -36.3012 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 374 : 0.0760101 arcsec, 0.060007 arcsec, -36.3014 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 375 : 0.0760088 arcsec, 0.0600059 arcsec, -36.3017 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 376 : 0.0760074 arcsec, 0.0600049 arcsec, -36.3018 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 377 : 0.0760061 arcsec, 0.0600036 arcsec, -36.302 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 378 : 0.0760047 arcsec, 0.0600024 arcsec, -36.302 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 379 : 0.0760034 arcsec, 0.0600012 arcsec, -36.3022 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 380 : 0.0760021 arcsec, 0.0600001 arcsec, -36.3023 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 381 : 0.0760009 arcsec, 0.0599988 arcsec, -36.3026 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 382 : 0.0759996 arcsec, 0.0599977 arcsec, -36.3026 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 383 : 0.0759983 arcsec, 0.0599966 arcsec, -36.3029 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 384 : 0.0759967 arcsec, 0.0599953 arcsec, -36.3033 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 385 : 0.0759955 arcsec, 0.059994 arcsec, -36.3038 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 386 : 0.0759943 arcsec, 0.0599929 arcsec, -36.3041 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 387 : 0.0759929 arcsec, 0.0599919 arcsec, -36.3042 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 388 : 0.0759916 arcsec, 0.059991 arcsec, -36.304 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 389 : 0.0759903 arcsec, 0.0599896 arcsec, -36.3044 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 390 : 0.0759892 arcsec, 0.0599884 arcsec, -36.3047 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 391 : 0.0759879 arcsec, 0.0599873 arcsec, -36.3051 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 392 : 0.0759865 arcsec, 0.0599862 arcsec, -36.305 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 393 : 0.0759852 arcsec, 0.0599849 arcsec, -36.3051 deg
    2019-11-19 18:51:22	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 394 : 0.0759841 arcsec, 0.0599839 arcsec, -36.3047 deg
    2019-11-19 18:51:22	INFO	tclean::::casa	Result tclean: {}
    2019-11-19 18:51:22	INFO	tclean::::casa	Task tclean complete. Start time: 2019-11-19 12:45:10.564259 End time: 2019-11-19 12:51:22.122546
    2019-11-19 18:51:22	INFO	tclean::::casa	##### End Task: tclean               #####
    2019-11-19 18:51:22	INFO	tclean::::casa	##########################################
    2019-11-19 18:51:22	INFO	exportfits::::casa	##########################################
    2019-11-19 18:51:22	INFO	exportfits::::casa	##### Begin Task: exportfits         #####
    2019-11-19 18:51:22	INFO	exportfits::::casa	exportfits( imagename='ci10/sci.image', fitsimage='ci10/sci.fits', velocity=False, optical=False, bitpix=-32, minpix=0, maxpix=-1, overwrite=True, dropstokes=False, stokeslast=True, history=True, dropdeg=False )
    2019-11-19 18:51:22	INFO	exportfits::ImageFactory::toFITS	Applying mask of name 'mask0'
    2019-11-19 18:51:22	INFO	exportfits::ImageFitsConverter::ImageHeaderToFITS 	Truncating miscinfo field useweightimage to useweigh
    2019-11-19 18:51:23	INFO	exportfits::::casa	Result exportfits: None
    2019-11-19 18:51:23	INFO	exportfits::::casa	Task exportfits complete. Start time: 2019-11-19 12:51:22.126806 End time: 2019-11-19 12:51:22.788797
    2019-11-19 18:51:23	INFO	exportfits::::casa	##### End Task: exportfits           #####
    2019-11-19 18:51:23	INFO	exportfits::::casa	##########################################
    2019-11-19 18:51:25	INFO	tclean::::casa	##########################################
    2019-11-19 18:51:25	INFO	tclean::::casa	##### Begin Task: tclean             #####
    2019-11-19 18:51:25	INFO	tclean::::casa	tclean( vis=['../2017.1.01045.S/bb2.ms.mfs', '../2017.1.01045.S/bb4.ms.mfs', '../2013.1.00059.S/bb2.ms.mfs', '../2013.1.00059.S/bb4.ms.mfs'], selectdata=True, field='', spw='', timerange='', uvrange='', antenna='', scan='', observation='', intent='', datacolumn='data', imagename='cont/sci', imsize=[256, 256], cell=0.01, phasecenter='', stokes='I', projection='SIN', startmodel='', specmode='mfs', reffreq='', nchan=-1, start=0, width=1, outframe='LSRK', veltype='radio', restfreq=[], interpolation='nearest', perchanweightdensity=True, gridder='standard', facets=1, psfphasecenter='', chanchunks=1, wprojplanes=1, vptable='', mosweight=True, aterm=True, psterm=False, wbawp=True, conjbeams=False, cfcache='', usepointing=False, computepastep=360.0, rotatepastep=360.0, pointingoffsetsigdev=0.0, pblimit=0.2, normtype='flatnoise', deconvolver='hogbom', scales=[], nterms=2, smallscalebias=0.0, restoration=True, restoringbeam='', pbcor=False, outlierfile='', weighting='briggs', robust=1.0, noise='1.0Jy', npixels=0, uvtaper=[''], niter=0, gain=0.1, threshold=0.0, nsigma=0.0, cycleniter=-1, cyclefactor=1.0, minpsffraction=0.05, maxpsffraction=0.8, interactive=False, usemask='user', mask='', pbmask=0.0, sidelobethreshold=3.0, noisethreshold=5.0, lownoisethreshold=1.5, negativethreshold=0.0, smoothfactor=1.0, minbeamfrac=0.3, cutthreshold=0.01, growiterations=75, dogrowprune=True, minpercentchange=-1.0, verbose=False, fastnoise=True, restart=True, savemodel='none', calcres=True, calcpsf=True, parallel=False )
    2019-11-19 18:51:25	INFO	tclean::::casa	Verifying Input Parameters
    2019-11-19 18:51:25	INFO	SynthesisImagerVi2::selectData 	MS : ../2017.1.01045.S/bb2.ms.mfs | [Opened in readonly mode]
    2019-11-19 18:51:25	INFO	SynthesisImagerVi2::selectData 	  NRows selected : 276124
    2019-11-19 18:51:26	INFO	SynthesisImagerVi2::selectData 	MS : ../2017.1.01045.S/bb4.ms.mfs | [Opened in readonly mode]
    2019-11-19 18:51:26	INFO	SynthesisImagerVi2::selectData 	  NRows selected : 276124
    2019-11-19 18:51:26	INFO	SynthesisImagerVi2::selectData 	MS : ../2013.1.00059.S/bb2.ms.mfs | [Opened in readonly mode]
    2019-11-19 18:51:26	INFO	SynthesisImagerVi2::selectData 	  NRows selected : 74469
    2019-11-19 18:51:27	INFO	SynthesisImagerVi2::selectData 	MS : ../2013.1.00059.S/bb4.ms.mfs | [Opened in readonly mode]
    2019-11-19 18:51:27	INFO	SynthesisImagerVi2::selectData 	  NRows selected : 70778
    2019-11-19 18:51:28	INFO	SynthesisImagerVi2::defineImage 	Define image coordinates for [cont/sci] : 
    2019-11-19 18:51:28	INFO	SynthesisImagerVi2::defineImage 	Impars : start 0
    2019-11-19 18:51:28	INFO	SynthesisImagerVi2::defineImage 	Shape : [256, 256, 1, 1]Spectral : [1.48429e+11] at [0] with increment [1.58878e+10]
    2019-11-19 18:51:28	INFO	SynthesisImagerVi2::defineImage 	Set Gridding options for [cont/sci] with ftmachine : gridft
    2019-11-19 18:51:28	INFO	SynthesisImagerVi2::weight() 	Set imaging weights : Briggs weighting: sidelobes will be suppressed over full image
    2019-11-19 18:51:33	INFO	VisSetUtil::VisImagingWeight() 	Normal robustness, robust = 1
    2019-11-19 18:51:34	INFO	task_tclean::SynthesisDeconvolver::setupDeconvolution 	Set Deconvolution Options for [cont/sci] : hogbom
    2019-11-19 18:51:34	INFO	SynthesisImager::makePSF 	----------------------------------------------------------- Make PSF ---------------------------------------------
    2019-11-19 18:51:39	INFO	SIImageStore::calcSensitivity 	[cont/sci] Theoretical sensitivity (Jy/bm):1.95523e-06 
    2019-11-19 18:51:39	INFO	SIImageStore::printBeamSet 	Beam : 0.0801015 arcsec, 0.0647359 arcsec, -32.0456 deg
    2019-11-19 18:51:39	INFO	task_tclean::SynthesisImagerVi2::makePrimaryBeam 	vi2 : Evaluating Primary Beam model onto image grid(s)
    2019-11-19 18:51:40	INFO	task_tclean::SynthesisImager::executeMajorCycle 	----------------------------------------------------------- Run (Last) Major Cycle 1 -------------------------------------
    2019-11-19 18:51:46	INFO	task_tclean::SDAlgorithmBase::restore 	[cont/sci] : Restoring model image.
    2019-11-19 18:51:46	WARN	task_tclean::SIImageStore::restore (file casa-source/code/synthesis/ImagerObjects/SIImageStore.cc, line 2068)	Restoring with an empty model image. Only residuals will be processed to form the output restored image.
    2019-11-19 18:51:46	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 0 : 0.0801015 arcsec, 0.0647359 arcsec, -32.0456 deg
    2019-11-19 18:51:46	INFO	tclean::::casa	Result tclean: {}
    2019-11-19 18:51:46	INFO	tclean::::casa	Task tclean complete. Start time: 2019-11-19 12:51:25.310707 End time: 2019-11-19 12:51:45.804364
    2019-11-19 18:51:46	INFO	tclean::::casa	##### End Task: tclean               #####
    2019-11-19 18:51:46	INFO	tclean::::casa	##########################################
    2019-11-19 18:51:46	INFO	exportfits::::casa	##########################################
    2019-11-19 18:51:46	INFO	exportfits::::casa	##### Begin Task: exportfits         #####
    2019-11-19 18:51:46	INFO	exportfits::::casa	exportfits( imagename='cont/sci.image', fitsimage='cont/sci.fits', velocity=False, optical=False, bitpix=-32, minpix=0, maxpix=-1, overwrite=True, dropstokes=False, stokeslast=True, history=True, dropdeg=False )
    2019-11-19 18:51:46	INFO	exportfits::ImageFactory::toFITS	Applying mask of name 'mask0'
    2019-11-19 18:51:46	INFO	exportfits::ImageFitsConverter::ImageHeaderToFITS 	Truncating miscinfo field useweightimage to useweigh
    2019-11-19 18:51:46	INFO	exportfits::::casa	Result exportfits: None
    2019-11-19 18:51:46	INFO	exportfits::::casa	Task exportfits complete. Start time: 2019-11-19 12:51:45.809636 End time: 2019-11-19 12:51:45.825440
    2019-11-19 18:51:46	INFO	exportfits::::casa	##### End Task: exportfits           #####
    2019-11-19 18:51:46	INFO	exportfits::::casa	##########################################


2015.1.00250.S
^^^^^^^^^^^^^^

.. code:: ipython3

    demo_dir='/Users/Rui/Documents/Workspace/projects/GMaKE/examples/data/bx610/alma/2015.1.00250.S/'
    if  'hypersion' or 'mini' in socket.gethostname() :
        os.chdir(demo_dir)
    setLogfile(demo_dir+'/'+'demo_bx610_imaging.log')
    
    invert('bb2.ms','bb2.co76ci21/sci',cell=0.05,imsize=[64,64],datacolumn='data')
    invert('bb3.ms','bb3.h2o/sci',cell=0.05,imsize=[64,64],datacolumn='data')
    invert(['bb1.ms.mfs','bb4.ms.mfs'],'bb14.cont/sci',cell=0.05,imsize=[64,64],datacolumn='data',specmode='mfs')


.. parsed-literal::

    2019-11-19 17:51:00	INFO	tclean::::casa	##########################################
    2019-11-19 17:51:00	INFO	tclean::::casa	##### Begin Task: tclean             #####
    2019-11-19 17:51:00	INFO	tclean::::casa	tclean( vis='bb2.ms', selectdata=True, field='', spw='', timerange='', uvrange='', antenna='', scan='', observation='', intent='', datacolumn='data', imagename='bb2.co76ci21/sci', imsize=[64, 64], cell=0.05, phasecenter='', stokes='I', projection='SIN', startmodel='', specmode='cube', reffreq='', nchan=-1, start=0, width=1, outframe='LSRK', veltype='radio', restfreq=[], interpolation='nearest', perchanweightdensity=True, gridder='standard', facets=1, psfphasecenter='', chanchunks=1, wprojplanes=1, vptable='', mosweight=True, aterm=True, psterm=False, wbawp=True, conjbeams=False, cfcache='', usepointing=False, computepastep=360.0, rotatepastep=360.0, pointingoffsetsigdev=0.0, pblimit=0.2, normtype='flatnoise', deconvolver='hogbom', scales=[], nterms=2, smallscalebias=0.0, restoration=True, restoringbeam='', pbcor=False, outlierfile='', weighting='briggs', robust=1.0, noise='1.0Jy', npixels=0, uvtaper=[''], niter=0, gain=0.1, threshold=0.0, nsigma=0.0, cycleniter=-1, cyclefactor=1.0, minpsffraction=0.05, maxpsffraction=0.8, interactive=False, usemask='user', mask='', pbmask=0.0, sidelobethreshold=3.0, noisethreshold=5.0, lownoisethreshold=1.5, negativethreshold=0.0, smoothfactor=1.0, minbeamfrac=0.3, cutthreshold=0.01, growiterations=75, dogrowprune=True, minpercentchange=-1.0, verbose=False, fastnoise=True, restart=True, savemodel='none', calcres=True, calcpsf=True, parallel=False )
    2019-11-19 17:51:00	INFO	tclean::::casa	Verifying Input Parameters
    2019-11-19 17:51:00	INFO	SynthesisImagerVi2::selectData 	MS : bb2.ms | [Opened in readonly mode]
    2019-11-19 17:51:00	INFO	SynthesisImagerVi2::selectData 	  NRows selected : 56354
    2019-11-19 17:51:00	INFO	SynthesisImagerVi2::defineImage 	Define image coordinates for [bb2.co76ci21/sci] : 
    2019-11-19 17:51:00	INFO	MSTransformRegridder::calcChanFreqs	 phaseCenter='Direction: [0.973286, -0.0588581, 0.221923]'  Channels equidistant in freq
    2019-11-19 17:51:00	INFO	MSTransformRegridder::calcChanFreqs+	 Central frequency (in output frame) = 2.51679e+11 Hz
    2019-11-19 17:51:00	INFO	MSTransformRegridder::calcChanFreqs+	 Width of central channel (in output frame) = 7.81183e+06 Hz
    2019-11-19 17:51:00	INFO	MSTransformRegridder::calcChanFreqs+	 Number of channels = 238
    2019-11-19 17:51:00	INFO	MSTransformRegridder::calcChanFreqs+	 Total width of SPW (in output frame) = 1.85922e+09 Hz
    2019-11-19 17:51:00	INFO	MSTransformRegridder::calcChanFreqs+	 Lower edge = 2.50749e+11 Hz, upper edge = 2.52608e+11 Hz
    2019-11-19 17:51:00	INFO	SynthesisImagerVi2::defineImage 	Impars : start 0
    2019-11-19 17:51:00	INFO	SynthesisImagerVi2::defineImage 	Shape : [64, 64, 1, 238]Spectral : [2.50753e+11] at [0] with increment [7.81183e+06]
    2019-11-19 17:51:00	INFO	SynthesisImagerVi2::defineImage 	Set Gridding options for [bb2.co76ci21/sci] with ftmachine : gridft
    2019-11-19 17:51:00	INFO	SynthesisImagerVi2::weight() 	Set imaging weights : Briggs weighting: sidelobes will be suppressed over full image
    2019-11-19 17:51:00	INFO	SynthesisImagerVi2::weight() 	Doing spectral cube Briggs weighting formula --  norm
    2019-11-19 17:51:00	INFO	SynthesisImager::tuneSelectData 	Tuning frequency data selection to match image spectral coordinates
    2019-11-19 17:51:00	INFO	SynthesisImagerVi2::selectData 	MS : bb2.ms | [Opened in readonly mode]
    2019-11-19 17:51:00	INFO	SynthesisImagerVi2::selectData 	  NRows selected : 56354
    2019-11-19 17:51:00	INFO	task_tclean::SynthesisDeconvolver::setupDeconvolution 	Set Deconvolution Options for [bb2.co76ci21/sci] : hogbom
    2019-11-19 17:51:00	INFO	SynthesisImager::makePSF 	----------------------------------------------------------- Make PSF ---------------------------------------------
    
    0%....10....20....30....40....50....60....70....80....90....100%
    2019-11-19 17:51:17	INFO	SIImageStore::calcSensitivity 	[bb2.co76ci21/sci] Theoretical sensitivity (Jy/bm):c0:0.00014579 c1:0.00014579 c2:0.00014579 c3:0.00014579 c4:0.00014579 c5:0.000145791 c6:0.000145791 c7:0.000145791 c8:0.000145791 c9:0.000145791 c10:0.000145791 c11:0.000145792 c12:0.000145792 c13:0.000145791 c14:0.000145791 c15:0.000145791 c16:0.000145791 c17:0.000145791 c18:0.000145791 c19:0.000145792 c20:0.000145793 c21:0.000145793 c22:0.000145793 c23:0.000145793 c24:0.000145793 c25:0.000145793 c26:0.000145794 c27:0.000145794 c28:0.000145794 c29:0.000145794 c30:0.000145794 c31:0.000145794 c32:0.000145795 c33:0.000145796 c34:0.000145797 c35:0.000145797 c36:0.000145797 c37:0.000145797 c38:0.000145797 c39:0.000145797 c40:0.000145797 c41:0.000145798 c42:0.000145798 c43:0.000145798 c44:0.000145798 c45:0.000145798 c46:0.000145798 c47:0.000145798 c48:0.000145798 c49:0.000145799 c50:0.000145799 c51:0.000145799 c52:0.000145799 c53:0.000145799 c54:0.000145799 c55:0.000145799 c56:0.000145799 c57:0.000145799 c58:0.0001458 c59:0.0001458 c60:0.0001458 c61:0.000145801 c62:0.000145801 c63:0.000145801 c64:0.0001458 c65:0.000145801 c66:0.000145801 c67:0.000145801 c68:0.000145801 c69:0.000145801 c70:0.000145801 c71:0.000145802 c72:0.000145802 c73:0.000145802 c74:0.000145802 c75:0.000145802 c76:0.000145803 c77:0.000145803 c78:0.000145803 c79:0.000145804 c80:0.000145804 c81:0.000145804 c82:0.000145804 c83:0.000145804 c84:0.000145804 c85:0.000145804 c86:0.000145804 c87:0.000145804 c88:0.000145804 c89:0.000145804 c90:0.000145803 c91:0.000145804 c92:0.000145804 c93:0.000145805 c94:0.000145805 c95:0.000145805 c96:0.000145805 c97:0.000145805 c98:0.000145805 c99:0.000145805 c100:0.000145805 c101:0.000145805 c102:0.000145805 c103:0.000145805 c104:0.000145805 c105:0.000145805 c106:0.000145805 c107:0.000145806 c108:0.000145807 c109:0.000145807 c110:0.000145806 c111:0.000145806 c112:0.000145806 c113:0.000145807 c114:0.000145807 c115:0.000145807 c116:0.000145807 c117:0.000145807 c118:0.000145808 c119:0.000145808 c120:0.000145808 c121:0.000145808 c122:0.000145808 c123:0.000145808 c124:0.000145808 c125:0.000145808 c126:0.000145808 c127:0.000145808 c128:0.000145808 c129:0.000145808 c130:0.000145808 c131:0.000145808 c132:0.000145808 c133:0.000145809 c134:0.00014581 c135:0.00014581 c136:0.00014581 c137:0.00014581 c138:0.00014581 c139:0.00014581 c140:0.00014581 c141:0.00014581 c142:0.00014581 c143:0.00014581 c144:0.00014581 c145:0.00014581 c146:0.00014581 c147:0.00014581 c148:0.00014581 c149:0.00014581 c150:0.00014581 c151:0.00014581 c152:0.00014581 c153:0.00014581 c154:0.000145811 c155:0.000145811 c156:0.000145811 c157:0.000145811 c158:0.000145811 c159:0.000145811 c160:0.000145811 c161:0.000145811 c162:0.000145811 c163:0.000145811 c164:0.000145811 c165:0.000145811 c166:0.000145811 c167:0.000145811 c168:0.000145811 c169:0.000145812 c170:0.000145812 c171:0.000145812 c172:0.000145812 c173:0.000145812 c174:0.000145812 c175:0.000145812 c176:0.000145812 c177:0.000145812 c178:0.000145812 c179:0.000145812 c180:0.000145812 c181:0.000145812 c182:0.000145812 c183:0.000145812 c184:0.000145813 c185:0.000145813 c186:0.000145813 c187:0.000145814 c188:0.000145814 c189:0.000145814 c190:0.000145814 c191:0.000145814 c192:0.000145814 c193:0.000145814 c194:0.000145815 c195:0.000145815 c196:0.000145816 c197:0.000145816 c198:0.000145816 c199:0.000145816 c200:0.000145816 c201:0.000145816 c202:0.000145816 c203:0.000145816 c204:0.000145816 c205:0.000145816 c206:0.000145816 c207:0.000145816 c208:0.000145816 c209:0.000145817 c210:0.000145817 c211:0.000145817 c212:0.000145817 c213:0.000145817 c214:0.000145817 c215:0.000145817 c216:0.000145817 c217:0.000145817 c218:0.000145817 c219:0.000145817 c220:0.000145817 c221:0.000145817 c222:0.000145817 c223:0.000145818 c224:0.000145818 c225:0.000145818 c226:0.000145818 c227:0.000145818 c228:0.000145818 c229:0.000145818 c230:0.000145818 c231:0.000145818 c232:0.000145817 c233:0.000145817 c234:0.000145817 c235:0.000145818 c236:0.000145819 c237:0.000145819 
    2019-11-19 17:51:17	INFO	SIImageStore::printBeamSet 	Restoring Beams 
    2019-11-19 17:51:17	INFO	SIImageStore::printBeamSet +	Pol   Type Chan        Freq     Vel
    2019-11-19 17:51:17	INFO	SIImageStore::printBeamSet +	  I    Max    0 2.50753e+11 206759.30    0.3041 arcsec x    0.2743 arcsec pa= 38.0568 deg
    2019-11-19 17:51:17	INFO	SIImageStore::printBeamSet +	  I    Min  237 2.52604e+11 206072.40    0.3020 arcsec x    0.2723 arcsec pa= 38.0394 deg
    2019-11-19 17:51:17	INFO	SIImageStore::printBeamSet +	  I Median  118 2.51675e+11 206417.30    0.3031 arcsec x    0.2733 arcsec pa= 38.0571 deg
    2019-11-19 17:51:17	INFO	task_tclean::SynthesisImagerVi2::makePrimaryBeam 	vi2 : Evaluating Primary Beam model onto image grid(s)
    2019-11-19 17:51:18	INFO	task_tclean::SynthesisImager::executeMajorCycle 	----------------------------------------------------------- Run (Last) Major Cycle 1 -------------------------------------
    
    0%....10....20....30....40....50....60....70....80....90....100%
    2019-11-19 17:51:36	INFO	task_tclean::SDAlgorithmBase::restore 	[bb2.co76ci21/sci] : Restoring model image.
    2019-11-19 17:51:36	WARN	task_tclean::SIImageStore::restore (file casa-source/code/synthesis/ImagerObjects/SIImageStore.cc, line 2068)	Restoring with an empty model image. Only residuals will be processed to form the output restored image.
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 0 : 0.304148 arcsec, 0.274324 arcsec, 38.0568 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 1 : 0.30414 arcsec, 0.274314 arcsec, 38.0561 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 2 : 0.30413 arcsec, 0.274305 arcsec, 38.057 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 3 : 0.304121 arcsec, 0.274297 arcsec, 38.0558 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 4 : 0.304112 arcsec, 0.274289 arcsec, 38.0576 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 5 : 0.304104 arcsec, 0.27428 arcsec, 38.0574 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 6 : 0.304095 arcsec, 0.274271 arcsec, 38.058 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 7 : 0.304086 arcsec, 0.274263 arcsec, 38.0585 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 8 : 0.304078 arcsec, 0.274254 arcsec, 38.0595 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 9 : 0.304068 arcsec, 0.274245 arcsec, 38.0589 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 10 : 0.304058 arcsec, 0.274236 arcsec, 38.0598 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 11 : 0.304049 arcsec, 0.274227 arcsec, 38.0606 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 12 : 0.30404 arcsec, 0.274218 arcsec, 38.0608 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 13 : 0.304031 arcsec, 0.274209 arcsec, 38.0613 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 14 : 0.304021 arcsec, 0.274201 arcsec, 38.0609 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 15 : 0.304012 arcsec, 0.274193 arcsec, 38.061 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 16 : 0.304003 arcsec, 0.274185 arcsec, 38.0618 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 17 : 0.303994 arcsec, 0.274176 arcsec, 38.0619 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 18 : 0.303985 arcsec, 0.274167 arcsec, 38.062 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 19 : 0.303975 arcsec, 0.274158 arcsec, 38.0617 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 20 : 0.303966 arcsec, 0.274148 arcsec, 38.0616 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 21 : 0.303956 arcsec, 0.274139 arcsec, 38.0623 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 22 : 0.303947 arcsec, 0.274131 arcsec, 38.0625 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 23 : 0.303938 arcsec, 0.274122 arcsec, 38.0636 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 24 : 0.303929 arcsec, 0.274114 arcsec, 38.0636 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 25 : 0.30392 arcsec, 0.274106 arcsec, 38.0635 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 26 : 0.303909 arcsec, 0.274096 arcsec, 38.0626 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 27 : 0.3039 arcsec, 0.274087 arcsec, 38.0621 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 28 : 0.303891 arcsec, 0.274078 arcsec, 38.0628 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 29 : 0.303882 arcsec, 0.27407 arcsec, 38.0632 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 30 : 0.303873 arcsec, 0.274062 arcsec, 38.0638 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 31 : 0.303865 arcsec, 0.274054 arcsec, 38.0658 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 32 : 0.303855 arcsec, 0.274046 arcsec, 38.0657 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 33 : 0.303846 arcsec, 0.274037 arcsec, 38.0654 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 34 : 0.303836 arcsec, 0.274027 arcsec, 38.0665 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 35 : 0.303828 arcsec, 0.274019 arcsec, 38.0669 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 36 : 0.303819 arcsec, 0.27401 arcsec, 38.0671 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 37 : 0.303811 arcsec, 0.274003 arcsec, 38.0674 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 38 : 0.303801 arcsec, 0.273995 arcsec, 38.0679 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 39 : 0.303792 arcsec, 0.273986 arcsec, 38.0673 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 40 : 0.303783 arcsec, 0.273977 arcsec, 38.0666 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 41 : 0.303772 arcsec, 0.273967 arcsec, 38.0653 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 42 : 0.303762 arcsec, 0.273958 arcsec, 38.0641 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 43 : 0.303753 arcsec, 0.27395 arcsec, 38.0649 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 44 : 0.303742 arcsec, 0.273939 arcsec, 38.0616 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 45 : 0.303733 arcsec, 0.273931 arcsec, 38.0623 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 46 : 0.303724 arcsec, 0.273923 arcsec, 38.0634 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 47 : 0.303714 arcsec, 0.273915 arcsec, 38.064 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 48 : 0.303705 arcsec, 0.273906 arcsec, 38.0634 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 49 : 0.303696 arcsec, 0.273896 arcsec, 38.0628 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 50 : 0.303686 arcsec, 0.273887 arcsec, 38.0619 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 51 : 0.303677 arcsec, 0.273878 arcsec, 38.0633 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 52 : 0.303668 arcsec, 0.273868 arcsec, 38.0629 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 53 : 0.303659 arcsec, 0.27386 arcsec, 38.0616 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 54 : 0.30365 arcsec, 0.273851 arcsec, 38.0624 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 55 : 0.303641 arcsec, 0.273843 arcsec, 38.0639 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 56 : 0.303632 arcsec, 0.273835 arcsec, 38.0649 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 57 : 0.303624 arcsec, 0.273827 arcsec, 38.065 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 58 : 0.303614 arcsec, 0.273817 arcsec, 38.0656 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 59 : 0.303604 arcsec, 0.273807 arcsec, 38.0657 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 60 : 0.303594 arcsec, 0.273799 arcsec, 38.0659 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 61 : 0.303584 arcsec, 0.27379 arcsec, 38.0653 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 62 : 0.303575 arcsec, 0.273781 arcsec, 38.0639 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 63 : 0.303566 arcsec, 0.273772 arcsec, 38.063 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 64 : 0.303558 arcsec, 0.273765 arcsec, 38.0629 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 65 : 0.303548 arcsec, 0.273755 arcsec, 38.0641 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 66 : 0.303538 arcsec, 0.273746 arcsec, 38.0611 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 67 : 0.303528 arcsec, 0.273737 arcsec, 38.061 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 68 : 0.30352 arcsec, 0.273728 arcsec, 38.061 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 69 : 0.303512 arcsec, 0.27372 arcsec, 38.0619 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 70 : 0.303503 arcsec, 0.273712 arcsec, 38.0605 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 71 : 0.303493 arcsec, 0.273703 arcsec, 38.0611 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 72 : 0.303485 arcsec, 0.273694 arcsec, 38.0602 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 73 : 0.303475 arcsec, 0.273686 arcsec, 38.06 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 74 : 0.303466 arcsec, 0.273677 arcsec, 38.0603 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 75 : 0.303457 arcsec, 0.27367 arcsec, 38.0595 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 76 : 0.303448 arcsec, 0.273661 arcsec, 38.0605 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 77 : 0.303439 arcsec, 0.273652 arcsec, 38.0609 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 78 : 0.303428 arcsec, 0.273643 arcsec, 38.0607 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 79 : 0.303419 arcsec, 0.273634 arcsec, 38.06 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 80 : 0.30341 arcsec, 0.273626 arcsec, 38.0606 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 81 : 0.303401 arcsec, 0.273617 arcsec, 38.0603 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 82 : 0.303392 arcsec, 0.273608 arcsec, 38.0618 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 83 : 0.303383 arcsec, 0.273599 arcsec, 38.0616 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 84 : 0.303374 arcsec, 0.273591 arcsec, 38.0621 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 85 : 0.303364 arcsec, 0.273582 arcsec, 38.0642 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 86 : 0.303355 arcsec, 0.273574 arcsec, 38.0647 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 87 : 0.303346 arcsec, 0.273566 arcsec, 38.0645 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 88 : 0.303338 arcsec, 0.273558 arcsec, 38.064 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 89 : 0.303329 arcsec, 0.273549 arcsec, 38.0639 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 90 : 0.30332 arcsec, 0.27354 arcsec, 38.0627 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 91 : 0.303311 arcsec, 0.27353 arcsec, 38.0628 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 92 : 0.303302 arcsec, 0.273522 arcsec, 38.063 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 93 : 0.303291 arcsec, 0.273512 arcsec, 38.0633 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 94 : 0.303282 arcsec, 0.273504 arcsec, 38.0637 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 95 : 0.303272 arcsec, 0.273495 arcsec, 38.0637 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 96 : 0.303262 arcsec, 0.273487 arcsec, 38.0626 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 97 : 0.303253 arcsec, 0.273478 arcsec, 38.0625 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 98 : 0.303244 arcsec, 0.27347 arcsec, 38.0626 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 99 : 0.303236 arcsec, 0.273462 arcsec, 38.062 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 100 : 0.303226 arcsec, 0.273453 arcsec, 38.0612 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 101 : 0.303219 arcsec, 0.273444 arcsec, 38.0619 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 102 : 0.30321 arcsec, 0.273435 arcsec, 38.0617 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 103 : 0.303202 arcsec, 0.273428 arcsec, 38.0611 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 104 : 0.303192 arcsec, 0.273419 arcsec, 38.0609 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 105 : 0.303183 arcsec, 0.273409 arcsec, 38.0611 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 106 : 0.303174 arcsec, 0.273401 arcsec, 38.0594 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 107 : 0.303165 arcsec, 0.273391 arcsec, 38.0603 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 108 : 0.303155 arcsec, 0.273382 arcsec, 38.0589 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 109 : 0.303145 arcsec, 0.273374 arcsec, 38.0588 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 110 : 0.303137 arcsec, 0.273365 arcsec, 38.0577 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 111 : 0.303128 arcsec, 0.273357 arcsec, 38.058 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 112 : 0.303119 arcsec, 0.273349 arcsec, 38.0573 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 113 : 0.303109 arcsec, 0.273338 arcsec, 38.0569 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 114 : 0.3031 arcsec, 0.27333 arcsec, 38.0568 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 115 : 0.303091 arcsec, 0.273322 arcsec, 38.0556 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 116 : 0.30308 arcsec, 0.273314 arcsec, 38.0558 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 117 : 0.303071 arcsec, 0.273306 arcsec, 38.0553 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 118 : 0.303062 arcsec, 0.273296 arcsec, 38.0571 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 119 : 0.303053 arcsec, 0.273287 arcsec, 38.0567 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 120 : 0.303043 arcsec, 0.273278 arcsec, 38.0573 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 121 : 0.303034 arcsec, 0.27327 arcsec, 38.0564 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 122 : 0.303025 arcsec, 0.273262 arcsec, 38.0564 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 123 : 0.303015 arcsec, 0.273253 arcsec, 38.0562 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 124 : 0.303006 arcsec, 0.273244 arcsec, 38.0559 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 125 : 0.302998 arcsec, 0.273236 arcsec, 38.0547 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 126 : 0.302989 arcsec, 0.273227 arcsec, 38.0552 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 127 : 0.30298 arcsec, 0.273219 arcsec, 38.0546 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 128 : 0.302971 arcsec, 0.273209 arcsec, 38.0529 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 129 : 0.302964 arcsec, 0.2732 arcsec, 38.0535 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 130 : 0.302955 arcsec, 0.273192 arcsec, 38.0543 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 131 : 0.302946 arcsec, 0.273183 arcsec, 38.0531 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 132 : 0.302937 arcsec, 0.273174 arcsec, 38.0539 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 133 : 0.302929 arcsec, 0.273165 arcsec, 38.052 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 134 : 0.302919 arcsec, 0.273155 arcsec, 38.052 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 135 : 0.30291 arcsec, 0.273147 arcsec, 38.0521 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 136 : 0.302902 arcsec, 0.273138 arcsec, 38.052 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 137 : 0.302893 arcsec, 0.27313 arcsec, 38.0518 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 138 : 0.302883 arcsec, 0.273122 arcsec, 38.0526 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 139 : 0.302875 arcsec, 0.273114 arcsec, 38.0521 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 140 : 0.302865 arcsec, 0.273105 arcsec, 38.0513 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 141 : 0.302856 arcsec, 0.273096 arcsec, 38.0506 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 142 : 0.302847 arcsec, 0.273087 arcsec, 38.0503 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 143 : 0.302837 arcsec, 0.273078 arcsec, 38.0502 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 144 : 0.302828 arcsec, 0.27307 arcsec, 38.0498 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 145 : 0.302819 arcsec, 0.273062 arcsec, 38.0498 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 146 : 0.30281 arcsec, 0.273053 arcsec, 38.05 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 147 : 0.302801 arcsec, 0.273045 arcsec, 38.0504 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 148 : 0.302792 arcsec, 0.273037 arcsec, 38.0515 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 149 : 0.302782 arcsec, 0.273028 arcsec, 38.0503 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 150 : 0.302773 arcsec, 0.273019 arcsec, 38.0492 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 151 : 0.302764 arcsec, 0.27301 arcsec, 38.0486 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 152 : 0.302755 arcsec, 0.273003 arcsec, 38.0499 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 153 : 0.302746 arcsec, 0.272994 arcsec, 38.0486 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 154 : 0.302736 arcsec, 0.272984 arcsec, 38.0494 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 155 : 0.302727 arcsec, 0.272975 arcsec, 38.0479 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 156 : 0.302718 arcsec, 0.272968 arcsec, 38.0474 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 157 : 0.302709 arcsec, 0.272958 arcsec, 38.0484 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 158 : 0.3027 arcsec, 0.27295 arcsec, 38.0474 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 159 : 0.302692 arcsec, 0.27294 arcsec, 38.0496 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 160 : 0.302683 arcsec, 0.272932 arcsec, 38.049 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 161 : 0.302674 arcsec, 0.272923 arcsec, 38.0473 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 162 : 0.302665 arcsec, 0.272914 arcsec, 38.0467 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 163 : 0.302656 arcsec, 0.272906 arcsec, 38.046 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 164 : 0.302647 arcsec, 0.272897 arcsec, 38.046 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 165 : 0.302637 arcsec, 0.272888 arcsec, 38.0443 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 166 : 0.302628 arcsec, 0.27288 arcsec, 38.0438 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 167 : 0.302619 arcsec, 0.272871 arcsec, 38.0441 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 168 : 0.302611 arcsec, 0.272863 arcsec, 38.0449 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 169 : 0.302601 arcsec, 0.272854 arcsec, 38.0444 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 170 : 0.302593 arcsec, 0.272845 arcsec, 38.0431 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 171 : 0.302583 arcsec, 0.272837 arcsec, 38.0439 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 172 : 0.302574 arcsec, 0.272828 arcsec, 38.0442 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 173 : 0.302565 arcsec, 0.27282 arcsec, 38.0443 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 174 : 0.302556 arcsec, 0.272812 arcsec, 38.0437 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 175 : 0.302547 arcsec, 0.272804 arcsec, 38.0433 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 176 : 0.302537 arcsec, 0.272796 arcsec, 38.0445 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 177 : 0.302527 arcsec, 0.272787 arcsec, 38.0448 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 178 : 0.302519 arcsec, 0.272779 arcsec, 38.0453 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 179 : 0.30251 arcsec, 0.272771 arcsec, 38.0455 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 180 : 0.302501 arcsec, 0.272762 arcsec, 38.0457 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 181 : 0.302493 arcsec, 0.272754 arcsec, 38.0455 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 182 : 0.302484 arcsec, 0.272746 arcsec, 38.0443 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 183 : 0.302474 arcsec, 0.272736 arcsec, 38.0427 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 184 : 0.302463 arcsec, 0.272727 arcsec, 38.0428 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 185 : 0.302454 arcsec, 0.272718 arcsec, 38.0421 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 186 : 0.302445 arcsec, 0.272709 arcsec, 38.0406 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 187 : 0.302436 arcsec, 0.2727 arcsec, 38.0403 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 188 : 0.302427 arcsec, 0.272692 arcsec, 38.0404 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 189 : 0.302417 arcsec, 0.272682 arcsec, 38.0403 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 190 : 0.302409 arcsec, 0.272674 arcsec, 38.0408 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 191 : 0.302399 arcsec, 0.272665 arcsec, 38.0412 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 192 : 0.302392 arcsec, 0.272657 arcsec, 38.0405 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 193 : 0.302382 arcsec, 0.272649 arcsec, 38.0403 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 194 : 0.302372 arcsec, 0.272641 arcsec, 38.0405 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 195 : 0.302363 arcsec, 0.272632 arcsec, 38.0413 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 196 : 0.302353 arcsec, 0.272623 arcsec, 38.041 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 197 : 0.302344 arcsec, 0.272615 arcsec, 38.0422 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 198 : 0.302335 arcsec, 0.272606 arcsec, 38.042 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 199 : 0.302325 arcsec, 0.272598 arcsec, 38.0401 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 200 : 0.302317 arcsec, 0.27259 arcsec, 38.0406 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 201 : 0.302308 arcsec, 0.27258 arcsec, 38.0384 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 202 : 0.302299 arcsec, 0.272572 arcsec, 38.0384 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 203 : 0.30229 arcsec, 0.272564 arcsec, 38.0383 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 204 : 0.302281 arcsec, 0.272555 arcsec, 38.0395 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 205 : 0.302272 arcsec, 0.272547 arcsec, 38.0395 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 206 : 0.302263 arcsec, 0.272539 arcsec, 38.039 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 207 : 0.302255 arcsec, 0.27253 arcsec, 38.0383 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 208 : 0.302245 arcsec, 0.27252 arcsec, 38.0373 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 209 : 0.302235 arcsec, 0.272511 arcsec, 38.0377 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 210 : 0.302226 arcsec, 0.272503 arcsec, 38.0372 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 211 : 0.302217 arcsec, 0.272494 arcsec, 38.0365 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 212 : 0.302208 arcsec, 0.272486 arcsec, 38.036 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 213 : 0.302199 arcsec, 0.272477 arcsec, 38.0366 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 214 : 0.302191 arcsec, 0.272469 arcsec, 38.0386 deg
    2019-11-19 17:51:36	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 215 : 0.302182 arcsec, 0.272461 arcsec, 38.0388 deg
    2019-11-19 17:51:37	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 216 : 0.302173 arcsec, 0.272452 arcsec, 38.0378 deg
    2019-11-19 17:51:37	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 217 : 0.302164 arcsec, 0.272444 arcsec, 38.0376 deg
    2019-11-19 17:51:37	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 218 : 0.302155 arcsec, 0.272435 arcsec, 38.037 deg
    2019-11-19 17:51:37	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 219 : 0.302146 arcsec, 0.272427 arcsec, 38.037 deg
    2019-11-19 17:51:37	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 220 : 0.302136 arcsec, 0.272418 arcsec, 38.0362 deg
    2019-11-19 17:51:37	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 221 : 0.302126 arcsec, 0.272409 arcsec, 38.0359 deg
    2019-11-19 17:51:37	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 222 : 0.302116 arcsec, 0.272399 arcsec, 38.0363 deg
    2019-11-19 17:51:37	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 223 : 0.302106 arcsec, 0.272391 arcsec, 38.0356 deg
    2019-11-19 17:51:37	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 224 : 0.302096 arcsec, 0.272382 arcsec, 38.0354 deg
    2019-11-19 17:51:37	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 225 : 0.302087 arcsec, 0.272374 arcsec, 38.0362 deg
    2019-11-19 17:51:37	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 226 : 0.302079 arcsec, 0.272366 arcsec, 38.0373 deg
    2019-11-19 17:51:37	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 227 : 0.302071 arcsec, 0.272358 arcsec, 38.0375 deg
    2019-11-19 17:51:37	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 228 : 0.302063 arcsec, 0.27235 arcsec, 38.0368 deg
    2019-11-19 17:51:37	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 229 : 0.302054 arcsec, 0.272342 arcsec, 38.0371 deg
    2019-11-19 17:51:37	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 230 : 0.302045 arcsec, 0.272333 arcsec, 38.0366 deg
    2019-11-19 17:51:37	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 231 : 0.302037 arcsec, 0.272325 arcsec, 38.0377 deg
    2019-11-19 17:51:37	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 232 : 0.302028 arcsec, 0.272317 arcsec, 38.0387 deg
    2019-11-19 17:51:37	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 233 : 0.302019 arcsec, 0.272308 arcsec, 38.0381 deg
    2019-11-19 17:51:37	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 234 : 0.302011 arcsec, 0.2723 arcsec, 38.0375 deg
    2019-11-19 17:51:37	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 235 : 0.302 arcsec, 0.272291 arcsec, 38.0372 deg
    2019-11-19 17:51:37	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 236 : 0.301992 arcsec, 0.272283 arcsec, 38.038 deg
    2019-11-19 17:51:37	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 237 : 0.301983 arcsec, 0.272274 arcsec, 38.0394 deg
    2019-11-19 17:51:37	INFO	tclean::::casa	Result tclean: {}
    2019-11-19 17:51:37	INFO	tclean::::casa	Task tclean complete. Start time: 2019-11-19 11:50:59.610694 End time: 2019-11-19 11:51:36.644649
    2019-11-19 17:51:37	INFO	tclean::::casa	##### End Task: tclean               #####
    2019-11-19 17:51:37	INFO	tclean::::casa	##########################################
    2019-11-19 17:51:37	INFO	exportfits::::casa	##########################################
    2019-11-19 17:51:37	INFO	exportfits::::casa	##### Begin Task: exportfits         #####
    2019-11-19 17:51:37	INFO	exportfits::::casa	exportfits( imagename='bb2.co76ci21/sci.image', fitsimage='bb2.co76ci21/sci.fits', velocity=False, optical=False, bitpix=-32, minpix=0, maxpix=-1, overwrite=True, dropstokes=False, stokeslast=True, history=True, dropdeg=False )
    2019-11-19 17:51:37	INFO	exportfits::ImageFactory::toFITS	Applying mask of name 'mask0'
    2019-11-19 17:51:37	INFO	exportfits::ImageFitsConverter::ImageHeaderToFITS 	Truncating miscinfo field useweightimage to useweigh
    2019-11-19 17:51:37	INFO	exportfits::::casa	Result exportfits: None
    2019-11-19 17:51:37	INFO	exportfits::::casa	Task exportfits complete. Start time: 2019-11-19 11:51:36.648566 End time: 2019-11-19 11:51:36.757608
    2019-11-19 17:51:37	INFO	exportfits::::casa	##### End Task: exportfits           #####
    2019-11-19 17:51:37	INFO	exportfits::::casa	##########################################
    2019-11-19 17:51:40	INFO	tclean::::casa	##########################################
    2019-11-19 17:51:40	INFO	tclean::::casa	##### Begin Task: tclean             #####
    2019-11-19 17:51:40	INFO	tclean::::casa	tclean( vis='bb3.ms', selectdata=True, field='', spw='', timerange='', uvrange='', antenna='', scan='', observation='', intent='', datacolumn='data', imagename='bb3.h2o/sci', imsize=[64, 64], cell=0.05, phasecenter='', stokes='I', projection='SIN', startmodel='', specmode='cube', reffreq='', nchan=-1, start=0, width=1, outframe='LSRK', veltype='radio', restfreq=[], interpolation='nearest', perchanweightdensity=True, gridder='standard', facets=1, psfphasecenter='', chanchunks=1, wprojplanes=1, vptable='', mosweight=True, aterm=True, psterm=False, wbawp=True, conjbeams=False, cfcache='', usepointing=False, computepastep=360.0, rotatepastep=360.0, pointingoffsetsigdev=0.0, pblimit=0.2, normtype='flatnoise', deconvolver='hogbom', scales=[], nterms=2, smallscalebias=0.0, restoration=True, restoringbeam='', pbcor=False, outlierfile='', weighting='briggs', robust=1.0, noise='1.0Jy', npixels=0, uvtaper=[''], niter=0, gain=0.1, threshold=0.0, nsigma=0.0, cycleniter=-1, cyclefactor=1.0, minpsffraction=0.05, maxpsffraction=0.8, interactive=False, usemask='user', mask='', pbmask=0.0, sidelobethreshold=3.0, noisethreshold=5.0, lownoisethreshold=1.5, negativethreshold=0.0, smoothfactor=1.0, minbeamfrac=0.3, cutthreshold=0.01, growiterations=75, dogrowprune=True, minpercentchange=-1.0, verbose=False, fastnoise=True, restart=True, savemodel='none', calcres=True, calcpsf=True, parallel=False )
    2019-11-19 17:51:40	INFO	tclean::::casa	Verifying Input Parameters
    2019-11-19 17:51:40	INFO	SynthesisImagerVi2::selectData 	MS : bb3.ms | [Opened in readonly mode]
    2019-11-19 17:51:40	INFO	SynthesisImagerVi2::selectData 	  NRows selected : 53466
    2019-11-19 17:51:40	INFO	SynthesisImagerVi2::defineImage 	Define image coordinates for [bb3.h2o/sci] : 
    2019-11-19 17:51:40	INFO	MSTransformRegridder::calcChanFreqs	 phaseCenter='Direction: [0.973286, -0.0588581, 0.221923]'  *** Encountered negative channel widths in input spectral window.
    2019-11-19 17:51:40	INFO	MSTransformRegridder::calcChanFreqs	 Channels equidistant in freq
    2019-11-19 17:51:40	INFO	MSTransformRegridder::calcChanFreqs+	 Central frequency (in output frame) = 2.3418e+11 Hz
    2019-11-19 17:51:40	INFO	MSTransformRegridder::calcChanFreqs+	 Channel central frequency is decreasing with increasing channel number.
    2019-11-19 17:51:40	INFO	MSTransformRegridder::calcChanFreqs+	 Width of central channel (in output frame) = 7.81183e+06 Hz
    2019-11-19 17:51:40	INFO	MSTransformRegridder::calcChanFreqs+	 Number of channels = 238
    2019-11-19 17:51:40	INFO	MSTransformRegridder::calcChanFreqs+	 Total width of SPW (in output frame) = 1.85922e+09 Hz
    2019-11-19 17:51:40	INFO	MSTransformRegridder::calcChanFreqs+	 Lower edge = 2.3325e+11 Hz, upper edge = 2.3511e+11 Hz
    2019-11-19 17:51:40	INFO	SynthesisImagerVi2::defineImage 	Impars : start 0
    2019-11-19 17:51:40	INFO	SynthesisImagerVi2::defineImage 	Shape : [64, 64, 1, 238]Spectral : [2.35106e+11] at [0] with increment [-7.81183e+06]
    2019-11-19 17:51:40	INFO	SynthesisImagerVi2::defineImage 	Set Gridding options for [bb3.h2o/sci] with ftmachine : gridft
    2019-11-19 17:51:40	INFO	SynthesisImagerVi2::weight() 	Set imaging weights : Briggs weighting: sidelobes will be suppressed over full image
    2019-11-19 17:51:40	INFO	SynthesisImagerVi2::weight() 	Doing spectral cube Briggs weighting formula --  norm
    2019-11-19 17:51:40	INFO	SynthesisImager::tuneSelectData 	Tuning frequency data selection to match image spectral coordinates
    2019-11-19 17:51:40	INFO	SynthesisImagerVi2::selectData 	MS : bb3.ms | [Opened in readonly mode]
    2019-11-19 17:51:40	INFO	SynthesisImagerVi2::selectData 	  NRows selected : 53466
    2019-11-19 17:51:40	INFO	task_tclean::SynthesisDeconvolver::setupDeconvolution 	Set Deconvolution Options for [bb3.h2o/sci] : hogbom
    2019-11-19 17:51:40	INFO	SynthesisImager::makePSF 	----------------------------------------------------------- Make PSF ---------------------------------------------
    
    0%....10....20....30....40....50....60....70....80....90....100%
    2019-11-19 17:52:00	INFO	SIImageStore::calcSensitivity 	[bb3.h2o/sci] Theoretical sensitivity (Jy/bm):c0:0.000140174 c1:0.000140174 c2:0.000140174 c3:0.000140174 c4:0.000140174 c5:0.000140174 c6:0.000140175 c7:0.000140175 c8:0.000140175 c9:0.000140175 c10:0.000140175 c11:0.000140175 c12:0.000140175 c13:0.000140175 c14:0.000140174 c15:0.000140174 c16:0.000140174 c17:0.000140174 c18:0.000140174 c19:0.000140173 c20:0.000140173 c21:0.000140173 c22:0.000140173 c23:0.000140173 c24:0.000140173 c25:0.000140173 c26:0.000140173 c27:0.000140173 c28:0.000140173 c29:0.000140173 c30:0.000140173 c31:0.000140173 c32:0.000140174 c33:0.000140174 c34:0.000140173 c35:0.000140172 c36:0.000140172 c37:0.000140172 c38:0.000140172 c39:0.000140172 c40:0.000140172 c41:0.000140172 c42:0.000140172 c43:0.000140172 c44:0.000140172 c45:0.000140173 c46:0.000140173 c47:0.000140173 c48:0.000140173 c49:0.000140172 c50:0.000140172 c51:0.000140172 c52:0.000140172 c53:0.000140172 c54:0.000140172 c55:0.000140172 c56:0.000140172 c57:0.000140172 c58:0.000140172 c59:0.000140172 c60:0.000140172 c61:0.000140172 c62:0.000140172 c63:0.000140173 c64:0.000140173 c65:0.000140173 c66:0.000140173 c67:0.000140173 c68:0.000140173 c69:0.000140173 c70:0.000140173 c71:0.000140173 c72:0.000140173 c73:0.000140173 c74:0.000140172 c75:0.000140172 c76:0.000140173 c77:0.000140173 c78:0.000140173 c79:0.000140172 c80:0.000140172 c81:0.000140172 c82:0.000140173 c83:0.000140173 c84:0.000140173 c85:0.000140173 c86:0.000140173 c87:0.000140173 c88:0.000140172 c89:0.000140171 c90:0.000140172 c91:0.000140172 c92:0.000140172 c93:0.000140172 c94:0.000140172 c95:0.00014017 c96:0.00014017 c97:0.000140171 c98:0.00014017 c99:0.00014017 c100:0.00014017 c101:0.00014017 c102:0.000140169 c103:0.000140169 c104:0.00014017 c105:0.00014017 c106:0.00014017 c107:0.00014017 c108:0.00014017 c109:0.00014017 c110:0.00014017 c111:0.00014017 c112:0.00014017 c113:0.00014017 c114:0.00014017 c115:0.000140168 c116:0.000140167 c117:0.000140167 c118:0.000140167 c119:0.000140167 c120:0.000140168 c121:0.000140167 c122:0.000140167 c123:0.000140167 c124:0.000140167 c125:0.000140167 c126:0.000140167 c127:0.000140167 c128:0.000140167 c129:0.000140167 c130:0.000140167 c131:0.000140167 c132:0.000140166 c133:0.000140166 c134:0.000140166 c135:0.000140167 c136:0.000140167 c137:0.000140167 c138:0.000140166 c139:0.000140166 c140:0.000140166 c141:0.000140165 c142:0.000140166 c143:0.000140166 c144:0.000140166 c145:0.000140166 c146:0.000140166 c147:0.000140166 c148:0.000140166 c149:0.000140166 c150:0.000140166 c151:0.000140166 c152:0.000140166 c153:0.000140166 c154:0.000140166 c155:0.000140165 c156:0.000140165 c157:0.000140165 c158:0.000140165 c159:0.000140164 c160:0.000140164 c161:0.000140164 c162:0.000140164 c163:0.000140164 c164:0.000140164 c165:0.000140163 c166:0.000140163 c167:0.000140163 c168:0.000140163 c169:0.000140164 c170:0.000140164 c171:0.000140164 c172:0.000140164 c173:0.000140164 c174:0.000140163 c175:0.000140163 c176:0.000140163 c177:0.000140163 c178:0.000140163 c179:0.000140163 c180:0.000140163 c181:0.000140162 c182:0.000140162 c183:0.000140162 c184:0.000140163 c185:0.000140163 c186:0.000140163 c187:0.000140163 c188:0.000140163 c189:0.000140163 c190:0.000140162 c191:0.000140162 c192:0.000140163 c193:0.000140163 c194:0.000140163 c195:0.000140163 c196:0.000140163 c197:0.000140163 c198:0.000140163 c199:0.000140163 c200:0.000140162 c201:0.000140162 c202:0.000140163 c203:0.000140162 c204:0.000140162 c205:0.000140161 c206:0.000140161 c207:0.000140162 c208:0.000140161 c209:0.000140161 c210:0.000140162 c211:0.000140162 c212:0.000140161 c213:0.000140161 c214:0.000140161 c215:0.000140161 c216:0.000140161 c217:0.00014016 c218:0.00014016 c219:0.00014016 c220:0.00014016 c221:0.00014016 c222:0.00014016 c223:0.00014016 c224:0.00014016 c225:0.00014016 c226:0.00014016 c227:0.00014016 c228:0.000140161 c229:0.000140161 c230:0.00014016 c231:0.00014016 c232:0.00014016 c233:0.00014016 c234:0.00014016 c235:0.00014016 c236:0.00014016 c237:0.00014016 
    2019-11-19 17:52:01	INFO	SIImageStore::printBeamSet 	Restoring Beams 
    2019-11-19 17:52:01	INFO	SIImageStore::printBeamSet +	Pol   Type Chan         Freq     Vel
    2019-11-19 17:52:01	INFO	SIImageStore::printBeamSet +	  I    Max  237 2.332543e+11 206784.96    0.3222 arcsec x    0.2908 arcsec pa= 39.0330 deg
    2019-11-19 17:52:01	INFO	SIImageStore::printBeamSet +	  I    Min    1 2.350979e+11 206049.85    0.0000 arcsec x    0.0000 arcsec pa=  0.0000 deg
    2019-11-19 17:52:01	INFO	SIImageStore::printBeamSet +	  I Median  119 2.341761e+11 206417.41    0.3210 arcsec x    0.2897 arcsec pa= 39.0282 deg
    2019-11-19 17:52:01	INFO	task_tclean::SynthesisImagerVi2::makePrimaryBeam 	vi2 : Evaluating Primary Beam model onto image grid(s)
    2019-11-19 17:52:02	INFO	task_tclean::SynthesisImager::executeMajorCycle 	----------------------------------------------------------- Run (Last) Major Cycle 1 -------------------------------------
    
    0%....10....20....30....40....50....60....70....80....90....100%
    2019-11-19 17:52:19	INFO	task_tclean::SDAlgorithmBase::restore 	[bb3.h2o/sci] : Restoring model image.
    2019-11-19 17:52:19	WARN	task_tclean::SIImageStore::restore (file casa-source/code/synthesis/ImagerObjects/SIImageStore.cc, line 2068)	Restoring with an empty model image. Only residuals will be processed to form the output restored image.
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 0 : 0.319713 arcsec, 0.288505 arcsec, 39.0196 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 1 : 0.319724 arcsec, 0.288514 arcsec, 39.0208 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 2 : 0.319734 arcsec, 0.288524 arcsec, 39.0215 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 3 : 0.319745 arcsec, 0.288534 arcsec, 39.0222 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 4 : 0.319755 arcsec, 0.288543 arcsec, 39.0224 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 5 : 0.319765 arcsec, 0.288552 arcsec, 39.0227 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 6 : 0.319774 arcsec, 0.288563 arcsec, 39.0229 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 7 : 0.319786 arcsec, 0.288573 arcsec, 39.0228 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 8 : 0.319797 arcsec, 0.288583 arcsec, 39.0216 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 9 : 0.319808 arcsec, 0.288594 arcsec, 39.021 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 10 : 0.319818 arcsec, 0.288603 arcsec, 39.0215 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 11 : 0.319827 arcsec, 0.288613 arcsec, 39.0221 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 12 : 0.319838 arcsec, 0.288622 arcsec, 39.0225 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 13 : 0.319849 arcsec, 0.288633 arcsec, 39.0226 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 14 : 0.31986 arcsec, 0.288643 arcsec, 39.0235 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 15 : 0.31987 arcsec, 0.288653 arcsec, 39.0234 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 16 : 0.319881 arcsec, 0.288663 arcsec, 39.0238 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 17 : 0.319891 arcsec, 0.288672 arcsec, 39.0229 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 18 : 0.319901 arcsec, 0.288682 arcsec, 39.0226 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 19 : 0.319911 arcsec, 0.288692 arcsec, 39.0227 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 20 : 0.319922 arcsec, 0.288702 arcsec, 39.0227 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 21 : 0.319933 arcsec, 0.288711 arcsec, 39.0229 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 22 : 0.319943 arcsec, 0.28872 arcsec, 39.0235 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 23 : 0.319955 arcsec, 0.28873 arcsec, 39.0232 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 24 : 0.319965 arcsec, 0.28874 arcsec, 39.0232 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 25 : 0.319975 arcsec, 0.28875 arcsec, 39.0241 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 26 : 0.319986 arcsec, 0.288759 arcsec, 39.0244 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 27 : 0.319996 arcsec, 0.288768 arcsec, 39.0239 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 28 : 0.320007 arcsec, 0.288779 arcsec, 39.0236 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 29 : 0.320016 arcsec, 0.288788 arcsec, 39.0224 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 30 : 0.320027 arcsec, 0.288798 arcsec, 39.0215 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 31 : 0.320036 arcsec, 0.288807 arcsec, 39.02 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 32 : 0.320046 arcsec, 0.288816 arcsec, 39.0192 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 33 : 0.320056 arcsec, 0.288826 arcsec, 39.0192 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 34 : 0.320067 arcsec, 0.288836 arcsec, 39.0198 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 35 : 0.320079 arcsec, 0.288847 arcsec, 39.0204 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 36 : 0.320089 arcsec, 0.288857 arcsec, 39.0209 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 37 : 0.320099 arcsec, 0.288867 arcsec, 39.0223 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 38 : 0.320108 arcsec, 0.288876 arcsec, 39.0218 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 39 : 0.320119 arcsec, 0.288886 arcsec, 39.0217 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 40 : 0.320129 arcsec, 0.288895 arcsec, 39.0222 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 41 : 0.320139 arcsec, 0.288905 arcsec, 39.0219 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 42 : 0.320149 arcsec, 0.288914 arcsec, 39.022 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 43 : 0.320159 arcsec, 0.288924 arcsec, 39.0216 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 44 : 0.32017 arcsec, 0.288934 arcsec, 39.0212 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 45 : 0.320181 arcsec, 0.288943 arcsec, 39.0204 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 46 : 0.320191 arcsec, 0.288954 arcsec, 39.0215 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 47 : 0.320202 arcsec, 0.288963 arcsec, 39.0215 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 48 : 0.320213 arcsec, 0.288973 arcsec, 39.024 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 49 : 0.320223 arcsec, 0.288984 arcsec, 39.0237 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 50 : 0.320233 arcsec, 0.288994 arcsec, 39.0227 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 51 : 0.320243 arcsec, 0.289003 arcsec, 39.0228 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 52 : 0.320254 arcsec, 0.289013 arcsec, 39.0221 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 53 : 0.320264 arcsec, 0.289022 arcsec, 39.0221 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 54 : 0.320274 arcsec, 0.289033 arcsec, 39.0227 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 55 : 0.320285 arcsec, 0.289043 arcsec, 39.0216 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 56 : 0.320296 arcsec, 0.289053 arcsec, 39.0235 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 57 : 0.320306 arcsec, 0.289063 arcsec, 39.0243 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 58 : 0.320316 arcsec, 0.289072 arcsec, 39.0233 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 59 : 0.320325 arcsec, 0.289083 arcsec, 39.0239 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 60 : 0.320336 arcsec, 0.289092 arcsec, 39.0233 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 61 : 0.320346 arcsec, 0.289102 arcsec, 39.0245 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 62 : 0.320357 arcsec, 0.289112 arcsec, 39.0238 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 63 : 0.320368 arcsec, 0.289121 arcsec, 39.0221 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 64 : 0.320377 arcsec, 0.28913 arcsec, 39.0234 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 65 : 0.320387 arcsec, 0.289139 arcsec, 39.0244 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 66 : 0.320398 arcsec, 0.289149 arcsec, 39.0249 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 67 : 0.320408 arcsec, 0.289159 arcsec, 39.0259 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 68 : 0.320419 arcsec, 0.289169 arcsec, 39.0255 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 69 : 0.320429 arcsec, 0.289178 arcsec, 39.0251 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 70 : 0.32044 arcsec, 0.289189 arcsec, 39.0271 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 71 : 0.320449 arcsec, 0.289198 arcsec, 39.027 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 72 : 0.320459 arcsec, 0.289208 arcsec, 39.0284 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 73 : 0.32047 arcsec, 0.289216 arcsec, 39.0275 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 74 : 0.320481 arcsec, 0.289227 arcsec, 39.0265 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 75 : 0.32049 arcsec, 0.289236 arcsec, 39.0259 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 76 : 0.320502 arcsec, 0.289246 arcsec, 39.0267 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 77 : 0.320512 arcsec, 0.289256 arcsec, 39.0267 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 78 : 0.320522 arcsec, 0.289267 arcsec, 39.0274 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 79 : 0.320532 arcsec, 0.289277 arcsec, 39.0269 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 80 : 0.320542 arcsec, 0.289287 arcsec, 39.0281 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 81 : 0.320552 arcsec, 0.289297 arcsec, 39.0281 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 82 : 0.320563 arcsec, 0.289306 arcsec, 39.0274 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 83 : 0.320573 arcsec, 0.289316 arcsec, 39.0283 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 84 : 0.320583 arcsec, 0.289326 arcsec, 39.0268 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 85 : 0.320594 arcsec, 0.289336 arcsec, 39.0265 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 86 : 0.320604 arcsec, 0.289346 arcsec, 39.0291 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 87 : 0.320615 arcsec, 0.289356 arcsec, 39.0316 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 88 : 0.320626 arcsec, 0.289365 arcsec, 39.0309 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 89 : 0.320635 arcsec, 0.289374 arcsec, 39.0303 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 90 : 0.320646 arcsec, 0.289385 arcsec, 39.0302 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 91 : 0.320657 arcsec, 0.289394 arcsec, 39.0298 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 92 : 0.320667 arcsec, 0.289405 arcsec, 39.0294 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 93 : 0.320676 arcsec, 0.289414 arcsec, 39.0293 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 94 : 0.320686 arcsec, 0.289423 arcsec, 39.0294 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 95 : 0.320698 arcsec, 0.289433 arcsec, 39.0301 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 96 : 0.320708 arcsec, 0.289442 arcsec, 39.0289 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 97 : 0.320719 arcsec, 0.289452 arcsec, 39.0283 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 98 : 0.32073 arcsec, 0.289462 arcsec, 39.0291 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 99 : 0.32074 arcsec, 0.289472 arcsec, 39.0297 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 100 : 0.320751 arcsec, 0.289482 arcsec, 39.0301 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 101 : 0.320762 arcsec, 0.289491 arcsec, 39.0296 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 102 : 0.320773 arcsec, 0.289501 arcsec, 39.0289 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 103 : 0.320782 arcsec, 0.28951 arcsec, 39.0283 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 104 : 0.320793 arcsec, 0.289519 arcsec, 39.0294 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 105 : 0.320804 arcsec, 0.289529 arcsec, 39.0307 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 106 : 0.320815 arcsec, 0.289539 arcsec, 39.0308 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 107 : 0.320826 arcsec, 0.289549 arcsec, 39.03 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 108 : 0.320835 arcsec, 0.289558 arcsec, 39.029 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 109 : 0.320847 arcsec, 0.289567 arcsec, 39.0289 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 110 : 0.320859 arcsec, 0.289577 arcsec, 39.0311 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 111 : 0.320869 arcsec, 0.289586 arcsec, 39.0311 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 112 : 0.320879 arcsec, 0.289595 arcsec, 39.0301 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 113 : 0.320889 arcsec, 0.289604 arcsec, 39.031 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 114 : 0.320898 arcsec, 0.289614 arcsec, 39.0315 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 115 : 0.320909 arcsec, 0.289624 arcsec, 39.0308 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 116 : 0.320921 arcsec, 0.289636 arcsec, 39.0301 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 117 : 0.32093 arcsec, 0.289645 arcsec, 39.0304 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 118 : 0.320941 arcsec, 0.289654 arcsec, 39.0294 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 119 : 0.320951 arcsec, 0.289663 arcsec, 39.0282 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 120 : 0.320961 arcsec, 0.289673 arcsec, 39.0285 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 121 : 0.320972 arcsec, 0.289682 arcsec, 39.0294 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 122 : 0.320983 arcsec, 0.289692 arcsec, 39.0305 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 123 : 0.320993 arcsec, 0.289702 arcsec, 39.0307 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 124 : 0.321004 arcsec, 0.289712 arcsec, 39.0304 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 125 : 0.321014 arcsec, 0.289721 arcsec, 39.0312 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 126 : 0.321026 arcsec, 0.289731 arcsec, 39.0282 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 127 : 0.321036 arcsec, 0.289741 arcsec, 39.0266 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 128 : 0.321047 arcsec, 0.289751 arcsec, 39.0255 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 129 : 0.321058 arcsec, 0.289761 arcsec, 39.0233 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 130 : 0.321068 arcsec, 0.28977 arcsec, 39.0232 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 131 : 0.321079 arcsec, 0.28978 arcsec, 39.0231 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 132 : 0.321089 arcsec, 0.28979 arcsec, 39.0248 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 133 : 0.321101 arcsec, 0.2898 arcsec, 39.0233 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 134 : 0.321112 arcsec, 0.289811 arcsec, 39.0212 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 135 : 0.321122 arcsec, 0.289821 arcsec, 39.0193 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 136 : 0.321133 arcsec, 0.289832 arcsec, 39.0196 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 137 : 0.321142 arcsec, 0.289841 arcsec, 39.0201 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 138 : 0.321153 arcsec, 0.289851 arcsec, 39.0193 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 139 : 0.321164 arcsec, 0.289861 arcsec, 39.0186 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 140 : 0.321174 arcsec, 0.289871 arcsec, 39.0192 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 141 : 0.321185 arcsec, 0.289882 arcsec, 39.0204 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 142 : 0.321194 arcsec, 0.28989 arcsec, 39.0193 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 143 : 0.321205 arcsec, 0.289901 arcsec, 39.0193 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 144 : 0.321215 arcsec, 0.28991 arcsec, 39.021 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 145 : 0.321226 arcsec, 0.28992 arcsec, 39.021 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 146 : 0.321236 arcsec, 0.28993 arcsec, 39.0194 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 147 : 0.321246 arcsec, 0.289939 arcsec, 39.019 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 148 : 0.321257 arcsec, 0.289949 arcsec, 39.0205 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 149 : 0.321267 arcsec, 0.28996 arcsec, 39.0219 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 150 : 0.321278 arcsec, 0.289969 arcsec, 39.0232 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 151 : 0.321288 arcsec, 0.289979 arcsec, 39.0233 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 152 : 0.321298 arcsec, 0.28999 arcsec, 39.0228 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 153 : 0.321308 arcsec, 0.289999 arcsec, 39.0235 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 154 : 0.321321 arcsec, 0.290009 arcsec, 39.0238 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 155 : 0.321331 arcsec, 0.290019 arcsec, 39.0237 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 156 : 0.321341 arcsec, 0.290029 arcsec, 39.0235 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 157 : 0.321351 arcsec, 0.290039 arcsec, 39.0232 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 158 : 0.321362 arcsec, 0.290049 arcsec, 39.0251 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 159 : 0.321373 arcsec, 0.290059 arcsec, 39.0248 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 160 : 0.321385 arcsec, 0.290068 arcsec, 39.024 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 161 : 0.321394 arcsec, 0.290077 arcsec, 39.0246 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 162 : 0.321403 arcsec, 0.290086 arcsec, 39.0246 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 163 : 0.321413 arcsec, 0.290096 arcsec, 39.024 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 164 : 0.321424 arcsec, 0.290106 arcsec, 39.0258 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 165 : 0.321433 arcsec, 0.290116 arcsec, 39.0264 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 166 : 0.321444 arcsec, 0.290126 arcsec, 39.0265 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 167 : 0.321455 arcsec, 0.290136 arcsec, 39.028 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 168 : 0.321465 arcsec, 0.290145 arcsec, 39.0294 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 169 : 0.321476 arcsec, 0.290155 arcsec, 39.0318 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 170 : 0.321488 arcsec, 0.290165 arcsec, 39.0338 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 171 : 0.321499 arcsec, 0.290175 arcsec, 39.0331 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 172 : 0.321509 arcsec, 0.290185 arcsec, 39.0324 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 173 : 0.32152 arcsec, 0.290196 arcsec, 39.0338 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 174 : 0.321532 arcsec, 0.290207 arcsec, 39.0342 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 175 : 0.321542 arcsec, 0.290217 arcsec, 39.0345 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 176 : 0.321552 arcsec, 0.290226 arcsec, 39.0348 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 177 : 0.321563 arcsec, 0.290236 arcsec, 39.0348 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 178 : 0.321573 arcsec, 0.290245 arcsec, 39.0347 deg
    2019-11-19 17:52:19	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 179 : 0.321584 arcsec, 0.290256 arcsec, 39.0344 deg
    2019-11-19 17:52:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 180 : 0.321594 arcsec, 0.290265 arcsec, 39.0349 deg
    2019-11-19 17:52:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 181 : 0.321605 arcsec, 0.290275 arcsec, 39.0359 deg
    2019-11-19 17:52:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 182 : 0.321616 arcsec, 0.290285 arcsec, 39.0358 deg
    2019-11-19 17:52:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 183 : 0.321626 arcsec, 0.290294 arcsec, 39.0344 deg
    2019-11-19 17:52:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 184 : 0.321637 arcsec, 0.290303 arcsec, 39.0337 deg
    2019-11-19 17:52:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 185 : 0.321648 arcsec, 0.290313 arcsec, 39.0363 deg
    2019-11-19 17:52:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 186 : 0.321659 arcsec, 0.290323 arcsec, 39.0356 deg
    2019-11-19 17:52:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 187 : 0.321669 arcsec, 0.290331 arcsec, 39.0344 deg
    2019-11-19 17:52:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 188 : 0.321679 arcsec, 0.290342 arcsec, 39.0344 deg
    2019-11-19 17:52:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 189 : 0.32169 arcsec, 0.290352 arcsec, 39.0343 deg
    2019-11-19 17:52:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 190 : 0.321701 arcsec, 0.290362 arcsec, 39.0344 deg
    2019-11-19 17:52:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 191 : 0.321711 arcsec, 0.290371 arcsec, 39.0338 deg
    2019-11-19 17:52:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 192 : 0.321721 arcsec, 0.290382 arcsec, 39.0335 deg
    2019-11-19 17:52:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 193 : 0.321732 arcsec, 0.290392 arcsec, 39.0325 deg
    2019-11-19 17:52:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 194 : 0.321743 arcsec, 0.290402 arcsec, 39.0337 deg
    2019-11-19 17:52:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 195 : 0.321754 arcsec, 0.290412 arcsec, 39.0338 deg
    2019-11-19 17:52:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 196 : 0.321764 arcsec, 0.29042 arcsec, 39.0338 deg
    2019-11-19 17:52:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 197 : 0.321773 arcsec, 0.29043 arcsec, 39.0329 deg
    2019-11-19 17:52:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 198 : 0.321783 arcsec, 0.29044 arcsec, 39.0326 deg
    2019-11-19 17:52:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 199 : 0.321793 arcsec, 0.29045 arcsec, 39.0329 deg
    2019-11-19 17:52:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 200 : 0.321804 arcsec, 0.290459 arcsec, 39.0325 deg
    2019-11-19 17:52:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 201 : 0.321813 arcsec, 0.290469 arcsec, 39.0344 deg
    2019-11-19 17:52:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 202 : 0.321824 arcsec, 0.290479 arcsec, 39.0342 deg
    2019-11-19 17:52:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 203 : 0.321835 arcsec, 0.290489 arcsec, 39.0343 deg
    2019-11-19 17:52:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 204 : 0.321846 arcsec, 0.290498 arcsec, 39.034 deg
    2019-11-19 17:52:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 205 : 0.321856 arcsec, 0.290509 arcsec, 39.0348 deg
    2019-11-19 17:52:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 206 : 0.321866 arcsec, 0.290519 arcsec, 39.0342 deg
    2019-11-19 17:52:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 207 : 0.321875 arcsec, 0.290528 arcsec, 39.0348 deg
    2019-11-19 17:52:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 208 : 0.321886 arcsec, 0.290538 arcsec, 39.034 deg
    2019-11-19 17:52:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 209 : 0.321896 arcsec, 0.290549 arcsec, 39.0352 deg
    2019-11-19 17:52:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 210 : 0.321905 arcsec, 0.290559 arcsec, 39.0343 deg
    2019-11-19 17:52:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 211 : 0.321916 arcsec, 0.290569 arcsec, 39.0337 deg
    2019-11-19 17:52:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 212 : 0.321926 arcsec, 0.290581 arcsec, 39.0354 deg
    2019-11-19 17:52:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 213 : 0.321936 arcsec, 0.290591 arcsec, 39.0348 deg
    2019-11-19 17:52:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 214 : 0.321946 arcsec, 0.2906 arcsec, 39.0346 deg
    2019-11-19 17:52:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 215 : 0.321956 arcsec, 0.29061 arcsec, 39.0335 deg
    2019-11-19 17:52:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 216 : 0.321968 arcsec, 0.290619 arcsec, 39.0331 deg
    2019-11-19 17:52:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 217 : 0.321978 arcsec, 0.290629 arcsec, 39.0328 deg
    2019-11-19 17:52:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 218 : 0.321989 arcsec, 0.290639 arcsec, 39.0314 deg
    2019-11-19 17:52:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 219 : 0.322 arcsec, 0.290649 arcsec, 39.0321 deg
    2019-11-19 17:52:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 220 : 0.32201 arcsec, 0.290657 arcsec, 39.0323 deg
    2019-11-19 17:52:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 221 : 0.322019 arcsec, 0.290666 arcsec, 39.0317 deg
    2019-11-19 17:52:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 222 : 0.32203 arcsec, 0.290676 arcsec, 39.0322 deg
    2019-11-19 17:52:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 223 : 0.32204 arcsec, 0.290685 arcsec, 39.0326 deg
    2019-11-19 17:52:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 224 : 0.32205 arcsec, 0.290694 arcsec, 39.0312 deg
    2019-11-19 17:52:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 225 : 0.322061 arcsec, 0.290705 arcsec, 39.0303 deg
    2019-11-19 17:52:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 226 : 0.322071 arcsec, 0.290714 arcsec, 39.0302 deg
    2019-11-19 17:52:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 227 : 0.322081 arcsec, 0.290724 arcsec, 39.0304 deg
    2019-11-19 17:52:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 228 : 0.322092 arcsec, 0.290734 arcsec, 39.0311 deg
    2019-11-19 17:52:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 229 : 0.322102 arcsec, 0.290742 arcsec, 39.0304 deg
    2019-11-19 17:52:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 230 : 0.322113 arcsec, 0.290753 arcsec, 39.0314 deg
    2019-11-19 17:52:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 231 : 0.322123 arcsec, 0.290763 arcsec, 39.0316 deg
    2019-11-19 17:52:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 232 : 0.322132 arcsec, 0.290773 arcsec, 39.0312 deg
    2019-11-19 17:52:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 233 : 0.322143 arcsec, 0.290783 arcsec, 39.0329 deg
    2019-11-19 17:52:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 234 : 0.322153 arcsec, 0.290793 arcsec, 39.0337 deg
    2019-11-19 17:52:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 235 : 0.322163 arcsec, 0.290805 arcsec, 39.0342 deg
    2019-11-19 17:52:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 236 : 0.322172 arcsec, 0.290814 arcsec, 39.0337 deg
    2019-11-19 17:52:20	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 237 : 0.322183 arcsec, 0.290822 arcsec, 39.033 deg
    2019-11-19 17:52:20	INFO	tclean::::casa	Result tclean: {}
    2019-11-19 17:52:20	INFO	tclean::::casa	Task tclean complete. Start time: 2019-11-19 11:51:39.562540 End time: 2019-11-19 11:52:19.731154
    2019-11-19 17:52:20	INFO	tclean::::casa	##### End Task: tclean               #####
    2019-11-19 17:52:20	INFO	tclean::::casa	##########################################
    2019-11-19 17:52:20	INFO	exportfits::::casa	##########################################
    2019-11-19 17:52:20	INFO	exportfits::::casa	##### Begin Task: exportfits         #####
    2019-11-19 17:52:20	INFO	exportfits::::casa	exportfits( imagename='bb3.h2o/sci.image', fitsimage='bb3.h2o/sci.fits', velocity=False, optical=False, bitpix=-32, minpix=0, maxpix=-1, overwrite=True, dropstokes=False, stokeslast=True, history=True, dropdeg=False )
    2019-11-19 17:52:20	INFO	exportfits::ImageFactory::toFITS	Applying mask of name 'mask0'
    2019-11-19 17:52:20	INFO	exportfits::ImageFitsConverter::ImageHeaderToFITS 	Truncating miscinfo field useweightimage to useweigh
    2019-11-19 17:52:20	INFO	exportfits::::casa	Result exportfits: None
    2019-11-19 17:52:20	INFO	exportfits::::casa	Task exportfits complete. Start time: 2019-11-19 11:52:19.734872 End time: 2019-11-19 11:52:19.814326
    2019-11-19 17:52:20	INFO	exportfits::::casa	##### End Task: exportfits           #####
    2019-11-19 17:52:20	INFO	exportfits::::casa	##########################################
    2019-11-19 17:52:22	INFO	tclean::::casa	##########################################
    2019-11-19 17:52:22	INFO	tclean::::casa	##### Begin Task: tclean             #####
    2019-11-19 17:52:22	INFO	tclean::::casa	tclean( vis=['bb1.ms.mfs', 'bb4.ms.mfs'], selectdata=True, field='', spw='', timerange='', uvrange='', antenna='', scan='', observation='', intent='', datacolumn='data', imagename='bb14.cont/sci', imsize=[64, 64], cell=0.05, phasecenter='', stokes='I', projection='SIN', startmodel='', specmode='mfs', reffreq='', nchan=-1, start=0, width=1, outframe='LSRK', veltype='radio', restfreq=[], interpolation='nearest', perchanweightdensity=True, gridder='standard', facets=1, psfphasecenter='', chanchunks=1, wprojplanes=1, vptable='', mosweight=True, aterm=True, psterm=False, wbawp=True, conjbeams=False, cfcache='', usepointing=False, computepastep=360.0, rotatepastep=360.0, pointingoffsetsigdev=0.0, pblimit=0.2, normtype='flatnoise', deconvolver='hogbom', scales=[], nterms=2, smallscalebias=0.0, restoration=True, restoringbeam='', pbcor=False, outlierfile='', weighting='briggs', robust=1.0, noise='1.0Jy', npixels=0, uvtaper=[''], niter=0, gain=0.1, threshold=0.0, nsigma=0.0, cycleniter=-1, cyclefactor=1.0, minpsffraction=0.05, maxpsffraction=0.8, interactive=False, usemask='user', mask='', pbmask=0.0, sidelobethreshold=3.0, noisethreshold=5.0, lownoisethreshold=1.5, negativethreshold=0.0, smoothfactor=1.0, minbeamfrac=0.3, cutthreshold=0.01, growiterations=75, dogrowprune=True, minpercentchange=-1.0, verbose=False, fastnoise=True, restart=True, savemodel='none', calcres=True, calcpsf=True, parallel=False )
    2019-11-19 17:52:22	INFO	tclean::::casa	Verifying Input Parameters
    2019-11-19 17:52:22	INFO	SynthesisImagerVi2::selectData 	MS : bb1.ms.mfs | [Opened in readonly mode]
    2019-11-19 17:52:22	INFO	SynthesisImagerVi2::selectData 	  NRows selected : 56354
    2019-11-19 17:52:22	INFO	SynthesisImagerVi2::selectData 	MS : bb4.ms.mfs | [Opened in readonly mode]
    2019-11-19 17:52:22	INFO	SynthesisImagerVi2::selectData 	  NRows selected : 56354
    2019-11-19 17:52:22	INFO	SynthesisImagerVi2::defineImage 	Define image coordinates for [bb14.cont/sci] : 
    2019-11-19 17:52:22	INFO	SynthesisImagerVi2::defineImage 	Impars : start 0
    2019-11-19 17:52:22	INFO	SynthesisImagerVi2::defineImage 	Shape : [64, 64, 1, 1]Spectral : [2.42977e+11] at [0] with increment [1.60527e+10]
    2019-11-19 17:52:22	INFO	SynthesisImagerVi2::defineImage 	Set Gridding options for [bb14.cont/sci] with ftmachine : gridft
    2019-11-19 17:52:22	INFO	SynthesisImagerVi2::weight() 	Set imaging weights : Briggs weighting: sidelobes will be suppressed over full image
    2019-11-19 17:52:23	INFO	VisSetUtil::VisImagingWeight() 	Normal robustness, robust = 1
    2019-11-19 17:52:23	INFO	task_tclean::SynthesisDeconvolver::setupDeconvolution 	Set Deconvolution Options for [bb14.cont/sci] : hogbom
    2019-11-19 17:52:23	INFO	SynthesisImager::makePSF 	----------------------------------------------------------- Make PSF ---------------------------------------------
    2019-11-19 17:52:23	INFO	SIImageStore::calcSensitivity 	[bb14.cont/sci] Theoretical sensitivity (Jy/bm):6.89133e-06 
    2019-11-19 17:52:23	INFO	SIImageStore::printBeamSet 	Beam : 0.303935 arcsec, 0.274494 arcsec, 38.5598 deg
    2019-11-19 17:52:23	INFO	task_tclean::SynthesisImagerVi2::makePrimaryBeam 	vi2 : Evaluating Primary Beam model onto image grid(s)
    2019-11-19 17:52:23	INFO	task_tclean::SynthesisImager::executeMajorCycle 	----------------------------------------------------------- Run (Last) Major Cycle 1 -------------------------------------
    2019-11-19 17:52:24	INFO	task_tclean::SDAlgorithmBase::restore 	[bb14.cont/sci] : Restoring model image.
    2019-11-19 17:52:24	WARN	task_tclean::SIImageStore::restore (file casa-source/code/synthesis/ImagerObjects/SIImageStore.cc, line 2068)	Restoring with an empty model image. Only residuals will be processed to form the output restored image.
    2019-11-19 17:52:24	INFO	task_tclean::SIImageStore::restore 	Beam for chan : 0 : 0.303935 arcsec, 0.274494 arcsec, 38.5598 deg
    2019-11-19 17:52:24	INFO	tclean::::casa	Result tclean: {}
    2019-11-19 17:52:24	INFO	tclean::::casa	Task tclean complete. Start time: 2019-11-19 11:52:22.198773 End time: 2019-11-19 11:52:23.899755
    2019-11-19 17:52:24	INFO	tclean::::casa	##### End Task: tclean               #####
    2019-11-19 17:52:24	INFO	tclean::::casa	##########################################
    2019-11-19 17:52:24	INFO	exportfits::::casa	##########################################
    2019-11-19 17:52:24	INFO	exportfits::::casa	##### Begin Task: exportfits         #####
    2019-11-19 17:52:24	INFO	exportfits::::casa	exportfits( imagename='bb14.cont/sci.image', fitsimage='bb14.cont/sci.fits', velocity=False, optical=False, bitpix=-32, minpix=0, maxpix=-1, overwrite=True, dropstokes=False, stokeslast=True, history=True, dropdeg=False )
    2019-11-19 17:52:24	INFO	exportfits::ImageFactory::toFITS	Applying mask of name 'mask0'
    2019-11-19 17:52:24	INFO	exportfits::ImageFitsConverter::ImageHeaderToFITS 	Truncating miscinfo field useweightimage to useweigh
    2019-11-19 17:52:24	INFO	exportfits::::casa	Result exportfits: None
    2019-11-19 17:52:24	INFO	exportfits::::casa	Task exportfits complete. Start time: 2019-11-19 11:52:23.902650 End time: 2019-11-19 11:52:23.911984
    2019-11-19 17:52:24	INFO	exportfits::::casa	##### End Task: exportfits           #####
    2019-11-19 17:52:24	INFO	exportfits::::casa	##########################################


