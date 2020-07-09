<link rel="stylesheet" href="modest.css">
<style>
pre, code, pre code {
  max-height: 400px;
}
</style>
## Use of `nonzeroCoordinates`

#### Authors: [Colin Crowley](https://sites.google.com/view/colincrowley/home), and [Jose Israel Rodriguez](https://www.math.wisc.edu/~jose/)

Here we demonstrate how to use the user defined variable 
`nonzeroCoordinates`. If, in the relevant application, solutions with 
zeros in certain coordinates should be ignored, the user may specify 
this and `multiregeneration.py` will save time by not tracking these 
points.

### Defining equations

Consider the multiaffine variety consisting of points $(x,y,z) \in 
\mathbb{C} \times \mathbb{C}^2$ defined by the following equation.

$$
x*y*z = 0
$$

This variety consists of the union of the three coordinate hyperplanes. 
Say we would like a witness set for all components which do not lie in 
either of the coordinate planes $x = 0$ and $y = 0$.


### Input format

There are four files that comprise the input to multiregeneration.py

#### inputFile.py
```python
degrees = [[1,2]]
verbose = 1
nonzeroCoordinates = [0,1]
```
This file contains the multidegrees of the defining equations, as well 
as additional options. The command `verbose=1` tells 
multiregeneration.py to display a progress update.

The list `nonzeroCoordinates` tells `multiregeneration.py` that all 
points with zeros in the first two coordinates should be thrown away.

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
directory
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
  1                                1  1  
Done.
```

### A witness set
While multiregeneration.py is running, it creates a directory called 
`run` where it stores the partial witness set data. This data is 
organized in the folder `run/_completed_smooth_solutions`.
```bash
$ tree run/_completed_smooth_solutions/
run/_completed_smooth_solutions/
└── depth_0
    └── solution_tracking_depth_0_gens_1_dim_1_1_varGroup_1_regenLinear_1_pointId_420399841269_434492049963

1 directory, 1 file
```

The folder `depth_0` contains the point of intersection of 
$z = 0$ and the 
linear equation `l[1][0]`, which can be found in 
`run/_tracking_information`. This point is the following.
```bash 
$ cat run/_completed_smooth_solutions/depth_0/*

3.394525056706128e-01 4.060281681158974e-01
1.326130072769161e-01 -3.428814811548347e-01
8.117682338556469e-17 4.004079930720481e-17
```
