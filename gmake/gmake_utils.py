from .gmake_init import *
#import inspect


from copy import deepcopy


from .metadata import gmake_cfg

logger = logging.getLogger(__name__)
# get a logger named after a function name
# logger=logging.getLogger(inspect.stack()[0][3])

"""
import ast, operator

binOps = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod
}

def arithmeticEval (s):
    node = ast.parse(s, mode='eval')

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        elif isinstance(node, ast.Str):
            return node.s
        elif isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.BinOp):
            return binOps[type(node.op)](_eval(node.left), _eval(node.right))
        else:
            raise Exception('Unsupported type {}'.format(node))

    return _eval(node.body)
"""


import sys
import gc

def read_inp(parfile,log=False):
    """
    read parameters/setups from a .inp file into a dictionary nest:
        inp_dct[id][keywords]=values.
        inp_dct['comments']='??'
        inp_dct['changlog']='??'
        inp_dct['optimize']='??'
        
    keyword value formatting
        1.remove trailing/prefix space / comments
        2.split my space
        3.first element is the key
        4.the rest elements will be filled into value
            more than one element : list
            one element: scaler
    """

    inp_dct={}
    with open(parfile,'r') as f:
        lines=f.readlines()
    lines= filter(None, (line.split('#')[0].strip() for line in lines))

    tag='default'
    cfg=gmake_cfg
    
    for line in lines:
        if  line.startswith('@'):
            tag=line.replace('@','',1).strip()
            #pars={'content':''}
            pars={}
            #pars['content']+=line+"\n"
            if  log==True:
                logger.debug("+"*40)
                logger.debug('@ {}'.format(tag))
                logger.debug("-"*40)
        else:
            
            if  any(section in tag.lower() for section in cfg['inp.comment']['id'].split(',')):
                pass
                #pars['content']+=line+"\n"
                #inp_dct[tag]=pars
            else:
                #pars['content']+=line+"\n"               
                #   identify the "key"
                key=line.split()[0]
                #   remove leading/trailing space to get the "value" portion
                value=line.replace(key,'',1).strip()
                if  log==True:
                    logger.debug('{:20}'.format(key)+" : "+str(value))
                
                """                    
                try:                #   likely mutiple-elements are provided, 
                                    #   but be careful of eval() usage here
                                    #   e.g.:"tuple (1)" will be a valid statement
                    #pars[key]=eval(value)
                    #pars[key]=ast.literal_eval(value)
                    pars[key]=aeval(value)
                except SyntaxError: #   pack the value content into a list
                    values=value.split()
                    #pars[key]=[eval(value0) for value0 in value]
                    #pars[key]=[ast.literal_eval(value0) for value0 in value]
                    pars[key]=[aeval(value0) for value0 in values]
                """
                pars[key]=aeval(value)
                if  len(aeval.error)>0 and pars[key] is None:
                    values=value.split()
                    pars[key]=[aeval(value0) for value0 in values]
                
                inp_dct[tag]=pars

    
    if  'general' in inp_dct.keys():
        if  'outdir' in (inp_dct['general']).keys():
            outdir=inp_dct['general']['outdir']
            if  isinstance(outdir,str):
                if  not os.path.exists(outdir):
                    os.makedirs(outdir)
                #np.save(outdir+'/inp_dct.npy',inp_dct)
                #write_inp(inp_dct,inpfile=outdir+'/p_start.inp',
                #          overwrite=True)
                                
                
    return inp_dct


def write_inp(inp_dct,
              inpfile='example.inp',writepar=None,
              overwrite=False):
    """
    write out inp files from inp_dct
    if overwrite=False, the function will try to append .0/.1/.2... to the .inp file name
    writepar is two-element tuple, first element is the key name to be modified
                                   second element is the value
                                   
    note: py>=3.7 use the ordered dict by default (so the output keyword order is preserved) 
    """
    
    logger.info('save the model input parameter: '+inpfile)    
    
    inp_dct0=deepcopy(inp_dct)
    if  writepar is not None:
        for ind in range(len(writepar[0])):
            write_par(inp_dct0,writepar[0][ind],writepar[1][ind])
    
    outname=inpfile
    
    ind=0
    if  overwrite==False:
        while os.path.isfile(outname):
            outname=inpfile+'.'+str(ind) 
            ind+=1
            
    f=open(outname,'w')
    output=''
    for obj in inp_dct0.keys():
        output+='#'*80+'\n'
        output+='@'+obj+'\n'
        output+='#'*80+'\n\n'
        for key in inp_dct0[obj].keys():
            output+='{:20} {}\n'.format(key,repr(inp_dct0[obj][key]))
        output+='\n'
    f.write(output)
    f.close()


