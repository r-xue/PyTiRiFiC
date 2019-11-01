import gmake
import os,socket

if  'hypersion' or 'mini' in socket.gethostname() :
    os.chdir('/Users/Rui/Dropbox/Worklib/projects/GMaKE/examples/output/')
print(socket.gethostname())
print(os.getcwd())


inpfile=gmake.__demo__+'/../examples/inpfile/hxmm01_b6c3_uv_mc.inp'

inp_dct=gmake.read_inp(inpfile)
gmake.pprint(inp_dct,indent=4,width=100)

#print(getattr(inp_dct['compa']['xypos'],'ra'))
x=gmake.read_par(inp_dct,'xypos.ra@compa')
print(x)

x=gmake.read_par(inp_dct,'xypos.ra@compa',to_value=True)
print(x)