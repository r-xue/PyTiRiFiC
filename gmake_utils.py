

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
            print '>>>',tag
        else:
            if  tag=='comments' or tag=='changelog':
                pass
            else:
                key=line.split()[0]
                value=line.replace(key,'',1).strip()
                value=eval(value)
                print key,'---',value
                pars[key]=value
                objs[tag]=pars
        
    return objs
        
if  __name__=="__main__":
    
    objs=gmake_readpars('examples/bx610/bx610xy.inp',verbose=True)
    
    