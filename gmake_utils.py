
def moments(imagename,outname='test',
            maskname='',linechan=None):
        
    cube=SpectralCube.read(imagename,mode='readonly')
            
    if  linechan is not None:
        subcube=cube.spectral_slab(linechan[0],linechan[1])
    else:
        subcube=cube
    
    moment_0 = subcube.moment(order=0)  
    moment_1 = subcube.moment(order=1)  
    moment_2 = subcube.moment(order=2)  
    
    moment_0.write(outname+'_mom0.fits',overwrite=True)
    moment_1.write(outname+'_mom1.fits',overwrite=True)
    moment_2.write(outname+'_mom2.fits',overwrite=True)
        

def imcontsub(imagename,linefile='',contfile='',
              fitorder=0,   # not implemented yet
              verbose=False,
              linechan=None,contchan=None):
    """
    linechan / contchan: tuple with [fmin,fmax] in each element 
    """
    cube=SpectralCube.read(imagename,mode='readonly')
    spectral_axis = cube.spectral_axis
    if  linechan is not None:
        if  isinstance(linechan,tuple):
            linechan=[linechan]
        bad_chans=[(spectral_axis > linechan0[0]) & (spectral_axis < linechan0[1])  for linechan0 in linechan]
        bad_chans=np.logical_or.reduce(bad_chans)
        good_chans=~bad_chans
    if  contchan is not None:
        if  isinstance(contchan,tuple):
            contchan=[contchan]        
        good_chans=[(spectral_axis > contchan0[0]) & (spectral_axis < contchan0[1])  for contchan0 in contchan]
        good_chans=np.logical_or.reduce(good_chans)
        
    masked_cube = cube.with_mask(good_chans[:, np.newaxis, np.newaxis])
    cube_mean = masked_cube.mean(axis=0)  
    cube_imcontsub=cube-cube_mean

    cube_imcontsub.write(linefile,overwrite=True)
    cube_mean.write(contfile,overwrite=True)
    

def cr_tanh(r,r_in=0.0,r_out=1.0,theta_out=30.0):
    """
    """
    
    cdef=0.23
    A=2*cdef/(np.abs(theta_out)+cdef)-1.00001
    B=(2.-np.arctanh(A))*r_out/(r_out-r_in)

    tanh_fun=np.tanh(B*(r/r_out-1)+2.)+1.
    tanh_fun=0.5*tanh_fun

    return tanh_fun

def pdf2rv_nd(pdf,size=100000,
              sort=False,interp=True):
    """
    provide random sampling variables approxnimately following an arbitrary nd-dimension discrete PDF 
    without expensive MC
    
    An over-sampled PDF (with pdf_sort/pdf_interp=True) is preferred for accuracy.
    output:
        nx*ny PDF is in (ny,nx) shape (matching in the FITS convention)
        xpos=sample[0,:]
        ypos=sample[1,:]
        ...
        in 0-based pixel index units.
        xypos=[0,0] means the first pixel center.
    """

    pdf_shape=pdf.shape
    pdf_flat=pdf.ravel()
    
    if  sort==True:
        sortindex=np.argsort(pdf, axis=None)
        pdf_flat=pdf_flat[sortindex]
    cdf=np.cumsum(pdf_flat)
    
    choice = np.random.uniform(high=cdf[-1],size=size)
    index = np.searchsorted(cdf, choice)

    if  sort==True:
        index=sortindex[index]
    index = np.vstack(np.unravel_index(index,pdf_shape))

    if  interp==True:
        sample=np.flip(index,axis=0)-0.5+np.random.uniform(size=index.shape)
    else:
        sample=np.flip(index,axis=0)

    return sample


def cdf2rv(x,cdf,size=100000,seed=None):
    """
    generate a cheap random variable set following a target distribution described by the CDF
    using the inverse transform / pesudo-random number sampling method
    
    Assume that cdf has been sorted mono increasing
    
    the result will be in the range of cdf_x
    """

    y_cdf=cdf-cdf[0]
    y_cdf/=np.max(y_cdf)
    rng = np.random.RandomState(seed=seed)  
    pick =rng.random_sample(size)
    interpfunc=interpolate.interp1d(y_cdf,x,kind='linear')
    
    return interpfunc(pick)

def pdf2rv(x,pdf,size=100000,seed=None):
    """
    generate cheap random variable set following a target distribution described by the PDF
    using the inverse transform / pesudo-random number sampling method
    
    the resut will be in teh range of pdf_x
    """

    cdf=scipy.integrate.cumtrapz(pdf,x,initial=0.)
    
    return cdf2rv(x,cdf,size=size,seed=seed)

def sort_on_runtime(p):
    p = np.atleast_2d(p)
    idx = np.argsort(p[:, 0])[::-1]
    return p[idx], idx

