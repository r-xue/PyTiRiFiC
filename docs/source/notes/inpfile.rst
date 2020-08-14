Parameter File Format
=====================


Basics
------

The syntax of **ism3d** input parameter files (.inp or .ini) strictly follows the `INI`_ format, which can be easily parsed by the built-in Python module `configparser`_. 
The choice was made after a comparison among several readable plain-text syntaxes options (e.g., json/yaml/xml/TOML), mainly due to the simplifcity and wide support from many other languages for the `INI`_ format.
It's also very readable and easy to write, much less verbose than other syntaxs, and support inline comments (starting with "#").
Foundamentally, the file content is always divided into **sections**, each of which contains keys with values.

However, `INI`_ is not designed as a data interchange format (not strongly typed), and `configparser`_ natively do not guess datatypes of values and always storing them internally as string,
`INI`_ files are also typically limited to two levels and doesn't support arbitary nesting.
To support more advantages features need for our purpose, we build an under-layer interpreter to further convert the string-based input values into datatype-sensitive nested dictionary using `ASTEVAL`_.
This nested dictionary not only specifiy individual source models, but also contain the metadata of observed data and control model rendering and fitting workflows.
Here, we describe some useful features built-in the parameter file intepreter and how to use sections to manage modeling workflows.


.. _configParser: https://docs.python.org/3/library/configparser.html
.. _parameters.inp: https://github.com/r-xue/GMaKE/blob/master/gmake/parameters.inp
.. _INI: https://en.wikipedia.org/wiki/INI_file
.. _ASTEVAL: https://newville.github.io/asteval


Interpreter
-----------

DataType/Expression Support
^^^^^^^^^^^^^^^^^^^^^^^^^^^

All values associated with individual keys will be evaluated by `ASTEVAL`_, which treats strings as mathematical expressions and statements (an alterantive to `ast.literal_eval()`_ or the built-in "evil" `eval()`_). 
Therefore, all values specified within parameter files should be written as Python literals（e.g., string representations of Python objects). They are evaluated and mapped into desired data types (see the example below). 
Beside the default built-in Python datatypes, we also include some objects from astropy (e.g., ``astropy.units`` and ``astropy.coordinates.SkyCoord``).
Specifcailly, we add the following notation into the `ASTEVAL`_ symtable::

    u           : astropy.units
    Angle       : astropy.coordiante.Angle
    Quantity    : astropy.units.quantity
    SkyCoord    : astropy.coordinates.SkyCoord
    np          : numpy


.. code-block:: ini

    [disk1] 
    type          =      'disk3d'
    import        =      'basics'
    z           =        4.06
    xypos       =        SkyCoord(ra=0,dec=0,unit="deg")
    contflux     =       (0.00001 * u.Unit('Jy'),20* u.Unit('GHz'),1.0)
    pa          =        (70+90)*u.deg
    inc         =        60.00*u.deg
    sbProf       =       ('norm2d',40*u.kpc)


.. _ast.literal_eval(): https://docs.python.org/3/library/ast.html#ast.literal_eval
.. _eval(): https://docs.python.org/3/library/functions.html#eval

While `ASTEVAL`_ generally determines the value content and type, we note that the converted datatypes for some individual parameters will further passed through further parsing and converted into restricted object types.
For example, ``xypos`` will be saved as a SkyCoord object although it can be written as a two-element tuple, a string, or a litereal expression of SkyCoord.

In addition, the built-in interpreter in ``ism3d`` will check parsed datatype with the expected datatype of each keyword, and provide warning when unexpected values are detected (e.g. the position angle keyword ``pa`` should not be a string).

The datatype-sensitive extension from traditional `INI`_ files is similar to the design built in the `TOML`_ format and its parsers.
However, we decide to use a custome interpreter to not only handle basic datatype, but also support advanced datatypes and literal mathematical expression. The built-in interpreter will decide and check on value datatype expected for individual keywords (as the ``xypos`` example above)

.. _TOML: https://en.wikipedia.org/wiki/TOML

.. code-block:: ini

    [object1] 
    ...
    xypos       =        SkyCoord(ra=0,dec=0,unit="deg")    # option 1
    xypos       =        '23h46m09.4373s +12d49m19.2479s'   # option 2
    xypos       =        (189.2933333-1*40/3600,62.3711111+1*15/3600)  # option 3
    ...