def read_range(center=0,delta=0,mode='a'):
    """
        modifiy the parameter exploring bounrdary according to the info from opt section
        a:    absolute
        
        
    """
    if  mode=='a':
        return delta
    if  mode=='o':
        return center+delta
    if  mode=='r':
        return center*delta



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

def gal_flat(im,ang,inc,cen=None,interp=True,
             align_major=False,
             fill_value=None):
    """
    translated from IDL/gal_flat.pro
    im in (nz,ny,nx)
    cen is (xc,yc)
    """
    angr = np.deg2rad(ang+90.)
    tanang = np.tan(angr)
    cosang = np.cos(angr)
    cosinc = np.cos(np.deg2rad(inc))
    
    dims=im.shape

    if  cen is None:
        xcen = dims[-1]/2.0      
        ycen = dims[-2]/2.0
    else:
        xcen = cen[0]
        ycen = cen[1]

    b=ycen-xcen*tanang
    
    gridx = xcen + np.array([ [-1,1], [-1,1] ]) * dims[-1]/6.0
    gridy = ycen + np.array([ [-1,-1], [1,1] ]) * dims[-2]/6.0      

    yprime = gridx*tanang + b            
    r0 = (gridy-yprime)*np.cos(angr)     
    delr = r0*(1.0-cosinc)               
    dely = -delr*np.cos(angr)               
    delx =  delr*np.sin(angr)
    distx = gridx + delx
    disty = gridy + dely

    x0 = dims[1]/3.0
    y0 = dims[0]/3.0
    dx = x0                            
    dy = y0

    t=transform.PolynomialTransform()
    source=np.array((gridx.flatten(),gridy.flatten()))
    destination=np.array((distx.flatten(),disty.flatten()))
    t.estimate(source.T,destination.T,1)
    
    if  fill_value is None:
        cval=float('nan')
    else:
        cval=fill_value
    im_wraped=transform.warp(im, t, order=1, mode='constant',cval=cval)
    
    
    if  align_major==True:
        #print('-->',90+ang)
        # (0,0)  sckit-image is the left-top corner, so the presentation is actually flipped along the x-axis 
        # counter-clockwise in sckit-image is eqaveulent with clockwise in FITS  
        im_wraped=transform.rotate(im_wraped,90+ang-180,center=(xcen,ycen),
                                   resize=False,
                                   order=1,cval=cval)

    return im_wraped    

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
              sort=False,interp=True,seed=None):
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


def gmake_listpars(objs,showcontent=True):
    """
    print out the parameter dict
    """
    for tag in objs.keys():
        logger.info("+"*40)
        logger.info('@'+tag)
        logger.info("-"*40)
        for key in objs[tag].keys():
            if  key=='content':
                print(objs[tag][key])
            else: 
                print(key," : ",objs[tag][key])
        

