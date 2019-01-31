PRO HZDYN_SUBREG_BX610_2015

export_dir='/Volumes/D1/projects/hzdyn/2015.1.00250.S/science_goal.uid___A001_X2fe_X20d/group.uid___A001_X2fe_X20e/member.uid___A001_X2fe_X20f/export/'


input=['uid___A001_X2fe_X20f_target.spw25.cube.I.iter0.residual.fits',$
'uid___A001_X2fe_X20f_target.spw27.cube.I.iter0.residual.fits',$
'uid___A001_X2fe_X20f_target.spw29.cube.I.iter0.residual.fits',$
'uid___A001_X2fe_X20f_target.spw31.cube.I.iter0.residual.fits']
output_tag=['spw25','spw27','spw29','spw31']

for i=0,n_elements(input)-1 do begin
    im=readfits(export_dir+input[i],hd)
    hextractx,im,hd,subim,subhd,[-1.,1.]*2.0,[-1.,1.]*2.0,radec=[356.53929,12.822]
    writefits,'bx610_'+output_tag[i]+'.fits',subim,subhd
endfor

END

PRO HZDYN_SUBREG_BX610_2015_MASK

im=readfits('bx610_spw27.fits',hd)

mk=im*0.0
mk[28:67,32:68,*]=1.0
writefits,'bx610_spw27_mask.fits',mk,hd

unc=im*0.0
unc=unc+robust_sigma(im)
writefits,'bx610_spw27_unc.fits',unc,hd

END