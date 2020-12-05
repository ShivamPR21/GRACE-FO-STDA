# GRACE-FO-STDA

Spatio Temporal Variation analysis of GRACE-FO data and Prediction based on that. The package provides composite tools
to analyse the spatio-temporal variation of the Surface mass density of a given area.

Structure of the program is defined as

### grace_read module
Consists of 2 main functions `read`, and `read_header`. 

`read_header` used to read the header of all the files for which paths are given as input, serves as a helper function
for `read`.

`read` is the core of `grace_read` module and reads the file path provided via path list.

### preprocessing
`anomaly` function implements the method to compute the anomaly for given sc coefficients.

`filters` module implements filters to get rid of the noise in sc coefficients, presently there is only `gauss_filter` 
implemented and can be used via call upon sc anomaly.

### physics
Physics module deals with the gravity field related computations, the main calss there is `GravityField` and presently 
implements method to get the SMD(Surface mass density).

### models
This module implements different method to get the regression fit for the spatio-temporal anomalies.

### Examples
```For Usage related information please view the Docs/spatio-temporal-analysis.ipynb```