def inp2mod(inp_dct):
    """
    Convert Input Parameter Dictionary to Model Properties Dictionary
    
    The code will make a dictionary ready for model constructions, including:
        + add the default values
        + fill optional keywords
        + fill the "tied" values
        
    inp_dct
    
    --> write_par (changed some modeling parameter values, e.g. shifting during the optimization iteration) 
    
    inp_dct_modified
    
    --> inp2mod (fullfill the default value / ties / reject comments <-- act as a formatter) 
    
    mod_dct
    
    """
    
    objs=deepcopy(inp_dct)
    
    cfg=gmake_cfg
    ids_ignore=cfg['inp.comment']['id'].split(',')+cfg['inp.optimizer']['id'].split(',')

    #   assemble all parameters
    
    par_list=[]
    for sec_name in objs.keys():
        for key_name in objs[sec_name].keys():
            par_list+=[key_name+'@'+sec_name]
    
    secs_imported=[]
    
    for tag in list(objs.keys()):
        
        #   remove sections not related to model component properties
                         
        if  any(section in tag.lower() for section in ids_ignore):            
            tmp=objs.pop(tag,None)
            continue

        for key in list(objs[tag].keys()):

            #value=objs[tag][key]
            #for value0 in value:
            #    if  isinstance(value0,str):
            #        if  '@' in value:
            #            key_nest=value0.split("@")
            #            objs[tag][key]=objs[key_nest[1]][key_nest[0]]
 
            value=objs[tag][key]
            if  isinstance(value, str):
                
                pars=[par for par in par_list if par in value] 
                if  pars!=[]:   # a string expression for parameter tie is detected
                    par=max(pars, key=len) 
                    key_nest=par.split("@")
                    tmp0=objs[key_nest[1]][key_nest[0]]
                    if  isinstance(tmp0, str):  # copy string
                        objs[tag][key]=tmp0
                        #print(tmp0,'-->',objs[tag][key])
                    else:                       # math expression evluation
                        value_expr=value.replace(par,"tmp0")
                        aeval.symtable["tmp0"]=objs[key_nest[1]][key_nest[0]]
                        #print(value_expr,value)
                        #objs[tag][key]=ne.evaluate(value_expr).tolist()
                        objs[tag][key]=aeval(value_expr)
                        #print(value,'-->',objs[tag][key])
                
                if  value in list(objs.keys()) and key.lower() == 'import':
                    #   value: the section to be imported
                    secs_imported+=[value]
                    
                    del objs[tag][key]
                    for import_key in list(objs[value].keys()):
                        objs[tag][import_key]=objs[value][import_key]
                    
                    #logger.debug('{:16}'.format(key+'@'+tag)+' : '+'{:16}'.format(value)+'-->'+str(objs[tag][key]))
                """
                if  '@' in value:
                    key_nest=value.split("@")
                    objs[tag][key]=objs[key_nest[1]][key_nest[0]]
                """
    
    for par_group in list(set(secs_imported)):
        del objs[par_group]
    
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

def read_par(inp_dct,par_name):
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
    
def write_par(inp_dct,par_name,par_value,verbose=False):
    """
    write parameter values
        key:    par_str[ind_str]@obj_str
        
    example:
        test=read_par(inp_dct,'xypos[0]@co76')
        print(test)
        test=read_par(inp_dct,'vrot@co76')
        print(test)
        test=read_par(inp_dct,'vrot[0:2]@co76')
        print(test)    
        write_par(inp_dct,'vrot[0:2]@co76',[2,5])
        test=read_par(inp_dct,'vrot@co76')
        print(test)
    """
    #print(par_name)
    
    if  verbose==True:
        print('before: {} : {}'.format(par_name,read_par(inp_dct,par_name)))    
    
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
        
    if  verbose==True:
        print('after: {} : {}'.format(par_name,read_par(inp_dct,par_name)))        
    
