print("\n scale_range off\n")

qlist=[ 1234567*u.m,
        1.2*1e-6*u.m,
        (0.2)*u.km/u.s,
        1024*u.Mibyte,
        1.23e4*u.km,
        1e-4*u.km,
        1024*u.byte,
        (1024**2)*u.byte,
        (1024**2)*u.byte/u.s,
        (1024**2-1)*u.byte/u.s,
        1300*u.MHz]
for q in qlist:
    print("")
    for opt in [True,False]:
        q_new=human_unit(q,return_unit=opt)
        print('{0:25s} {1:20s}'.format('return_unit='+str(opt),q_new),type(q_new))       
        if  opt==False:
            text1=human_to_string(q_new)
            text2=human_to_string(q_new,format_string='{0:0.3f}   {1}')
            print(text1)
            print(text2)

#   if you don't like the code goes to "u.Mm" from "u.m", set a scale range

print("\n scale_range on\n")

qlist=[ 1234567*u.m]
for q in qlist:
    print("")
    for opt in [True,False]:
        q_new=human_unit(q,return_unit=opt,scale_range=[1e-3,1e3])
        print('{0:25s} {1:20s}'.format('return_unit='+str(opt),q_new),type(q_new))         
        if  opt==False:
            text1=human_to_string(q_new)
            text2=human_to_string(q_new,format_string='{0:0.3f}   {1}')
            print(text1)
            print(text2)