inp_dct=gmake.read_inp(inpfile)
#gmake.pprint(gmake.inp2mod(inp_dct))
gmake.pprint(inp_dct)
gmake.write_inp(inp_dct,inpfile='/Users/Rui/Downloads/test.inp',overwrite=True)

inp_dct_2=gmake.read_inp('/Users/Rui/Downloads/test.inp')