def gmake_pformat(fit_dct):
    """
    fill..
    p_format            : format for values
    p_format_keys       : format for p_name
    """
    p_format=[]
    p_format_keys=[]
    p_format_prec=[]
    
    
    logger.debug("+"*90)
    #print("outdir:               ",fit_dct['optimize']['outdir'])
    logger.debug("optimizer: "+fit_dct['method'])
    logger.debug("optimizing parameters: index / name / start / lo_limit / up_limit / scale")
    
    metadata_path=os.path.dirname(os.path.abspath(__file__))+'/metadata/'
    template_inp=read_inp(metadata_path+'parameter_definition.inp',log=False)
    def_dct=template_inp
    def_dct_obj=def_dct['emission_component']
    def_dct_opt=def_dct['optimize']
    
    
    maxlen=len(max(fit_dct['p_name'],key=len))
    for ind in range(len(fit_dct['p_name'])):
        
        p_key=fit_dct['p_name'][ind]
        p_start=fit_dct['p_start'][ind]
        p_lo=fit_dct['p_lo'][ind]
        p_up=fit_dct['p_up'][ind]
        p_up=fit_dct['p_up'][ind]
        p_scale=fit_dct['p_scale'][ind]
        
        smin=len(p_key)        
        for keyword in def_dct_obj.keys():
            if  keyword+'@' in p_key or keyword+'[' in p_key:
                #print(keyword,def_dct_obj[keyword])
                p_format0_prec=def_dct_obj[keyword][1]
                p_format0_keys=''+str(max(smin,5))
                
        #  same widths for all parameters in one trial
        textout=' {:{align}{width}} '.format(ind,align='<',width=2)
        textout+=' {:{align}{width}} '.format(p_key,align='<',width=maxlen)
        textout+=' {:{align}{width}{prec}} '.format(p_start,align='^',width=13,prec=p_format0_prec)
        textout+=' ( {:{align}{width}{prec}}, '.format(p_lo,align='^',width=13,prec=p_format0_prec)
        textout+=' {:{align}{width}{prec}} )'.format(p_up,align='^',width=13,prec=p_format0_prec)
        textout+=' {:{align}{width}{prec}} '.format(p_scale,align='^',width=13,prec=p_format0_prec)
        logger.debug(textout)


        #   used for emcee table output
        p_format0='<'+str(max(smin,5))+p_format0_prec
        p_format0_keys='<'+str(max(smin,5))      
        p_format+=[p_format0]
        p_format_keys+=[p_format0_keys]
        p_format_prec+=[p_format0_prec]
        
    logger.debug("+"*90)
    
    fit_dct['p_format']=deepcopy(p_format)
    fit_dct['p_format_keys']=deepcopy(p_format_keys)
    fit_dct['p_format_prec']=deepcopy(p_format_prec)


def convert_size(size_bytes): 
    """
    **obsolete** now we use human_unit()/human_to_string()
    """
    if size_bytes == 0: 
        return "0B" 
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB") 
    i = int(np.floor(np.log(size_bytes)/np.log(1024)))
    power = np.power(1024, i) 
    size = round(size_bytes / power, 2) 
    return "{} {}".format(size, size_name[i])


def human_unit(quantity, return_unit=False, base_index=0, scale_range=None):

    """
    Sugguest a better unit for the quantity and make it more human readable
    e.g. 1200 m/s -> 1.2 km/s
        
    return_unit:
        False:          return the input quantity in a suggested unit
        True:           just return a suggested unit

    base_index:
        the index of the unitbase which we examine its prefix possibility.
            
    For time:           try built-in astropy.utils.console.human_time()
    For file size:      one may also use astropy.utils.concolse.human_file_size()

    reference:    https://docs.astropy.org/en/stable/_modules/astropy/units/core.html
    
    have tried the functions below,they work similar for PrefixUnit, but they dont work well 
    with composited units (e.g. u.km/u.s)
        get_current_unit_registry().get_units_with_physical_type(unit)
        unit.find_equivalent_units(include_prefix_units=True)
        unit.compose(include_prefix_units=True) might work but the results can be unexpected
    note:
        get_units_with_same_physical_type() is a private method, since end users should be encouraged
        to use the more powerful `compose` and `find_equivalent_units`
        methods (which use this under the hood).
        
    help find the best human readable unit
    then you can do q.to_string(unit='*')        
    
    """

    
    if  not quantity.isscalar:
        raise Exception("given quantity is not scalar")
   
    

    human_unit=quantity.unit

    bases=human_unit.bases.copy()
    powers=human_unit.powers.copy()
    base=bases[base_index]
    candidate_list=(base).compose(include_prefix_units=True,max_depth=1)

    if  not base.is_equivalent(u.byte):
        base_factor=1e3     # SI
    else:
        base_factor=2**10   # Binary

    for candidate in candidate_list:
    
        if  scale_range is not None:
            if  candidate.scale < min(scale_range) or candidate.scale > max(scale_range):
                continue
        
        if  1 <= abs(quantity.value)*candidate.scale < base_factor and \
            (np.log(candidate.scale)/np.log(base_factor)).is_integer():
            
            human_base=(candidate.bases)[0]
            bases[base_index]=human_base
            human_unit=u.Unit(1)
            for b, p in zip(bases, powers): 
                human_unit *= b if p == 1 else b**p # make sure back to PrefixUnit when possible
            break

    if  return_unit==False:
        return quantity.to(human_unit)
    else:
        return human_unit
        
        
