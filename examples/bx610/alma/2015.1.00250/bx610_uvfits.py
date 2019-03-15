
spw_list=['0','1','2','3']
spw_list=[]
spwtag_list=['spw25','spw27','spw29','spw31']

spw_list=['0','3','1','2']
out_list=['band6_bb1.ms','band6_bb4.ms','band6_bb2.ms','band6_bb3.ms']
ave_list=[True,True,False,False]

for ind in range(len(spw_list)):

    #if  spw_list[ind]!='3':
    #    continue
    
    #os.system('rm -rf uid___A001_X2fe_X20f_target.'+spwtag_list[ind]+'.ms')
    #os.system('rm -rf uid___A001_X2fe_X20f_target.'+spwtag_list[ind]+'.uvfits')
    os.system('rm -rf '+out_list[ind])
#    mstransform(vis='uid___A001_X2fe_X20f_target.ms',outputvis='uid___A001_X2fe_X20f_target.'+spwtag_list[ind]+'.ms',
#                timeaverage=True,timebin='30s',spw=spw_list[ind],datacolumn='data',chanaverage=True,chanbin=1000,
#                keepflags=False)
    mstransform(vis='uid___A001_X2fe_X20f_target.ms',outputvis=out_list[ind],
                timeaverage=False,timebin='30s',spw=spw_list[ind],datacolumn='data',chanaverage=ave_list[ind],chanbin=1000,
                keepflags=False)
    
    #initweights('uid___A001_X2fe_X20f_target.'+spwtag_list[ind]+'.ms',wtmode='weight',dowtsp=True)
    #exportuvfits('uid___A001_X2fe_X20f_target.'+spwtag_list[ind]+'.ms','uid___A001_X2fe_X20f_target.'+spwtag_list[ind]+'.uvfits')