If the first ASTEVAL evaluation fails, the program will:

    do split() -> re-evaluate on each element -> assemble the results into a list -> assign the list to the keyword
    This feature is only designed to work a backend solution for some special paramater input files 



The data/output file paths are specified in relative to the working directory (where you lunch GMaKE, either using CLI or a Python script).
To clear up any confusion, absolute paths can also be used.
    

Section/Keyword Reference
^^^^^^^^^^^^^^^^^^^^^^^^^

The keywords from one section will not inference keywords from another section with a different section name.
In another word, a keyword will only reside within a section (or local)

Section referencing is introduced to link the parameters from one section (with dedicated purposes) to one keyword of another section.
For example, we can link a section describing gravitional potential to the rotation curve of a disk model (see ``basics.rcProf``):
    
    rcProf         =      ('potential','pots')

Another important application of section referencing is sharing common parameters between different sections. 
Specifcailly, a set of keyword which can be "imported" into another input section using the syntax ``import = 'section_name'``
Then a group of parameters can be shared across several sections of different purpose
For example, if two emission lines arised from the same thin-disk galaxy geometry but with different spatial distribution in the disk plane,
we can write the parameters describing disk geometry into one paramater section and only reference them from other two sections actually specifiying line models. This will simplying model fitting and reduce redudent paramater requirements (see ``co43.import`` and ``ci10.import``):

.. code-block:: ini

    import             =  'basics'

Note that the place where this line is will be important as inp2mod will overwrite existing keywords by design

Keyword referencing can be used to "tie" different parameters within a section or even across differen section. In the example below, ``ci10.lineflux`` is set to a third of the value of ``co43.lineflux`` as:

.. code-block:: ini

    lineflux           =  co43['lineflux']/3

In general, 'A[b]', "b@A", or "${A:b}" is interpreted as the value of the keyword "b" from Section "A".
Value slicing is supported, as 'A[b][2]', "b[2]@A", or "${A:b}[2]" is interpreted as the third element of the "b" value from Section "A". 
e.g. "pa@co21disk" = the position angle of the components named "co21disk"
This capability is similar to the function of `configparser.ExtendedInterpolation`_.
More advanced mathmetical expressions and keyword reference can be combiend together, for example:

.. code-block:: ini

    px = 2.0*(py@objz)  
    px = sqrt(2*(py@objz))  

as long as it follows the correct referening syntax and the expression can be understood by `ASTEVAL`_.

.. _configparser.ExtendedInterpolation: https://docs.python.org/3/library/configparser.html#configparser.ExtendedInterpolation

.. code-block:: ini


    [basics]
    object         =    'bx610'
    z              =    2.21
    pa             =    -54.22660862671279 * u.Unit('deg')
    inc            =    46.24786218695453 * u.Unit('deg')              
    xypos          =    '23h46m09.4373s +12d49m19.2479s' # or SkyCoord('23h46m09.4373s +12d49m19.2479s',frame='icrs')
    vsys           =      104 * u.Unit('km / s')
    rcProf         =      ('potential','pots')
    vSigma         =        50.430210605487204 * u.Unit('km / s')
    vrot_rpcorr    =      True

    [pots]
    type           =      'potential'
    import         =      'basics'
    expdisk        =      (1000.2938616145047 * u.Unit('solMass / pc2'),3.5 * u.Unit('kpc'))
    dexpdisk       =       (10 * u.Unit('solMass / pc3'),3.5 * u.Unit('kpc'),0.5 * u.Unit('kpc'))
    nm3expdisk     =       (10 * u.Unit('solMass / pc3'),3.5 * u.Unit('kpc'),0.5 * u.Unit('kpc'),True)
    nfw            =      (500000000000.0 * u.Unit('solMass'),2.21)
    isochrone      =      (10**10*u.Unit('solMass'),0.1*u.kpc)
    kepler         =       10**10*u.Unit('solMass')

    [co43]
    type               =  'disk3d'
    import             =  'basics'
    note               =  'CO 4-3 of BX610 in BB2'
    vis                =   '../data/bx610/alma/2013.1.00059.S/bb3.ms.pt2'
    restfreq           =  461.0407682 * u.Unit('GHz')
    lineflux           =  1.4 * u.Unit('Jy km / s')
    sbProf             =  ('sersic2d',2.0*u.kpc,1)
    vbProf             =  ('sech',0.25*u.kpc)

    [ci10] 
    type               =  'disk3d'
    import             =  'basics'
    note               =  'CI 1-0 of BX610 in BB2'
    vis                =  '../data/bx610/alma/2013.1.00059.S/bb1.ms.pt2'
    restfreq           =  492.160651 * u.Unit('GHz')
    lineflux           =  co43['lineflux']/3
    sbProf             =  ('sersic2d',3.0*u.kpc,1)
    vbProf             =  ('sech',0.5*u.kpc)    


