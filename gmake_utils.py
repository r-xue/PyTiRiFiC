from __future__ import print_function

def gmake_readpars(parfile,verbose=False):
    """
    read parameters/setups from a .inp file into a dictionary nest
    """
    objs={}
    
    with open(parfile,'r') as f:
        lines=f.readlines()
    lines= filter(None, (line.split('#')[0].strip() for line in lines))

    tag='default'
    pars={}
    for line in lines:
        if  line.startswith('@'):
            tag=line.replace('@','',1).strip()
            pars={}
            if  verbose==True:
                print("+"*40)
                print('@',tag)
                print("-"*40)
        else:
            if  tag=='comments' or tag=='changelog':
                pass
            else:
                key=line.split()[0]
                value=line.replace(key,'',1).strip()
                value=eval(value)
                if  verbose==True:
                    print(key," : ",value)
                pars[key]=value
                objs[tag]=pars
        
    return objs

def gmake_listpars(objs):
    
    for tag in objs.keys():
        print("+"*40)
        print('@',tag)
        print("-"*40)
        for key in objs[tag].keys():
            print(key," : ",objs[tag][key])
        

def gmake_fillpars(objs):
    """
    get ready for model constructions (add the default/tied values)
    """
    for tag in objs.keys():
        for key in objs[tag].keys():
            value=objs[tag][key]
            if  isinstance(value, str):
                if  '@' in value:
                    key_nest=value.split("@")
                    objs[tag][key]=objs[key_nest[1]][key_nest[0]]
    
    return objs
    
        
if  __name__=="__main__":
    
    objs=gmake_readpars('examples/bx610/bx610xy.inp',verbose=False)
    gmake_listpars(objs)
    objs=gmake_fillpars(objs)
    gmake_listpars(objs)
    
    