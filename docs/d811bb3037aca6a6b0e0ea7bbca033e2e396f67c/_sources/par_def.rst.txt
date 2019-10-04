Input File Format
=================

Brief
~~~~~
The content of a input parameter file is divided into different sections/blocks.
Any line begins with '@' (followed with the section name) mark the beginning of a new section (as in this file).
Each section describe one specific aspect of parameterized models or provides controls on how the program works.


Sections
~~~~~~~~

A section should fall into one the following categories:

+ Model Properties

    @ emission_component_name   :   describe the model properties of a emission component
                                    with a user-specified section name
    
    @ dynamics_component_name   :   describe the model properties of a dynamical component
                                    with a user-specified section name

+ Program Controls

    @ optimize  :   a uniq parameter section named "optimize", which contains
                    parameters controlling how the program perform parameter optimization
    @ analyze   :   a uniq parameter section named "analyze", which contains
                    parameters controlling how the program runs analysis on the fitting results
    @ plot      :   a uniq parameter section named "plot", which contains 
                    parameters controlling how the program generate diagnostic plots
    @ misc      :   other general program control parameters

+ Parameter Groups

    @ paramater_group_name      :   a set of keyword which can be "imported" into another parameter section:
                                    for example, a set of parameters shared across different emission components

+ Comments

    @ *comments*notes*          :   any section with the name containing the following word: 
    @ *note*                        "commnet", "note", "changlog" will be marked as comments
    @ *changlog*                    and the content will not be ignored by the program
    
    note: "#" also marks the beginning of inline comments or commented line,
          i.a. anything behind it will also not be passed to the program.

Keyword-Value Pair Syntax
~~~~~~~~~~~~~~~~~~~~~~~~~

Under each none-comments section, each line always follow the basic keyword+value pair syntax, separated by white space
The first word is considered as the parameter "keyword", and the rest of the line will be considered as the value content.
The "value" part needs to be the string representation of a Python object (think about repr()), e.g.:
    'test'      :   a string type with a value of "test"
    3.0         :   a float type with a value of 3.0

Technical note:
    The program uses the Python package ASTEVAL to determine the value content and type, not the evil eval()...
    If the first ASTEVAL evaluation fails, the program will:
        do split() -> re-evaluate on each element -> assemble the results into a list -> assign the list to the keyword
        This feature is only designed to work a backend solution for some special paramater input files 
    
        
  + Directory Path
    
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