def gmake_read_inp(parfile,verbose=False):
    """
    read parameters/setups from a .inp file into a dictionary nest:
        inp_dct[id][keywords]=values.
        inp_dct['comments']='??'
        inp_dct['changlog']='??'
        inp_dct['optimize']='??'
    """
    
    inp_dct={}
    with open(parfile,'r') as f:
        lines=f.readlines()
    lines= filter(None, (line.split('#')[0].strip() for line in lines))

    tag='default'
    for line in lines:
        if  line.startswith('@'):
            tag=line.replace('@','',1).strip()
            #pars={'content':''}
            pars={}
            #pars['content']+=line+"\n"
            if  verbose==True:
                print("+"*40)
                print('@',tag)
                print("-"*40)
        else:
            if    'comments' in tag or 'changelog' in tag or 'ignore' in tag:
                pass
                #pars['content']+=line+"\n"
                #inp_dct[tag]=pars
            elif  'optimize' in tag:
                #pars['content']+=line+"\n"
                key=line.split()[0]
                value=line.replace(key,'',1).split()
                if  len(value)==1:
                    pars[key]=eval(value[0])
                else:
                    pars[key]=[eval(value0) for value0 in value]
                #pars[key]=[eval(value[0]),eval(value[1]),eval(value[2])]
                inp_dct[tag]=pars
                if  verbose==True:
                    print(key," : ",value)
            else:
                #pars['content']+=line+"\n"
                key=line.split()[0]
                value=line.replace(key,'',1).strip()
                value=eval(value)
                pars[key]=value
                inp_dct[tag]=pars
                if  verbose==True:
                    print(key," : ",value)
    
    if  'optimize' in inp_dct.keys():
        if  'outdir' in (inp_dct['optimize']).keys():
            outdir=inp_dct['optimize']['outdir']
            if  not os.path.exists(outdir):
                os.makedirs(outdir)
            np.save(outdir+'/inp_dct.npy',inp_dct)
    
    return inp_dct

def gmake_listpars(objs,showcontent=True):
    """
    print out the parameter dict
    """
    for tag in objs.keys():
        print("+"*40)
        print('@',tag)
        print("-"*40)
        for key in objs[tag].keys():
            if  key=='content':
                print(objs[tag][key])
            else: 
                print(key," : ",objs[tag][key])
        

def gmake_inp2mod(objs):
    """
    get ready for model constructions, including:
        + add the default values
        + fill optional keywords
        + fill the "tied" values
    """

    for tag in objs.keys():
        for key in objs[tag].keys():
            if  'comments' in tag or 'changelog' in tag:
                pass
            elif 'optimize' in tag:
                pass
                #value=objs[tag][key]
                #for value0 in value:
                #    if  isinstance(value0,str):
                #        if  '@' in value:
                #            key_nest=value0.split("@")
                #            objs[tag][key]=objs[key_nest[1]][key_nest[0]]
            else:    
                value=objs[tag][key]
                if  isinstance(value, str):
                    if  '@' in value:
                        key_nest=value.split("@")
                        objs[tag][key]=objs[key_nest[1]][key_nest[0]]
    
    return objs
    



def paste_slice(tup):
    """
    make slice for the overlapping region
    """
    pos, w, max_w = tup
    wall_min = max(pos, 0)
    wall_max = min(pos+w, max_w)
    block_min = -min(pos, 0)
    block_max = max_w-max(pos+w, max_w)
    block_max = block_max if block_max != 0 else None
    
    return slice(wall_min, wall_max), slice(block_min, block_max)

def paste_array(wall, block, loc,method='replace'):
    """
    past a small array into a larger array with shifting
    works for high dimension or off-edge cases
    wall/block requires in the same dimension number 
    """
    loc_zip = zip(loc, block.shape, wall.shape)
    wall_slices, block_slices = zip(*map(paste_slice, loc_zip))
    if  method=='replace':
        wall[wall_slices] = block[block_slices].copy()
    if  method=='add':
        wall[wall_slices] += block[block_slices]

    return wall

def make_slice(expr):
    """
    parsing the slicing syntax in STRING
    """
    if  len(expr.split(':'))>1:
        s=slice(*map(lambda x: int(x.strip()) if x.strip() else None, expr.split(':')))
    else:
        s=int(expr.strip())
    return s

def gmake_readpar(inp_dct,par_name):
    """
    read parameter values
        key:    par_str[ind_str]@obj_str
    """
    po_key=par_name.split("@")
    i_key=re.findall("\[(.*?)\]", po_key[0])
    if  len(i_key)==0:
        p_key=po_key[0]
        o_key=po_key[1]
        return inp_dct[o_key][p_key]
    else:
        p_key=(po_key[0].split("["))[0]
        o_key=po_key[1]
        i_key=i_key[0]
        return inp_dct[o_key][p_key][make_slice(i_key)]
    
