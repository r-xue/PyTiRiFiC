from __future__ import print_function

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
from astropy.io.fits.diff import indent
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

def gmake_readinp(parfile,verbose=False):
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
            if    'comments' in tag or 'changelog' in tag:
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
    get ready for model constructions:
        add the default values
        fill optional keywords
        fill the "tied" values
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
    

def gmake_insertmodel(data,model,offset=[0,0,0],verbose=False):
    """
    insert a model into the data
        data/model is supposed to be transposed already,
        therefore follows the IDL indexing convention.
    offset is define from the left-bottom corner of data.
        so    model        -->    data
            [0,0,0]-pix    -->    offset-pix
    """
    d_nd=data.shape
    m_nd=model.shape

    
    mx_range=[0,m_nd[0]]
    my_range=[0,m_nd[1]]
    mz_range=[0,m_nd[2]]
    dx_range=[0+int(offset[0]),m_nd[0]+int(offset[0])]
    dy_range=[0+int(offset[1]),m_nd[1]+int(offset[1])]
    dz_range=[0+int(offset[2]),m_nd[2]+int(offset[2])]
    
    if  dx_range[0]<0:
        mx_range[0]+=-dx_range[0]
        dx_range[0]=0
    if  dx_range[1]>d_nd[0]:
        mx_range[1]+=-(dx_range[1]-d_nd[0])
        dx_range[1]+=-(dx_range[1]-d_nd[0])
    
    if  dy_range[0]<0:
        my_range[0]+=-dy_range[0]
        dy_range[0]=0
    if  dy_range[1]>d_nd[1]:
        my_range[1]+=-(dy_range[1]-d_nd[1])
        dy_range[1]+=-(dy_range[1]-d_nd[1])
    
    if  dz_range[0]<0:
        mz_range[0]+=-dz_range[0]
        dz_range[0]=0
    if  dz_range[1]>d_nd[2]:
        mz_range[1]+=-(dz_range[1]-d_nd[2])
        dz_range[1]+=-(dz_range[1]-d_nd[2])
    
    if  verbose==True:
        print("+"*20)
        print(offset)
        print(d_nd)
        print(dx_range[0],dx_range[1])
        print(dy_range[0],dy_range[1])
        print(dz_range[0],dz_range[1])
        print(m_nd)
        print(mx_range[0],mx_range[1])
        print(my_range[0],my_range[1])
        print(mz_range[0],mz_range[1])    
    
    if  data.ndim==3 and model.ndim==3:
        data[dx_range[0]:dx_range[1],
             dy_range[0]:dy_range[1],
             dz_range[0]:dz_range[1]]=model[mx_range[0]:mx_range[1],
                                            my_range[0]:my_range[1],
                                            mz_range[0]:mz_range[1]]
    if  data.ndim==4 and model.ndim==3:
        data[dx_range[0]:dx_range[1],
             dy_range[0]:dy_range[1],
             dz_range[0]:dz_range[1],0]=model[mx_range[0]:mx_range[1],
                                            my_range[0]:my_range[1],
                                            mz_range[0]:mz_range[1]]    
    
    return data


def make_slice(expr):
    """
    parsing the slicing syntax in STRING
    """
    if  len(expr.split(':'))>1:
        s=slice(*map(lambda x: int(x.strip()) if x.strip() else None, expr.split(':')))
    else:
        s=int(expr.strip())
    return s

def gmake_readpar(mod_dct,par_name):
    """
    read parameter values
        key:    par_str[ind_str]@obj_str
    """
    po_key=par_name.split("@")
    i_key=re.findall("\[(.*?)\]", po_key[0])
    if  len(i_key)==0:
        p_key=po_key[0]
        o_key=po_key[1]
        return mod_dct[o_key][p_key]
    else:
        p_key=(po_key[0].split("["))[0]
        o_key=po_key[1]
        i_key=i_key[0]
        return mod_dct[o_key][p_key][make_slice(i_key)]
    
def gmake_writepar(mod_dct,par_name,par_value):
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
        mod_dct[o_key][p_key]=par_value
    else:
        p_key=(po_key[0].split("["))[0]
        o_key=po_key[1]
        i_key=i_key[0]
        if  isinstance(mod_dct[o_key][p_key][make_slice(i_key)],list) and \
            not isinstance(par_value,list):
            par_value=[par_value]*len(mod_dct[o_key][p_key][make_slice(i_key)])
        mod_dct[o_key][p_key][make_slice(i_key)]=par_value
    
def gmake_pformat(fit_dct):
    """
    fill..
    p_format            : format for values
    p_format_keys       : format for p_name
    """
    p_format=[]
    p_format_keys=[]
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
        
        p_format+=[p_format0]
        p_format_keys+=[p_format0_keys]
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
        if  tag=='optimize':
            continue
        obj=inp_dct[tag]
        
        im_list=obj['image'].split(",")
        if  'mask' in obj:
            mk_list=obj['mask'].split(",")
        if  'error' in obj:
            em_list=obj['error'].split(",")
        if  'sample' in obj:
            sp_list=obj['sample'].split(",")            
        
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
    
def gmake_dct2fits(dct,outname='dct2fits',save_npy=False):
    """
        save a non-nested dictionary into a FITS binary table
        note:  not every Python object can be dumped into a FITS column, 
               e.g. a dictionary type can be aded into a column of a astropy/Table, but
               the Table can'be saved into FITS.
        example:
            gmake_dct2fits(dat_dct,save_npy=True)
    """
    print(outname)
    t=Table()
    
    for key in dct:
        #   the value is wrapped into a one-element list
        #   so the saved FITS table will "technically" have one row.
        t.add_column(Column(name=key,data=[dct[key]]))
    t.write(outname+'.fits',overwrite=True)    
    if  save_npy==True:
        np.save(outname+'.npy',dct)


if  __name__=="__main__":
    
    pass
    #objs=gmake_readinp('examples/bx610/bx610xy.inp',verbose=False)
    
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
    
    