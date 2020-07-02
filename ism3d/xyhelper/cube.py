def hextract(data, header, ss):
    """
    similar to hextract.pro or hextract3d.pro in idl_moments
    However, it can also process stokes spectral cube
    prange can be something like:
        a list of two element tuple: 
            [(0,2),(218,220),(218,250),(222,230)]
        or a list of slice
            np.s_[1:5,1::5]=(slice(1, 5, None), slice(1, None, 5))
        or a list of slice expression string (from make_slice)

    e.g. subim,subhd=hextract(im,hd,np.s_[:,:,(256-3):(256+3),(256-3):(256+3)]) 

    two operations are performed:
        slice the original data array
        update the header crpix value
    """

    ss_list = []
    for s in ss:
        if isinstance(s, tuple):
            ss_list.append(slice(*s))
        if isinstance(s, str):
            ss_list.append(make_slice(s))
        if isinstance(s, slice):
            ss_list.append(s)

    newdata = data[tuple(ss_list)]
    newheader = header.copy()

    # first slice is for the last axis in FITS
    axisno = 1
    ds = newdata.shape
    for i in range(len(ss_list))[::-1]:
        newheader['NAXIS'+str(axisno)] = ds[i]
        newstart = ss_list[i].start
        if ss_list[i].start is None:
            newstart = 0
        else:
            newstart = ss_list[i].start
        newheader['CRPIX'+str(axisno)] = newheader['CRPIX' +
                                                   str(axisno)]-newstart
        axisno += 1

    return newdata, newheader
