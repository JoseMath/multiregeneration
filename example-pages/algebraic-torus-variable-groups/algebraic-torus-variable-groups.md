<link rel="stylesheet" href="modest.css">
<style>
pre, code, pre code {
  max-height: 400px;
}
</style>
## Use of `algebraicTorusVariableGroups`

#### Authors: [Colin Crowley](https://sites.google.com/view/colincrowley/home) and [Jose Israel Rodriguez](https://www.math.wisc.edu/~jose/)

Here we demonstrate how to use the user defined variable 
`algebraicTorusVariableGroups`. If, in the relevant application, solutions with 
zeros in certain variable *groups* should be ignored, the user may specify 
this and `multiregeneration.py` will save time by not tracking these 
points.

### Defining equations

Consider the multiaffine variety consisting of points $(x,y,z) \in 
\mathbb{C} \times \mathbb{C}^2$ defined by the following equation.

$$
xyz = 0
$$

Variable group number zero is $x$, and variable group number one is 
$y,z$.

This variety consists of the union of the three coordinate hyperplanes. 
Say we are interested in components of the solution set where the 
variables $\{y,z\}$ achieve nonzero values.
(In this example, the plane $x = 0$ is the only such component.)


### Input format

There are four files that comprise the input to multiregeneration.py.

#### inputFile.py
```python
degrees = [[1,2]]
verbose = 1
algebraicTorusVariableGroups = [1]
```
This file contains the multidegrees of the defining equations, as well 
as additional options. The command `verbose=1` tells 
multiregeneration.py to display a progress update.

The list `algebraicTorusVariableGroups` tells `multiregeneration.py` that all 
points with zeros in variable group one (i.e. $\{y,z\}$) should be thrown away.

#### bertiniInput_variables
```c
variable_group x;
variable_group y,z;
```
#### bertiniInput_equations
```c
function f;

f = x*y*z;
```
#### bertiniInput_trackingOptions
```
SecurityLevel:1;
```

### Running multiregeneration.py

Make sure that the four files discussed above are in your current 
directory.
```bash
$ ls
bertiniInput_equations  bertiniInput_trackingOptions  bertiniInput_variables  inputFile.py
```
and then run multiregeneration.py from this directory using python.
```bash
python /path/to/multiregeneration.py
```
The output will look like the following.
```
################### Setup multiregeneration ####################

These variable groups have been selected:
variable_group x;
variable_group y,z;

Solutions are found in run/_completed_smooth_solutions and:
depth >= 0 satisfy f = 0

Exploring tree in order depthFirst

################### Starting multiregeneration ####################

PROGRESS
Depth 0: 1

------------------------------------------------------------------
| # of smooth isolated solutions | # of general linear equations |
| found                          | added with variables in group |
------------------------------------------------------------------
                                 | 0  1
----------------------------------------------------------------
  1                                0  2  
Done.
```

### A witness set
While multiregeneration.py is running, it creates a directory called 
`run` where it stores the partial witness set data. This data is 
organized in the folder `run/_completed_smooth_solutions`.
```bash
$ tree run/_completed_smooth_solutions
run/_completed_smooth_solutions/
└── depth_0
    └── solution_tracking_depth_0_gens_1_dim_0_2_varGroup_0_regenLinear_0_pointId_866084791946_158664827564

1 directory, 1 file
```

The folder `depth_0` contains the point of intersection of 
$x = 0$ a random linear equations. This point is the following.
```bash 
$ cat run/_completed_smooth_solutions/depth_0/*

-4.048696831470263e-16 8.173382666818587e-16
-9.077031676898859e-01 -3.943108899739126e-01
-7.428696303170752e-01 3.495090812140431e-01
```
