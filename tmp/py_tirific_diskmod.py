imlist=['CICO76']
lines=['CO76,CI']
objects=['s1,s2,s3,s4']

disks=py_tirific_mc_setup_hxmm01_disks()
#disks[0]['esbr']=[28.0,11.0]
#disks[3]['esbr']=[4.4,40.0]
#disks[3]['inc']=0.0
#disks[0]['inc']=0.0

imsets,data=py_tirific_mc_setup_hxmm01_imsets(imlist,lines,objects)

imset=deepcopy(imsets['CICO76'])
imset['outfolder']='test'
imset['cflux_scale']=1e-7
imset['outname']='diskmod'

tirific_diskmod(imset,disks,verbose=True,decomp=True,ppp=False)

#imset['outname']='dismod_sm'
#imset['COOLBEAM']=0.1
#tirific_diskmod(imset,[disks[0],disks[3]],verbose=True,decomp=True)

#imset['outname']='dismod_na'
#imset['BMIN']=0.0   ;   imset['BMAJ']=0.0
#imset['COOLBEAM']=0.0
#tirific_diskmod(imset,[disks[0],disks[3]],verbose=True,decomp=True)



