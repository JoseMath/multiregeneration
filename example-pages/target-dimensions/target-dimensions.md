<slink rel="stylesheet" href="modest.css">
<style>
pre, code, pre code {
  max-height: 400px;
}
</style>
## Use of `targetDimensions`

#### Authors: [Colin Crowley](https://sites.google.com/view/colincrowley/home), and [Jose Israel Rodriguez](https://www.math.wisc.edu/~jose/)

Here we demonstrate how to use the user defined variable 
`targetDimensions`. This can be used when we have equations defining a 
variety, but we only care about its multidegree coefficients for certain 
multidimensions.

### Defining equations

Consider the multiaffine variety consisting of points $(x,y,z) \in 
\mathbb{C} \times \mathbb{C} \times \mathbb{C}$ defined by the following 
equations.

$$
\begin{align*}
(x^2+y+z)x &= 0\\
(x-2y^2+1)x &= 0
\end{align*}
$$


This variety consists of the union of the hyperplane defined by $x=0$ 
and the curve defined by $x^2 + y + z = 0$ and $x-2y^2+1=0$. Say we are 
only interested in the multidegree coefficient for dimension $(1,0,0)$. 
This is equivalent to asking how many isolated solutions there will be 
when a general value is chosen for $x$.


### Input format

There are four files that comprise the input to multiregeneration.py

#### inputFile.py
```python
degrees = [[3,1,1],[2,2,0]]
verbose = 1
targetDimensions = [[1,0,0]]
```
This file contains the multidegrees of the defining equations, as well 
as additional options. The command `verbose=1` tells 
multiregeneration.py to display a progress update.

The list `targetDimensions` tells `multiregeneration.py` which 
multidegree coefficients to compute.

#### bertiniInput_variables
```c
variable_group x;
variable_group y;
variable_group z;
```
#### bertiniInput_equations
```c
function f1,f2;

f1 = (x^2+y+z)*x;
f2 = (x-2*y^2+1)*x;

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
variable_group y;
variable_group z;

Solutions are found in run/_completed_smooth_solutions and:
depth >= 0 satisfy f1 = 0
depth >= 1 satisfy f2 = 0

Exploring tree in order depthFirst

################### Starting multiregeneration ####################

PROGRESS
Depth 0: 2
Depth 1: 2

------------------------------------------------------------------
| # of smooth isolated solutions | # of general linear equations |
| found                          | added with variables in group |
------------------------------------------------------------------
                                 | 0  1  2
----------------------------------------------------------------
  2                                1  0  0  
Done.
```

### A witness set
While multiregeneration.py is running, it creates a directory called 
`run` where it stores the partial witness set data. This data is 
organized in the folder `run/_completed_smooth_solutions`.
```bash
$ tree run/_completed_smooth_solutions/
run/_completed_smooth_solutions/
├── depth_0
│   ├── solution_tracking_depth_0_gens_1_dim_1_0_1_varGroup_2_regenLinear_0_pointId_261562148744_467834493564
│   └── solution_tracking_depth_0_gens_1_dim_1_1_0_varGroup_2_regenLinear_0_pointId_261562148744_699550604641
└── depth_1
    ├── solution_tracking_depth_1_gens_1_1_dim_1_0_0_varGroup_2_regenLinear_0_pointId_699550604641_304186546591
    └── solution_tracking_depth_1_gens_1_1_dim_1_0_0_varGroup_2_regenLinear_0_pointId_699550604641_561923727441

2 directories, 4 files
```

The folder `depth_1` contains the point of intersection of 
the variety in this example and the 
linear equation `l[0][0]` which can be found in 
`run/_tracking_information`.
These points are the following.
```bash 
$ cat run/_completed_smooth_solutions/depth_0/*

1.237512846685652e-02 -2.565814893562041e-01
5.894567502816868e-01 8.293254645696755e-01
-5.237758334060102e-01 -8.229750067836747e-01

1.237512846685652e-02 -2.565814893562041e-01
7.726719075507094e-03 2.917418097531476e-01
5.795419780016971e-02 -2.853913519671465e-01
```
