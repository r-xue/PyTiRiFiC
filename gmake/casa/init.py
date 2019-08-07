casalog.post('<<<<< init.py')

ind=(sys.argv).index('-c')
script_name=sys.argv[ind+1]

if  (len(sys.argv)-1)>=(ind+2):
    script_para=sys.argv[ind+2]
    par_file=open(script_para, "r")
    lines = par_file.readlines()
    par_file.close()
    lines = [line.strip() for line in lines]
    for line in lines:
        casalog.post(line)
        exec(line)
    
casalog.post('>>>>> init.py')