def gmake_writepar(inp_dct,par_name,par_value):
    """
    write parameter values
        key:    par_str[ind_str]@obj_str
        
    example:
        test=gmake_readpar(inp_dct,'xypos[0]@co76')
        print(test)
        test=gmake_readpar(inp_dct,'vrot@co76')
        print(test)
        test=gmake_readpar(inp_dct,'vrot[0:2]@co76')
        print(test)    
        gmake_writepar(inp_dct,'vrot[0:2]@co76',[2,5])
        test=gmake_readpar(inp_dct,'vrot@co76')
        print(test)
    """
    #print(par_name)
    po_key=par_name.split("@")
    i_key=re.findall("\[(.*?)\]", po_key[0])
    if  len(i_key)==0:
        p_key=po_key[0]
        o_key=po_key[1]
        inp_dct[o_key][p_key]=par_value
    else:
        p_key=(po_key[0].split("["))[0]
        o_key=po_key[1]
        i_key=i_key[0]
        if  isinstance(inp_dct[o_key][p_key][make_slice(i_key)],list) and \
            not isinstance(par_value,list):
            par_value=[par_value]*len(inp_dct[o_key][p_key][make_slice(i_key)])
        inp_dct[o_key][p_key][make_slice(i_key)]=par_value
    
def gmake_pformat(fit_dct,verbose=True):
    """
    fill..
    p_format            : format for values
    p_format_keys       : format for p_name
    """
    p_format=[]
    p_format_keys=[]
    
    if  verbose==True:
        print("+"*90)
        print("optimizing parameters:")
    
    for ind in range(len(fit_dct['p_name'])):
        
        p_key=fit_dct['p_name'][ind]
        p_start=fit_dct['p_start'][ind]
        p_lo=fit_dct['p_lo'][ind]
        p_up=fit_dct['p_up'][ind]
        
        smin=len(p_key)
        
        print("{0:<3} {1} {2} {3} {4}".format(ind,p_key,p_start,p_lo,p_up))

        p_format0='<'+str(max(smin,5))
        p_format0_keys='<'+str(max(smin,5))
        #   VELOCITY
        if  fnmatch.fnmatch(p_key,'v*'):
            p_format0='<'+str(max(smin,5))+'.0f'
            p_format0_keys='<'+str(max(smin,5))
        #   SURFACE BRIGHTNESS
        if  fnmatch.fnmatch(p_key,'sb*'):
            p_format0='<'+str(max(smin,5))+'.4f'
            p_format0_keys='<'+str(max(smin,5))
        if  fnmatch.fnmatch(p_key,'intflux*'):
            p_format0='<'+str(max(smin,5))+'.4f'
            p_format0_keys='<'+str(max(smin,5))            
        #   INC OR PA
        if  fnmatch.fnmatch(p_key,'inc*') or fnmatch.fnmatch(p_key,'pa*'):
            p_format0='<'+str(max(smin,3))+'.0f'
            p_format0_keys='<'+str(max(smin,3))         
        #   ERRR SCALING
        if  fnmatch.fnmatch(p_key,'lnf*'):
            p_format0='<'+str(max(smin,4))+'.4f'
            p_format0_keys='<'+str(max(smin,4))
        #   spectral index
        if  fnmatch.fnmatch(p_key,'alpha*'):
            p_format0='<'+str(max(smin,5))+'.2f'
            p_format0_keys='<'+str(max(smin,5))        
        
        p_format+=[p_format0]
        p_format_keys+=[p_format0_keys]
    
    if  verbose==True:
        print("+"*90)
    
    fit_dct['p_format']=deepcopy(p_format)
    fit_dct['p_format_keys']=deepcopy(p_format_keys)

