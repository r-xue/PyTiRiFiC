Special syntax in parameter input files:

**"@"**:

+ tag the parameter set associated with a specific object
+ tie different parameters across different.
A simple math function could be implemented in future, e.g.,
*px = 2.0\*(py@objz)*; *px = sqrt(\*(py@objz))*


**"#"**:

+ user comments, not read by the ***gmake_utils/gmake_readpars***
+ @comments / @changelog can be also used for comments/notes
