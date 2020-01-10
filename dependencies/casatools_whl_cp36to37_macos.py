#!/opt/local/bin/python


import glob,os,fileinput,sys
from pprint import pprint

print(sys.argv[0])
whlversion=sys.argv[1]
print(whlversion)

# modification 1: just modify the casacore lib *so name

flist=glob.glob('casatools-'+whlversion+'/casatools/__casac__/*-36m-*',recursive=True)

for filename in flist:
	newfilename=filename.replace('-36m-','-37m-')
	print(filename,'-->',newfilename)
	os.system('mv '+filename+' '+newfilename)
	
# modification 2: rename function keyword "async" to "isasync", not sure if this will break anything else

pyfile='casatools-'+whlversion+'/casatools/imager.py'
print('rename async in '+pyfile)
with fileinput.FileInput(pyfile, inplace=True, backup='.bak') as file:
    for line in file:
        print(line.replace(', async=', ', isasync=').replace(': async', ': isasync'), end='')