def gmake_read_data(inp_dct,verbose=False,
                    fill_mask=False,fill_error=False):
    """
    read data into the dictionary
    """
    dat_dct={}
    
    if  verbose==True:
        print("+"*80)
    for tag in inp_dct.keys():
        if  'image' not in inp_dct[tag].keys():
            continue
        obj=inp_dct[tag]
        
        im_list=obj['image'].split(",")
        if  'mask' in obj:
            mk_list=obj['mask'].split(",")
        if  'error' in obj:
            em_list=obj['error'].split(",")
        if  'sample' in obj:
            sp_list=obj['sample'].split(",")
        if  'psf' in obj:
            pf_list=obj['psf'].split(",")                        
        
        for ind in range(len(im_list)):
            if  ('data@'+im_list[ind] not in dat_dct) and 'image' in obj:
                data,hd=fits.getdata(im_list[ind],header=True,memmap=False)
                dat_dct['data@'+im_list[ind]]=data
                dat_dct['header@'+im_list[ind]]=hd
                if  verbose==True:
                    print('loading: '+im_list[ind]+' to ')
                    print('data@'+im_list[ind],'header@'+im_list[ind])
            if  ('error@'+im_list[ind] not in dat_dct) and 'error' in obj:
                data=fits.getdata(em_list[ind],memmap=False)
                dat_dct['error@'+im_list[ind]]=data
                if  verbose==True:
                    print('loading: '+em_list[ind]+' to ')
                    print('error@'+im_list[ind])
            if  ('mask@'+im_list[ind] not in dat_dct) and 'mask' in obj:
                data=fits.getdata(mk_list[ind],memmap=False)                
                dat_dct['mask@'+im_list[ind]]=data
                if  verbose==True:
                    print('loading: '+mk_list[ind]+' to ')
                    print('mask@'+im_list[ind])
            if  ('sample@'+im_list[ind] not in dat_dct) and 'sample' in obj:
                data=fits.getdata(sp_list[ind],memmap=False)                
                # sp_index; 3xnp array (px index of sampling data points)
                dat_dct['sample@'+im_list[ind]]=np.squeeze(data['sp_index'])
                if  verbose==True:
                    print('loading: '+sp_list[ind]+' to ')
                    print('sample@'+im_list[ind])
            if  ('psf@'+im_list[ind] not in dat_dct) and 'psf' in obj:
                data=fits.getdata(pf_list[ind],memmap=False)                
                dat_dct['psf@'+im_list[ind]]=data
                if  verbose==True:
                    print('loading: '+pf_list[ind]+' to ')
                    print('psf@'+im_list[ind])                    
                        
    if  fill_mask==True or fill_error==True:

        for tag in dat_dct.keys():
            if  'data@' in tag:
                if  (tag.replace('data@','mask@') not in dat_dct) and fill_mask==True:
                    data=dat_dct[tag]
                    dat_dct[tag.replace('data@','mask@')]=data*0.0+1.
                    if  verbose==True:
                        print('fill '+tag.replace('data@','mask@'),1.0)
                if  (tag.replace('data@','error@') not in dat_dct) and fill_error==True:
                    data=dat_dct[tag]
                    dat_dct[tag.replace('data@','error@')]=data*0.0+np.std(data)
                    if  verbose==True:
                        print('fill '+tag.replace('data@','error@'),np.std(data))                
    
    if  verbose==True:
        print("-"*80)    
    
    return dat_dct
    
def gmake_dct2fits(dct,outname='dct2fits',save_npy=False,verbose=False):
    """
        save a non-nested dictionary into a FITS binary table
        note:  not every Python object can be dumped into a FITS column, 
               e.g. a dictionary type can be aded into a column of a astropy/Table, but
               the Table can'be saved into FITS.
        example:
            gmake_dct2fits(dat_dct,save_npy=True)
    """
    
    if  verbose==True:
        print('dct2fits->outname',outname)
        
    t=Table()
    
    for key in dct:
        #   the value is wrapped into a one-element list
        #   so the saved FITS table will "technically" have one row.
        t.add_column(Column(name=key,data=[dct[key]]))
    t.write(outname+'.fits',overwrite=True)    
    if  save_npy==True:
        np.save(outname+'.npy',dct)


def gmake_fit_setup(inp_dct,dat_dct):
    
    sampler={'inp_dct':inp_dct,'dat_dct':dat_dct}

    if  'amoeba' in inp_dct['optimize']['method']:
        fit_dct=gmake_amoeba_setup(inp_dct,dat_dct)
    if  'emcee' in inp_dct['optimize']['method']:
        fit_dct,sampler=gmake_emcee_setup(inp_dct,dat_dct)
    if  'lmfit' in inp_dct['optimize']['method']:
        fit_dct=gmake_lmfit_setup(inp_dct,dat_dct)            

    #   for method='emcee': sampler is an emcee object
    #   for method=others: sampler is a dict

    return fit_dct,sampler


    
    #if  'lmfit' in inp_dct['optimize']['method']:
    #    gmake_lmfit_analyze(fit_dct,sampler['inp_dct'],sampler['inp_dct'],sampler['dat_dct'],nstep=nstep)

if  __name__=="__main__":
    
    pass

    #objs=gmake_read_inp('examples/bx610/bx610xy.inp',verbose=False)
    
    #print("\n"*2)
    #print(objs.keys())
    #gmake_listpars(objs)
    #objs=gmake_fillpars(objs)
    #print("\n"*10)
    #gmake_listpars(objs)
    
    #data=np.zeros((100,100,200))
    #model=np.ones((10,10,90))
    #offset=[20,20,100]
    #data=gmake_insertmodel(data,model,offset=offset)
    #fits.writeto('test.fits',data.T,overwrite=True)
    
    