def human_to_string(quantity,
                     nospace=True,shortname=True,
                     format='generic',format_string='{0:0.2f} {1}'):
                
    """
    format: forwarded to .to_string(format):
        options: generic, unscaled, cds, console, fits, latex, latex_inline, ogip, unicode, vounit
    
    format_string: {0:0.2f} {1}
        help format you output when output='string'
        
    output: 
        'string':       a string represent the input quantity in best-guess unit

            
    For time:           try built-in astropy.utils.console.human_time()
    For file size:      one may also use astropy.utils.concolse.human_file_size()

    
    """
    format_all=['generic', 'unscaled', 'cds', 'console', 'latex', 'latex_inline', 'ogip', 'unicode', 'vounit']

    unit_string=quantity.unit.to_string(format=format)
    if  shortname==True and format=='generic':
        unit_names=[]
        try:
            unit_names+=quantity.unit.names
        except AttributeError as error:
            unit_names+=[quantity.unit.to_string(format=f) for f in format_all]
        unit_string=min(unit_names,key=len)
    if  nospace==True and format=='generic':
        unit_string=unit_string.replace(' ','')
    quantity_str=format_string.format(quantity.value,unit_string)

    return quantity_str


    
    #if  'lmfit' in inp_dct['optimize']['method']:
    #    gmake_lmfit_analyze(fit_dct,sampler['inp_dct'],sampler['inp_dct'],sampler['dat_dct'],nstep=nstep)

def get_dirsize(dir):
    """
    get the size of a file or directory
    """
    dirsize=sum([os.path.getsize(fp) for fp in (os.path.join(dirpath, f) for dirpath, dirnames, filenames in os.walk(dir) for f in filenames) if not os.path.islink(fp)])
    
    return dirsize
    
def check_deps(package_name='gmake'):
    
    package = pkg_resources.working_set.by_key[package_name]
    deps = package.requires()
    for r in deps:
        name=str(r.name)
        version_required=str(r.specifier)
        if  version_required=='':
            version_required='unspecified'
        version_installed=pkg_resources.working_set.by_key[name].version
        logger.debug('{0:<18} {1:<12} {2:<12}'.format(name,version_required,version_installed))

    return

def get_obj_size(obj):
    marked = {id(obj)}
    obj_q = [obj]
    sz = 0

    while obj_q:
        sz += sum(map(sys.getsizeof, obj_q))

        # Lookup all the object referred to by the object in obj_q.
        # See: https://docs.python.org/3.7/library/gc.html#gc.get_referents
        all_refr = ((id(o), o) for o in gc.get_referents(*obj_q))

        # Filter object that are already marked.
        # Using dict notation will prevent repeated objects.
        new_refr = {o_id: o for o_id, o in all_refr if o_id not in marked and not isinstance(o, type)}

        # The new obj_q will be the ones that were not marked,
        # and we will update marked with their ids so we will
        # not traverse them again.
        obj_q = new_refr.values()
        marked.update(new_refr.keys())

    return sz

def check_setup():
    
    logger.debug("Python version:   {}".format(sys.version))
    logger.debug("Host Name:        {}".format(socket.gethostname()))
    logger.debug("Num of Core:      {}".format(multiprocessing.cpu_count()))
    mem=virtual_memory()
    logger.debug("Total Memory:     {}".format(convert_size(mem.total)))
    logger.debug("Available Memory: {}".format(convert_size(mem.available)))
    logger.debug("#"*80)
    check_deps()    

def h5ls_print(name,obj):
    print(name, dict(obj.attrs))

def h5ls(filename,logfile=None):
    
    if  logfile is None:
        with h5py.File(filename,'r') as hf:
            hf.visititems(h5ls_print)
    else:
        with open(logfile, 'w') as f:
            with redirect_stdout(f):
                with h5py.File(filename,'r') as hf:
                    hf.visititems(h5ls_print)
    

    #objs=gmake_read_inp('examples/bx610/bx610xy.inp',=False)
    
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
    
    