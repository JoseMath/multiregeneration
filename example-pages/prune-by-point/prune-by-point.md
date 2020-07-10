<link rel="stylesheet" href="modest.css">
<style>
pre, code, pre code {
  max-height: 400px;
}
</style>
## Saturation using `pruneByPoint`

#### Authors: [Colin Crowley](https://sites.google.com/view/colincrowley/home) and [Jose Israel Rodriguez](https://www.math.wisc.edu/~jose/)

It is often the case that the solution set to a system of polynomials 
contains many irreducible components, only some of which are of 
interest. We will demonstrate how to saturate out unwanted components 
using the user defined method `pruneByPoint`. We view regeneration as 
analogous to exploring a tree (or a graph), and so we call this method 
`pruneByPoint` because it "prunes" a branch of the search tree.

### Defining equations

Consider the variety consisting of points $(x,y,z) \in \mathbb{C}^3$ 
defined by the following equation.

$$
(x-y)(x^2+y^2+z^2) = 0
$$

This variety consists of the union of the quadratic hypersurface $x^2 + 
y^2 + z^2 = 0$ together with the hyperplane $x - y = 0$. Say we want a 
witness set for the component $x^2 + y^2 + z^2 = 0$.


### Input format

There are four files that comprise the input to multiregeneration.py.

#### inputFile.py
```python
degrees = [[3]]
verbose = 1
def pruneByPoint(coordinates):
    # If x-y is satisfied to within a 
    # tolerance of 1e-10, then the point will lie on the 'extra' 
    # component, and should be pruned.

    if abs(coordinates[0] - coordinates[1]) < 1e-10:
      return True
    else:
      return False
```
This file contains the multidegrees of the defining equations, as well 
as additional options. The command `verbose=1` tells 
multiregeneration.py to display a progress update.

The method prune by point is define by the user. It returns `True` if 
the given point lies on an unwanted component, and `False` otherwise. The 
argument `coordinates` is a list of complex numbers representing the 
coordinates of a point. (The coordinates are not separated into variable 
groups.)

In this example, a point is ignored if it satisfies $x-y$ to within a 
tolerance of $10^{-10}$.

#### bertiniInput_variables
```c
variable_group x,y,z;
```
#### bertiniInput_equations
```c
function f;

f = (x-y)*(x^2+y^2+z^2);
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
variable_group x,y,z;

Solutions are found in run/_completed_smooth_solutions and:
depth >= 0 satisfy f = 0

Exploring tree in order depthFirst

################### Starting multiregeneration ####################

PROGRESS
Depth 0: 2

------------------------------------------------------------------
| # of smooth isolated solutions | # of general linear equations |
| found                          | added with variables in group |
------------------------------------------------------------------
                                 | 0
----------------------------------------------------------------
  2                                2  
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
    ├── solution_tracking_depth_0_gens_1_dim_2_varGroup_0_regenLinear_2_pointId_164244926985_420259138669
    └── solution_tracking_depth_0_gens_1_dim_2_varGroup_0_regenLinear_2_pointId_164244926985_467325455839

1 directory, 2 files
```

The folder `depth_0` contains the two point on intersection of 
$x^2+y^2+z^2 = 0$ and the 
linear equation `l[0][0]`, which can be found in 
`run/_tracking_information`.
The two points are the following.
```bash 
$ cat run/_completed_smooth_solutions/depth_0/*

1.118119938371418e+00 1.000657557857476e+00
-1.346697422340464e+00 3.867478121940165e-01
4.142097786351300e-01 -1.443768148389819e+00

-7.993693379292369e-01 -5.015364124123406e-01
-4.938099911246115e-01 3.771925837430750e-01
-2.843431885126573e-01 7.549024283993541e-01
```