Section Types
-------------

As any `INI`_ configuration file, the basic strcuture of **ism3d** parameter file compose of **sections**.
Related key-value pairs are grouped into arbitarily named sections, names of which appear in square brackets (``[`` and ``]``).

Each section usually describes one specific aspect of parameterized models or provides controls on planned workflow tasks, i.e.  Source Specifications, Modeling Workflows, MISC.

One named parameter section generally fall into one of the following categories:

Source Model (type='disk3d' or type='apmodel')
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    A "source-model" section describes the physical properties of a emission component (either line or continuum), with the 
    section name as its identification. The keyword ``type`` can be `disk3d` or `apmodel`, which determine how the emission model is constructured and rendered.

Dynamical Model (type='potential')
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    A "dynamics-model" section describes the properties of a dynamical component, and its content will be used to specify kinematic model (e.g. rotational curve, veloccity dispersion) for line emission component(s). 
    Its section name (or i.d.) is usually referenced in the keyword `rcProf` of "source-model" sections.
    By combing a "dynamics-model" model with the prescription of line emission spatial distribution (from a "source-model" section, ``ism3d`` can construct the representation of a line emission in a spectral cube dimension. 

Lense Model (type='lens')
^^^^^^^^^^^^^^^^^^^^^^^^^

    A "lens-model" section describe the properties of a lensing model betwen the observer and simulated source

Database (type='data')
^^^^^^^^^^^^^^^^^^^^^^

    A "database" section specify the metadata of actual or simulated data  which will be used by ``ism3d``.
    The content can include file paths of FITS image/spectral-cube to be models or MeasurementSet to be fitted, or any ancillary data useful for modelling (PSF images, uncertainty images/cube)

Workflow Management with Reserved Section Names
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    Several section names are resevered for workflow managment (especially useful for the CLI interface)

    ``[ism3d.optimize]``
    
    The ``ism3d.optimize`` section specify how the program performs parameter optimization (i.e. model fitting)
    
    ``[ism3d.analyze]``   
    
    The ``ism3d.analyze`` section control how the program runs diagnostics analysis and plotting from modelling results.
    
    ``[ism3d.general]``
    
    The ``ism3d.general`` section provide general configuration information for ``ism3d`` (e.g., specifying the location of output files or working folders)


.. code-block:: ini

    ##########################################################################################
    [disk1] # specifications of disk1 
    ##########################################################################################

    type          =      'disk3d'
    import        =      'basics'
    z           =        4.06
    xypos       =        (189.2933333+0*40/3600,62.3711111+1*15/3600)
    contflux     =       (0.00001 * u.Unit('Jy'),20* u.Unit('GHz'),8.0)
    pa          =        70.00*u.deg
    inc         =        60.00*u.deg
    sbProf       =       ('norm2d',40*u.kpc)

    ###########################################################################################
    [disk2] # specifications of disk2 (eqvauilent to disk1, despite different rendering option
    ###########################################################################################

    type          =       'apmodel'
    z            =       4.0548
    xypos        =       (189.2933333+0*40/3600,62.3711111+0*15/3600)
    contflux     =       (0.001 * u.Unit('Jy'),46 * u.Unit('GHz'),3.0)
    sbProf       =       ('Gaussian2D',40*u.kpc,20*u.kpc,70*u.deg)

    ##########################################################################################
    [sie1] # lense model 
    ##########################################################################################

    type        = 'lens'
    xypos       =        '12h37m11.89s +62d22m11.8s'
    lsProf      =  ('sie',10*u.arcsec,0.5,70*u.deg)


Keyword-Value
----------------------

We provide a detailed table of all available keywords for different section types (see above)





