
spw_list=['0','1','2','3']
spwtag_list=['spw25','spw27','spw29','spw31']

for ind in range(4):

    if  spw_list[ind]!='3':
        continue
    
    os.system('rm -rf uid___A001_X2fe_X20f_target.'+spwtag_list[ind]+'.ms')
    os.system('rm -rf uid___A001_X2fe_X20f_target.'+spwtag_list[ind]+'.uvfits')
    mstransform(vis='uid___A001_X2fe_X20f_target.ms',outputvis='uid___A001_X2fe_X20f_target.'+spwtag_list[ind]+'.ms',
                timeaverage=True,timebin='30s',spw=spw_list[ind],datacolumn='data',chanaverage=True,chanbin=1000,
                keepflags=False)
    initweights('uid___A001_X2fe_X20f_target.'+spwtag_list[ind]+'.ms',wtmode='weight',dowtsp=True)
    exportuvfits('uid___A001_X2fe_X20f_target.'+spwtag_list[ind]+'.ms','uid___A001_X2fe_X20f_target.'+spwtag_list[ind]+'.uvfits')
