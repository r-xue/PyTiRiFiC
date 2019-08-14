"""
We use this trick script to preload variables for the called CASA script.
For each shell argument:
    if it's determined as a existing file name, then the file will be executed, with all statments inside executed
    if the argument is likley an python statment (with "="), then it's considered as a literal string and executed.

try:
     casa --rcdir ../casa/ --logfile casa.log --log2term --nologger --nogui --nocrashreport -c "test_gmake_casa_init.py" "a=1" "b= 2"
     casa --rcdir ../casa/ --logfile casa.log --log2term --nologger --nogui --nocrashreport -c "test_gmake_casa_init.py" "a=1 ; b= 2"
test the parameter handover mechanism for running a CASA script

try:
     casa --rcdir ../casa/ --logfile casa.log --log2term --nologger --nogui --nocrashreport -c "test_gmake_casa_init.py" "a=1" "b= 2"
     casa --rcdir ../casa/ --logfile casa.log --log2term --nologger --nogui --nocrashreport -c "test_gmake_casa_init.py" "a=1 ; b= 2"
     casa --rcdir ../casa/ --logfile casa.log --log2term --nologger --nogui --nocrashreport -c "test_gmake_casa_init.py" "a=1 ; b= 2+a"     
     
"""
casalog.post('<<<<< init.py')

ind=(sys.argv).index('-c')
script_name=sys.argv[ind+1]

#   loop through each additional arguments
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
                #exec(line)
            execfile(argv)
    
casalog.post('>>>>> init.py')