gmake_cli ../inpfile/bx610_uvb6_ab.inp --debug --logfile bx610_uvb6_ab.log              #   a complete workflow

gmake_cli ../inpfile/bx610_band6_uv_ab.inp --debug --fit        #   model fitting
gmake_cli ../inpfile/bx610_band6_uv_ab.inp --debug --analyze    #   analyze / model exporting/imaging
gmake_cli ../inpfile/bx610_band6_uv_ab.inp --debug --plot       #   diagnostic plots

gmake_cli ../inpfile/bx610_b6c3_uv_mc.inp --debug --fit        #   model fitting
gmake_cli ../inpfile/bx610_b6c3_uv_mc.inp --debug --analyze    #   analyze / model exporting/imaging
gmake_cli ../inpfile/bx610_b6c3_uv_mc.inp --debug --plot       #   diagnostic plots
