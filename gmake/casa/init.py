"""
We use this trick script to preload variables for the called CASA script.

try:
     casa --rcdir ../casa/ --logfile casa.log --log2term --nologger --nogui --nocrashreport -c "test_gmake_casa_init.py" "a=1" "b= 2"
     
"""
casalog.post('<<<<< init.py')

ind=(sys.argv).index('-c')
script_name=sys.argv[ind+1]

for ind in list(range(ind+2,len(sys.argv))):
    argv=sys.argv[ind]
    if  '=' in argv:
        #   likely a statement
        casalog.post(argv)
        exec(argv)
    else:
        #   likely a *.last like file 
        if  os.path.isfile(argv):
            par_file=open(argv, "r")
            lines = par_file.readlines()
            par_file.close()
            lines = [line.strip() for line in lines]
            for line in lines:
                casalog.post(line)
                exec(line)
    
casalog.post('>>>>> init.py')