from recipes.almahelpers import fixsyscaltimes # SACM/JAO - Fixes
__rethrow_casa_exceptions = True
h_init()
try:
    hifa_importdata (dbservice=False, vis=['../rawdata/uid___A002_Xa48b1f_X3ca7', '../rawdata/uid___A002_Xa4ce71_X1356'], session=['session_1', 'session_2'])
    fixsyscaltimes(vis = 'uid___A002_Xa48b1f_X3ca7.ms')# SACM/JAO - Fixes
    fixsyscaltimes(vis = 'uid___A002_Xa4ce71_X1356.ms')# SACM/JAO - Fixes
    h_save() # SACM/JAO - Finish weblog after fixes
    h_init() # SACM/JAO - Restart weblog after fixes
    hif_restoredata (vis=['uid___A002_Xa48b1f_X3ca7', 'uid___A002_Xa4ce71_X1356'], session=['session_1', 'session_2'])
finally:
    h_save()
