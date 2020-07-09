<link rel="stylesheet" href="modest.css">
<style>
pre, code, pre code {
  max-height: 400px;
}
</style>
## Regenerating the twisted cubic

#### Authors: [Colin Crowley](https://sites.google.com/view/colincrowley/home), and [Jose Israel Rodriguez](https://www.math.wisc.edu/~jose/)

We will demonstrate how multiregeneration.py handles noncomplete 
intersections using the classical example of the twisted cubic.

### Defining equations
The twisted cubic is the image of the map $$\mathbb{P}^1 \to 
\mathbb{P}^3$$ given by $$[t_0:t_1] \mapsto [t_0^3: t_0^2t_1: t_0t_1^2: 
t_1^3].$$

The image is implicitly given as the set of points $[x_0:x_1:x_2:x_3] 
\in \mathbb{P}^3$ which satisfy the following equations.
$$
\begin{align*}
    f_0 &= x_1^2 - x_0x_2\\
    f_1 &= x_2^2 - x_1x_3\\
    f_2 &= x_0x_3 - x_1x_2
\end{align*}
$$
The twisted cubic is not a *complete intersection* in the sense that it 
is codimension $2$ but it cannot be defined by only two equations. 
Geometrically, the first two equations define an algebraic set 
consisting of the twisted cubic together with the line $x_1=x_2=0$, and 
the third equation cuts away this extra line. This can be seen easily 
with the help of "Macaulay2":

```
i1 : R = QQ[x_0..x_3]

o1 = R

o1 : PolynomialRing

i2 : decompose ideal(x_1^2 - x_0*x_2, x_2^2 - x_1*x_3)

                2            2
o2 = {ideal (- x  + x x , - x  + x x , - x x  + x x ), ideal (x , x )}
                1    0 2     2    1 3     1 2    0 3           1   2

o2 : List
```

We now demonstrate how to use multiregeneration.py to compute a witness 
set for the twisted cubic.

### Input format

There are four files that comprise the input to multiregeneration.py

#### inputFile.py
```python
degrees = [[2], [2], [2]]
verbose = 1
```
This file contains the multidegrees of the defining equations, as well 
as additional options. For example, `verbose=1` tells 
multiregeneration.py to display a progress update.

#### bertiniInput_variables
```c
hom_variable_group x_0, x_1, x_2, x_3;
```
#### bertiniInput_equations
```c
function f0, f1, f2;

f0 = x_1^2 - x_0*x_2;
f1 = x_2^2 - x_1*x_3;
f2 = x_0*x_3 - x_1*x_2;
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
hom_variable_group x_0, x_1, x_2, x_3;

Solutions are found in run/_completed_smooth_solutions and:
depth >= 0 satisfy f0 = 0
depth >= 1 satisfy f1 = 0
depth >= 2 satisfy f2 = 0

Exploring tree in order depthFirst

################### Starting multiregeneration ####################

PROGRESS
Depth 0: 2
Depth 1: 4
Depth 2: 3

------------------------------------------------------------------
| # of smooth isolated solutions | # of general linear equations |
| found                          | added with variables in group |
------------------------------------------------------------------
                                 | 0
----------------------------------------------------------------
  3                                1  
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
│   ├── solution_tracking_depth_0_gens_1_dim_2_varGroup_0_regenLinear_3_pointId_602645055533_44034358559
│   └── solution_tracking_depth_0_gens_1_dim_2_varGroup_0_regenLinear_3_pointId_602645055533_826344570835
├── depth_1
│   ├── solution_tracking_depth_1_gens_1_1_dim_1_varGroup_0_regenLinear_3_pointId_44034358559_946411662718
│   ├── solution_tracking_depth_1_gens_1_1_dim_1_varGroup_0_regenLinear_3_pointId_44034358559_957654796862
│   ├── solution_tracking_depth_1_gens_1_1_dim_1_varGroup_0_regenLinear_3_pointId_826344570835_426332278539
│   └── solution_tracking_depth_1_gens_1_1_dim_1_varGroup_0_regenLinear_3_pointId_826344570835_931580444520
└── depth_2
    ├── solution_vanishing_depth_2_gens_1_1_0_dim_1_pointId_426332278539_426332278539
    ├── solution_vanishing_depth_2_gens_1_1_0_dim_1_pointId_946411662718_946411662718
    └── solution_vanishing_depth_2_gens_1_1_0_dim_1_pointId_957654796862_957654796862

3 directories, 9 files
```

The folder `depth_k` contains the data of a witness set collection for 
the system $f_0, \ldots, f_{k}$. We see that a witness set for the 
variety $f_0=f_1=0$ consists of four point, which is expected since $f_0 
= f_1 = 0$ describes a cubic curve together with a line. A witness set 
for the twisted cubic $f_0 = f_1 = f_2 = 0$ consists of one less point, 
since the extra line $x_1 = x_2 = 0$ is not included.

Therefore a witness system for the twisted cubic is given by the 
equations $f_1, f_2$, the linear equation `l[0][2]` which can be found 
in `run/_tracking_information` and the following points.
```bash 
$ cat run/_completed_smooth_solutions/depth_2/*

1.000000000000000e+00 0.000000000000000e+00
8.655494693944729e-01 -3.179513979168430e-02
7.481649530546808e-01 -5.504053275203097e-02
6.458237567029602e-01 -7.142831318832180e-02

1.000000000000000e+00 0.000000000000000e+00
-2.883834575360769e-01 8.488700931892024e-01
-6.374154165305825e-01 -4.896001849457478e-01
5.994270163262361e-01 -3.998902898855923e-01

1.127050539992347e-02 9.992386941399086e-01
4.932446428984644e-01 -8.693557963587947e-01
-8.639384885191288e-01 5.031352393206544e-01
1.000000000000000e+00 0.000000000000000e+00
```
