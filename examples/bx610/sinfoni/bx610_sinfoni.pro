PRO BX610_SINFONI


repo='/Users/Rui/Dropbox/Workspace/repo/SINS-ZCSINF_AO_release/'
outdir='/Users/Rui/Dropbox/Worklib/projects/GMaKE/examples/bx610/sinfoni/'

filename=repo+'Q2343-BX610_K100_08h20_PA+20_data_cut.fits'
pa=+20
im=readfits(filename,hd)


hrot3d,im,hd,newim,newhd,-pa,$
    sxpar(hd,'CRPIX1')-1,sxpar(hd,'CRPIX2')-1,$
    missing=!values.f_nan,interp=2,cubic=-0.5,/pivot
newim[where(abs(newim) gt 1e-10,/null)]=!values.f_nan

;SXADDPAR, newhd, 'BUNIT', 'SNR', before='HISTORY'
;https://arxiv.org/pdf/astro-ph/0207407.pdf


SXDELPAR,newhd,'CROTA1'
SXDELPAR,newhd,'CROTA2'
sxaddpar,newhd,'CDELT1',-0.05/3600
sxaddpar,newhd,'CDELT2',0.05/3600
get_coords,radec,instring='23:46:09.4 +12:49:19'
radec[0]=radec[0]*360./24
sxaddpar,newhd,'CRVAL1',radec[0]
sxaddpar,newhd,'CRVAL2',radec[1]

sxaddpar,newhd,'CTYPE1','RA---TAN', before='HISTORY'
sxaddpar,newhd,'CTYPE2','DEC--TAN', before='HISTORY'
sxaddpar,newhd,'CUNIT1','deg     ', before='HISTORY'
sxaddpar,newhd,'CUNIT2','deg     ', before='HISTORY'

; W/m^2/pixel/um
; ->cc *  1e-18 erg/s/cm^2/pixel/angstrom
cc=1e7/1e4/1e4*1e18

sxaddpar,newhd,'CUNIT3','angstrom'
sxaddpar,newhd,'CDELT3',sxpar(newhd,'CDELT3')*1e4
sxaddpar,newhd,'CRVAL3',sxpar(newhd,'CRVAL3')*1e4
SXADDPAR, newhd, 'DATAMAX', max(newim*cc,/nan), before='HISTORY'
SXADDPAR, newhd, 'DATAMIN', min(newim*cc,/nan), before='HISTORY'
sxaddpar,newhd,'BUNIT','1e-18 erg/s/cm^2/angstrom/pixel', before='HISTORY'
writefits,outdir+'bx610_data.fits',newim*cc,newhd

mask=(1-float(newim eq newim))
mask[*,*,0:442]=1.0
mask[*,*,539:-1]=1.0
writefits,outdir+'bx610_mask.fits',mask,newhd

print,filename,'-->',outdir+'bx610_data.fits'



filename=repo+'Q2343-BX610_K100_08h20_PA+20_noise_cut.fits'
em=readfits(filename,emhd)

hrot3d,em,emhd,newem,newemhd,-pa,$
    sxpar(hd,'CRPIX1')-1,sxpar(hd,'CRPIX2')-1,$
    missing=!values.f_nan,interp=2,cubic=-0.5,/pivot
writefits,outdir+'bx610_noise.fits',newem*cc,newhd


filename=repo+'Q2343-BX610_K100_08h20_PA+20_psf.fits'
psf=readfits(filename,psfhd)
tmp=max(psf,ind)
ind2d=array_indices(psf,ind)

hrot3d,psf,psfhd,newpsf,newpsfhd,-pa,$
    ind2d[0],ind2d[1],$
    missing=!values.f_nan,interp=2,cubic=-0.5,/pivot

psfhd=mk_hd(radec,[64,64],0.05)

small_psf=newpsf[(ind2d[0]-32):(ind2d[0]+31),(ind2d[1]-32):(ind2d[1]+31)]
dist_circle,dist_psf,64,32,32
tag=where(dist_psf gt 24)
back_value=median(small_psf[tag])
small_psf-=back_value
small_psf[where(small_psf ne small_psf,/null)]=0.0

small_psf=small_psf/total(small_psf)
writefits,outdir+'bx610_psf.fits',$
    small_psf,$
    psfhd
;Q2343-BX610_K100_08h20_PA+20_psf.fits
;Q2343-BX610_K100_08h20_PA+20_noise.fits
;Q2343-BX610_K100_08h20_PA+20_data_cut.fits
;Q2343-BX610_K100_08h20_PA+20_noise_cut.fits

END