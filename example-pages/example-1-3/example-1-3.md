<link rel="stylesheet" href="modest.css">
<style>
pre, code, pre code {
  max-height: 400px;
}
</style>
## Regenerating in $\mathbb{P}^3 \times \mathbb{P}^1$

#### Authors: [Colin Crowley](https://sites.google.com/view/colincrowley/home), and [Jose Israel Rodriguez](https://www.math.wisc.edu/~jose/)

<!-- We will demonstrate how multiregeneration.py handles noncomplete --> 
<!-- intersections using the classical example of the twisted cubic. -->

Here we compute the multidegree of a specific curve in $\mathbb{P}^3 \times \mathbb{P}^1$.

### Defining equations
Consider the curve in $\mathbb{P}^3 \times \mathbb{P}^1$ given as the 
points $[x_0:x_1:x_2:x_3] \times [y_0:y_1]$ which satisfy the following 
multihomogeneus equations.
$$
\begin{align*}
    f_0 &= x_0y_0 + x_1y_1\\
    f_1 &= x_1y_0 + x_2y_1\\
    f_2 &= x_2y_0 + x_3y_1\\
\end{align*}
$$

### Input format

There are four files that comprise the input to multiregeneration.py

#### inputFile.py
```python
degrees = [[1,1], [1,1], [1,1]]
verbose = 1
```
This file contains the multidegrees of the defining equations, as well 
as additional options. 

The multidegree vector of each equations is 
$\text{deg}(f_i) = (1,1)$, since each equation is linear in the 
variable group $\{x_i\}$ and also linear in the variable group 
$\{y_i\}$. In general the variable `degree` should be set to 
$(\text{deg}(f_0), \text{deg}(f_1), \ldots, \text{deg}(f_{n-1}))$, which 
in this case is $((1,1), (1,1), (1,1))$.

The option `verbose=1` tells 
multiregeneration.py to display a progress update.

#### bertiniInput_variables
```c
hom_variable_group x_0, x_1, x_2, x_3;
hom_variable_group y_0, y_1;
```
Above are two homogeneous variable groups. Note that the order in which 
the variable groups are declared in `bertiniInput_variables` should 
reflect the order in which degrees of variable groups are listed in 
`inputFile.py`. So in this example, we have $\text{deg}(x_0y_0^2) = 
(1,2)$ and not $(2,1)$.

#### bertiniInput_equations
```c
function f0, f1, f2;

f0 = x_0*y_0 + x_1*y_1;
f1 = x_1*y_0 + x_2*y_1;
f2 = x_2*y_0 + x_3*y_1;
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
and then run multiregeneration.py from this directory using python2.
```bash
python2 /path/to/multiregeneration.py
```
The output will look like the following.
```
################### Setup multiregeneration ####################

These variable groups have been selected:
hom_variable_group x_0,x_1,x_2,x_3;
hom_variable_group y_0,y_1;

Solutions are found in run/_completed_smooth_solutions and:
depth >= 0 satisfy f1 = 0
depth >= 1 satisfy f2 = 0
depth >= 2 satisfy f3 = 0

Exploring tree in order depthFirst

################### Starting multiregeneration ####################

PROGRESS
Depth 0: 2
Depth 1: 3
Depth 2: 4

------------------------------------------------------------------
| # of smooth isolated solutions | # of general linear equations |
| found                          | added with variables in group |
------------------------------------------------------------------
                                 | 0  1
----------------------------------------------------------------
  3                                1  0  
  1                                0  1  
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
│   ├── solution_tracking_depth_0_gens_1_dim_2_1_varGroup_1_regenLinear_1_pointId_310677581240_324230684877
│   └── solution_tracking_depth_0_gens_1_dim_3_0_varGroup_1_regenLinear_1_pointId_310677581240_838208509710
├── depth_1
│   ├── solution_tracking_depth_1_gens_1_1_dim_1_1_varGroup_1_regenLinear_1_pointId_324230684877_137429507871
│   ├── solution_tracking_depth_1_gens_1_1_dim_2_0_varGroup_1_regenLinear_1_pointId_324230684877_165716873287
│   └── solution_tracking_depth_1_gens_1_1_dim_2_0_varGroup_1_regenLinear_1_pointId_838208509710_800758061260
└── depth_2
    ├── solution_tracking_depth_2_gens_1_1_1_dim_0_1_varGroup_1_regenLinear_1_pointId_137429507871_741856788249
    ├── solution_tracking_depth_2_gens_1_1_1_dim_1_0_varGroup_1_regenLinear_1_pointId_137429507871_844460712299
    ├── solution_tracking_depth_2_gens_1_1_1_dim_1_0_varGroup_1_regenLinear_1_pointId_165716873287_538383802898
    └── solution_tracking_depth_2_gens_1_1_1_dim_1_0_varGroup_1_regenLinear_1_pointId_800758061260_520778168949

3 directories, 9 files
```

The folder `depth_k` contains the data of a witness set collection for 
the system $f_0, \ldots, f_{k}$. 

Since this variety is a complete intersection $\{f_0,f_1,f_2\}$ is a 
witness system. 

The remainder of the data for a multihomogenious witness 
set is given by the intersection of the variety with linear spaces of 
codimensions $(0,1)$ and $(1,0)$. In general the intersection of the variety 
$f_0 = \ldots = f_{k} = 0$ with a linear space of codimension $(n_0, 
\ldots, n_k)$ is stored in those files of `depth_k` containing the 
string `dim_n0_..._nk`. 

In this example there is one intersection point 
with a linear space of codimension $(0,1)$ which is the following.

```bash
$ cat run/_completed_smooth_solutions/depth_2/solution_tracking_depth_2_gens_1_1_1_dim_0_1_varGroup_1_regenLinear_1_pointId_137429507871_741856788249 

5.332349620238169e-04 -8.765489370690931e-06
6.575954243512093e-03 -7.206150765581929e-05
8.109347480602777e-02 -4.443113815765128e-04
1.000000000000000e+00 0.000000000000000e+00
1.000000000000000e+00 0.000000000000000e+00
-8.109347480602816e-02 4.443113815766047e-04
```

There are three intersection points with a linear space of codimension 
$(1,0)$ which are the following.
```bash
$ cat run/_completed_smooth_solutions/depth_2/solution_tracking_depth_2_gens_1_1_1_dim_1_0*

1.000000000000000e+00 0.000000000000000e+00
-4.664599700721133e-02 7.343186944133681e-01
-5.370480959281567e-01 -6.850605524389063e-02
7.535642092149711e-02 -3.911689233912669e-01
4.664599700721150e-02 -7.343186944133679e-01
1.000000000000000e+00 0.000000000000000e+00

1.000000000000000e+00 0.000000000000000e+00
-5.107328344332152e-01 -2.361601134924009e-01
2.050764289634426e-01 2.412294482880871e-01
-4.777049195451646e-02 -1.716346726115581e-01
5.107328344332150e-01 2.361601134924012e-01
1.000000000000000e+00 0.000000000000000e+00

1.000000000000000e+00 0.000000000000000e+00
3.950360716359839e-01 -5.288454235775965e-01
-1.236239841453772e-01 -4.178260372655233e-01
-2.698013207162134e-01 -9.967837812889078e-02
-3.950360716359837e-01 5.288454235775963e-01
1.000000000000000e+00 0.000000000000000e+00
```

The linear equations defining these linear spaces are given in the 
`run/_tracking_information` as `l[0][2]` and `l[1][0]`.
