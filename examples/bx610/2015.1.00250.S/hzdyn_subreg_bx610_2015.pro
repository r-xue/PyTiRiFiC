PRO HZDYN_SUBREG_BX610_2015

repo='/Volumes/D1/projects/hzdyn/2015.1.00250.S/science_goal.uid___A001_X2fe_X20d/group.uid___A001_X2fe_X20e/member.uid___A001_X2fe_X20f/imaging/'


;input=[ 'uid___A001_X2fe_X20f.BX610_sci.spw25.cube.I.pbcor.fits',$
;        'uid___A001_X2fe_X20f.BX610_sci.spw27.cube.I.pbcor.fits',$
;        'uid___A001_X2fe_X20f.BX610_sci.spw29.cube.I.pbcor.fits',$
;        'uid___A001_X2fe_X20f.BX610_sci.spw31.cube.I.pbcor.fits']
;output_tag=['spw25','spw27','spw29','spw31']
;
;for i=0,n_elements(input)-1 do begin
;    im=readfits(export_dir+input[i],hd)
;    hextractx,im,hd,subim,subhd,[-1.,1.]*2.0,[-1.,1.]*2.0,radec=[356.53929,12.822]
;    writefits,'bx610_'+output_tag[i]+'.fits',subim,subhd
;endfor

input=[ 'bx610.bb1_msc_ro1.mfs.itern.image.tt0.fits',$
        'bx610.bb2_msc_ro1.mfs.itern.image.tt0.fits',$
        'bx610.bb3_msc_ro1.mfs.itern.image.tt0.fits',$
        'bx610.bb4_msc_ro1.mfs.itern.image.tt0.fits']
for i=0,n_elements(input)-1 do begin
    im=readfits(repo+input[i],hd)
    hextractx,im,hd,subim,subhd,[-1.,1.]*2.0,[-1.,1.]*2.0,radec=[356.53929,12.822]
    shortname=repstr(input[i],'.tt0','')
    shortname=repstr(shortname,'_msc_ro1','')
    writefits,shortname,subim,subhd
endfor

input=[ 'bx610.bb1_msc_ro1.mfs.itern.psf.tt0.fits',$
    'bx610.bb2_msc_ro1.mfs.itern.psf.tt0.fits',$
    'bx610.bb3_msc_ro1.mfs.itern.psf.tt0.fits',$
    'bx610.bb4_msc_ro1.mfs.itern.psf.tt0.fits']
for i=0,n_elements(input)-1 do begin
    im=readfits(repo+input[i],hd)
    loc=where(im eq max(im,/nan))
    loc=loc[0]
    ind = ARRAY_INDICES(im, loc)
    hsize=49
    hextract,im,hd,subim,subhd,ind[0]-hsize,ind[0]+hsize,ind[1]-hsize,ind[1]+hsize
    shortname=repstr(input[i],'.tt0','')
    shortname=repstr(shortname,'_msc_ro1','')
    writefits,shortname,subim,subhd
endfor

END

PRO HZDYN_SUBREG_BX610_2015_MASK

prefix_list=[   'bx610.bb1.mfs.itern.image.fits',$
                'bx610.bb2.mfs.itern.image.fits',$
                'bx610.bb3.mfs.itern.image.fits',$
                'bx610.bb4.mfs.itern.image.fits']

for i=0,n_elements(prefix_list)-1 do begin
    im=readfits(prefix_list[i],hd)
    mk=im*0.0
    mk[(33-10):(60+10),(40-10):(64+10),*]=1.0
    writefits,repstr(prefix_list[i],'.image','.mask'),mk,hd
    unc=im*0.0
    unc=unc+robust_sigma(im)
    writefits,repstr(prefix_list[i],'.image','.unc'),unc,hd
endfor

END

PRO HZDYN_SUBREG_BX610_2015_HEXSAMPLE

;hexsample_bx610,'bx610_spw27',356.53929,12.822,xlimit=[33.-10.,60.+10.],ylimit=[40.-10.,64.+10.]

hexsample_bx610,'bx610.bb1.mfs.itern',356.53929,12.822,xlimit=[33.-10,60.+10],ylimit=[40.-10,64.+10]
hexsample_bx610,'bx610.bb2.mfs.itern',356.53929,12.822,xlimit=[33.-10,60.+10],ylimit=[40.-10,64.+10]
hexsample_bx610,'bx610.bb3.mfs.itern',356.53929,12.822,xlimit=[33.-10,60.+10],ylimit=[40.-10,64.+10]
hexsample_bx610,'bx610.bb4.mfs.itern',356.53929,12.822,xlimit=[33.-10,60.+10],ylimit=[40.-10,64.+10]

END


PRO HEXSAMPLE_BX610,prefix,cra,cdec,spacing=spacing,ratio=ratio,bpa=bpa,xlimit=xlimit,ylimit=ylimit

im=prefix+'.image.fits'
im=readfits(im,hd)

mk=readfits(prefix+'.mask.fits',mhd)



RADIOHEAD,hd,s=s
getrot,hd,rotang,cdelt
psize=abs(cdelt[0]*60.*60.)
sz=size(im,/d)
ctr=round(sz/2)
adxy,hd,cra,cdec,cx,cy



if  n_elements(spacing) eq 0 then spacing=s.bmaj/psize
if  n_elements(ratio) eq 0 then ratio=s.bmaj/s.bmin
if  n_elements(bpa) eq 0 then bpa=s.bpa
if  n_elements(xlimit) ne 2 then xlimit=[0,sz[0]-1]
if  n_elements(ylimit) ne 2 then ylimit=[0,sz[1]-1]

print,spacing,ratio,bpa

sample_grid,[cx,cy],spacing,/hex,$
    ratio=ratio,ang=bpa,$
    xout=xout,yout=yout,x_limit=xlimit,y_limit=ylimit
;tag=where(xout gt  and xout lt sz[0]-10 and yout gt 10 and yout lt sz[1]-10 )
;xout=xout[tag]
;yout=yout[tag]
xyad,hd,xout,yout,outra,outdec

if  n_elements(sz) eq 2 then nc=1 else nc=sz[2]

print,n_elements(xout)

hex_ind=MAKE_ARRAY(3,n_elements(xout)*nc)
for i=0,n_elements(xout)-1 do begin
    hex_ind[0,(i*nc+0):(i*nc+nc-1)]=xout[i]
    hex_ind[1,(i*nc+0):(i*nc+nc-1)]=yout[i]
    hex_ind[2,(i*nc+0):(i*nc+nc-1)]=findgen(nc)
endfor

hex={sp_ra:outra,sp_dec:outdec,sp_index:hex_ind}
mwrfits,hex,prefix+'.hex_tb.fits',/create


xout=round(xout)
yout=round(yout)
;print,xout
;print,yout
imhex=im*0.0
imhex0=im[*,*,0]*0.0
imhex0[xout,yout]=1.0
for i=0,nc-1 do begin
    imhex[*,*,i]=imhex0
endfor
print,'npix:',total(imhex)

writefits,prefix+'.hex_im.fits',imhex,hd

END