PRO GMAKE_PLOTXY

data_list=[]
model_list=[]
residual_list=[]
cmodel_list=[]
version='itern'
version='iter0'

for i=0,3 do begin
    data_list=[data_list,'data_bx610.bb'+strtrim(i+1,2)+'.mfs.'+version+'.image.fits']
    model_list=[model_list,'model_bx610.bb'+strtrim(i+1,2)+'.mfs.'+version+'.image.fits']
    residual_list=[residual_list,'residual_bx610.bb'+strtrim(i+1,2)+'.mfs.'+version+'.image.fits']
    cmodel_list=[cmodel_list,'cmodel_bx610.bb'+strtrim(i+1,2)+'.mfs.'+version+'.image.fits']
endfor


set_plot,'ps'
device, file='gmake_plotxy.eps', /color, bits=8, /cmyk, /encapsulated,$
    xsize=8.0,ysize=8.0,/inches,xoffset=0.0,yoffset=0.0
!p.thick=2.0
!x.thick = 2.0
!y.thick = 2.0
!z.thick = 2.0
!p.charsize=1.5
!p.charthick=2.0
xyouts,'!6'


xgap=4 & ygap=4 & OXMargin=[5,5] &  OYMargin=[5,5] & nx=3 & ny=3

for i=0,3 do begin
    for j=0,3 do begin
        pos=cglayout([4,4,i+1+4*j],xgap=xgap,ygap=ygap,oxmargin=oxmargin,oymargin=oymargin)
        if  j eq 0 then im=readfits(data_list[i])
        if  j eq 1 then im=readfits(model_list[i])
        if  j eq 2 then im=readfits(residual_list[i])
        if  j eq 3 then im=readfits(cmodel_list[i])
        maxv=80e-5 & minv=-8e-5
        if  j eq 3 then begin
            maxv=maxv/10.0
            minv=minv/10.0
        endif
        cgloadct,13,/rev
        cgimage,im,stretch=1,pos=pos,/noe,maxv=maxv,minv=minv
        cgloadct,0
    endfor

    
endfor

loadct,0
device,/close
set_plot,'x'

END