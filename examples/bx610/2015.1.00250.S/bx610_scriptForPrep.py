"""
os.system("rm -rf uid___A002_Xb638bc_X2aa8_target.ms")
mstransform(outputvis='uid___A002_Xb638bc_X2aa8_target.ms',
            vis='uid___A002_Xb638bc_X2aa8.ms.split.cal', datacolumn='data',
            reindex=False, spw='', field='BX610',
            intent='OBSERVE_TARGET#ON_SOURCE')

os.system("rm -rf uid___A002_Xb64387_X1f95_target.ms")
mstransform(outputvis='uid___A002_Xb64387_X1f95_target.ms',
            vis='uid___A002_Xb64387_X1f95.ms.split.cal', datacolumn='data',
            reindex=False, spw='', field='BX610',
            intent='OBSERVE_TARGET#ON_SOURCE')
"""

#os.system('rm -rf uid___A001_X2fe_X20f_target.ms')
#concat(vis=['uid___A002_Xb638bc_X2aa8_target.ms','uid___A002_Xb64387_X1f95_target.ms'],concatvis='uid___A001_X2fe_X20f_target.ms')


spw_list=['0','1','2','3']
spwtag_list=['spw25','spw27','spw29','spw31']

for ind in range(4):

    os.system('rm -rf uid___A001_X2fe_X20f_target.'+spwtag_list[ind]+'.ms')
    os.system('rm -rf uid___A001_X2fe_X20f_target.'+spwtag_list[ind]+'.uvfits')
    mstransform(vis='uid___A001_X2fe_X20f_target.ms',outputvis='uid___A001_X2fe_X20f_target.'+spwtag_list[ind]+'.ms',timeaverage=True,timebin='30s',spw=spw_list[ind],datacolumn='data',chanaverage=True,chanbin=10,
            keepflags=True)
    initweights('uid___A001_X2fe_X20f_target.'+spwtag_list[ind]+'.ms',wtmode='weight',dowtsp=True)
    exportuvfits('uid___A001_X2fe_X20f_target.'+spwtag_list[ind]+'.ms','uid___A001_X2fe_X20f_target.'+spwtag_list[ind]+'.uvfits')
#

