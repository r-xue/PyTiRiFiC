Input File Format
=================

Basics
~~~~~~
The content of a **GMaKE** input parameter file is always divided into **sections**.
Any line begins with ``@`` (followed with the **section name**) marks the beginning of a new input section (see `examples <https://github.com/r-xue/GMaKE/tree/master/examples/inpfile>`_).
Each section usually describes one specific aspect of parameterized models or provides controls on how the program works.

Sections
~~~~~~~~

A input section should fall into one of the following categories:

+ Model Properties

    ``@ emission_component_name``
    
    The section describes the physical properties of a emission component (either line or continuum), with a user-specified section name.
    Its content will be parsed and used by **GMaKE**, to build a spatially resolved multi-wavelength reference emission model.
    
    ``@ dynamics_component_name``
    
    The section describes the properties of a dynamical component, and its content will be used to a build kinematic model (e.g. rotational curve, veloccity dispersion) for line emission component(s). By combing the kinematic model with the prescription of line emission spatial distribution, **GMaKE** can construct the representation of a line emission in a spectral cube dimension. 

+ Program Controls

    ``@ optimize``
    
    a section named ``optimize``, which contains parameters controlling how the program perform parameter optimization
    
    ``@ analyze``   
    
    a section named ``analyze``, which contains parameters controlling how the program runs diagnostics analysis on fitting results.
    
    ``@ plot``      
    
    a section named ``plot``, which contains parameters controlling how the program generate diagnostic plots
    
    ``@ misc``
    
    a section named ``misc``, which contains some general configuration information on **GMaKE** (e.g., specifying the location of output files or working folders)

+ Keyword Groups

    ``@ keyword_group_name``
    
    A set of keyword which can be "imported" into another input section using the syntax ``import 'keyword_group_name'``. One good user example is a group of parameters shared across different emission components.

+ Comments

    ``@ comment/note/changlog``
    
    Any section with the name containing the following word: ``comment``, ``note``, ``changelog``. The content of such section will flagged as comments by *GMaKE*.

    
    *Note*: ``#`` still marks the beginning of inline comments or commented lines, i.a. anything behind ``#`` will not be passed to the program.

Keyword-Value Pairs
~~~~~~~~~~~~~~~~~~~~~~~~~

Within each none-comments section, every line always follow the basic keyword-value pair syntax, separated by white space.
The first word is considered as the parameter "keyword", and the rest of the line will be considered as its value.
In the **GMaKE** input file, the "value" needs to be the string representation of a Python object (think about the output of the Python function ``repr``), e.g., ::
    
    keyword1    'test'      #   a string "test" is assigned to keyword1
    keyword2    3.0         #   a float-type value of 3.0 is assigned to keyword2

The keywords from one section will not inference keywords from another section with a different section name.
In another word, a keyword will only reside within a section (or local)

+ Directory Path

Technical note:

    The program uses the Python package ASTEVAL to determine the value content and type, not the evil eval()...
    If the first ASTEVAL evaluation fails, the program will:
        do split() -> re-evaluate on each element -> assemble the results into a list -> assign the list to the keyword
        This feature is only designed to work a backend solution for some special paramater input files 
    

    
    The data/output file paths are specified in relative to the working directory (where you lunch GMaKE, either using CLI or a Python script).
    To clear up any confusion, absolute paths can also be used.
    


The magic of "@"
~~~~~~~~~~~~~~~~

+ Any line begins with '@' mark the beginning of a new section (as in this file)
    
    The section name is created from valid characters (ignoring comments) following  "@", with leading/trailing space removed
    some section names are reserved for special purposes:
        + A name containing "comment", "changelog", "ignore" is considered as comments and the content in that section will be discarded by the program
        + A name containing "optimize" denote the parameter section control the optimization. 
        + A name not meeting the above standard will be considered as a model component

+ denote the "parent" object of a parameter:
    e.g. "pa@co21disk" = the position angle of the components named "co21disk"

+ Tie the parameter values:
    
    when a parameter value is set to a string containing "@", it means its value is tied to a math expression of some other parameter(s)
    e.g.    if 'vdis@co21disk' is assigned to 'vdis' in the object '@co10disk' parameter section, 
            then the value of 'vdis@co10disk' is always tied to that of 'vdis@co21disk' in modeling.
            if '2.*influx@line1' is assigned to 'intflux' in the object '@line2' parameter section,
            then the value of 'intflux@line2' is always twice of 'flux@line1'

+ one can cross-reference all keywords from a different section by using

    import    'sectionname'
    the place where this line is will be important as inp2mod will overwrite existing keywords by design

+ cross reference will only work at 1st level.

Others
~~~~~~

Special syntax in parameter input files:

**"@"**:

+ tag the parameter set associated with a specific object; in short, "A@B" = A of B
+ tie different parameters across different.
A simple math function could be implemented in future, e.g.,
*px = 2.0\*(py@objz)*; *px = sqrt(\*(py@objz))*


**"#"**:

+ user comments, not read by the ***gmake_utils/gmake_readpars***
+ @comments / @changelog can be also used for comments/notes
