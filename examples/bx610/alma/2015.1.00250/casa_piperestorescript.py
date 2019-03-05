from recipes.almahelpers import fixsyscaltimes # SACM/JAO - Fixes
__rethrow_casa_exceptions = True
h_init()
try:
    hifa_importdata (dbservice=False, vis=['../rawdata/uid___A002_Xb638bc_X2aa8', '../rawdata/uid___A002_Xb64387_X1f95'], session=['session_1', 'session_2'], ocorr_mode='ca')
    fixsyscaltimes(vis = 'uid___A002_Xb64387_X1f95.ms')# SACM/JAO - Fixes
    fixsyscaltimes(vis = 'uid___A002_Xb638bc_X2aa8.ms')# SACM/JAO - Fixes
    h_save() # SACM/JAO - Finish weblog after fixes
    h_init() # SACM/JAO - Restart weblog after fixes
    hif_restoredata (vis=['uid___A002_Xb638bc_X2aa8', 'uid___A002_Xb64387_X1f95'], session=['session_1', 'session_2'], ocorr_mode='ca')
finally:
    h_save()
