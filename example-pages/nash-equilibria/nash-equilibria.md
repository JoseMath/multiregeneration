<link rel="stylesheet" href="modest.css">
<style>
pre, code, pre code {
  max-height: 400px;
}
</style>
## Finding Nash Equilibria

#### Authors: [Colin Crowley](https://sites.google.com/view/colincrowley/home), [Jose Israel Rodriguez](https://www.math.wisc.edu/~jose/), Jacob Weiker, and Jacob Zoromski

For a derivation of this system and how to solve it with 
polyhedral homotopy methods ([PHCpack](https://homepages.math.uic.edu/~jan/PHCpack/phcpack.html)), see Chapter 6 of [Sturmfels2002](https://math.berkeley.edu/~bernd/cbms.pdf). 


### Defining equations
For a 2 player game with $n$ pure strategies we have the following setup. 
Player $A$ and Player $B$ have the $n\times n$ payoff matrices $[A_{ij}]$  and $[B_{ij}]$ 
where the $(i,j)$th entry represents the payout to the player for playing pure strategy $i$
when the other plays pure strategy $j$.
When $n = 2$,  the solution set to the polynomial system 
$$
\begin{align*}
a_1 + a_2 &=1  				&b_1 + b_2  &=1  \\
 a_1(\Pi_a - A_{11}b_1 - A_{12}b_2) &= 0 & b_1(\Pi_b - B_{11}a_1 - B_{21}a_2) &=0 \\
a_2(\Pi_a - A_{21}b _1 - A_{22}b_2) &=0  & b_2(\Pi_b - B_{12}a_1 - B_{22}a_2) &=0  
\end{align*}
$$
with the variables group grouped as $(a_1,a_2)$ and $(b_1,b_2)$ respectively
and 
where 
$$
\begin{align*}
\Pi_a :&= A_{11}a_1b_1+A_{12}a_1b_2+A_{21}a_2b_1+ A_{22} a_2 b_2\\
\Pi_b :&= B_{11}a_1b_1+B_{12}a_1b_2+B_{21}a_2b_1+ B_{22} a_2 b_2,
\end{align*}
$$
contains the set of mixed Nash equilibria.

### Input format

There are four files that comprise the input to multiregeneration.py

#### inputFile.py
```python
degrees = [[1,0],[0,1],[2,1],[2,1],[1,2],[1,2]]
verbose = 1
```
This file contains the multidegrees of the defining equations, as well 
as additional options. The command `verbose=1` tells 
multiregeneration.py to display a progress update.

#### bertiniInput_variables
```c
variable_group a_1,a_2 ;
variable_group b_1,b_2 ;
```
#### bertiniInput_equations
```c
constant ii;
ii=I;
constant A_11,A_12,A_21,A_22;
constant B_11,B_12,B_21,B_22;

A_11 =9  ;
A_12 = 13;
A_21 = 20;
A_22 = 6;

B_11 = 16;
B_12 = 20;
B_21 = 12;
B_22 =  11;

function ga,gb,f0, f1, f2, f3;
ga= a_1+a_2-1;
gb= b_1+b_2-1;

f0 = a_1*(A_11*a_1*b_1+A_12*a_1*b_2+A_21*a_2*b_1+ A_22* a_2* b_2 - (A_11*b_1 + A_12*b_2) );
f1 = a_2*(A_11*a_1*b_1+A_12*a_1*b_2+A_21*a_2*b_1+ A_22* a_2* b_2 - (A_21*b_1 + A_22*b_2) );
f2 = b_1*(B_11*a_1*b_1+B_12*a_1*b_2+B_21*a_2*b_1+ B_22* a_2* b_2 - (B_11*a_1 + B_21*a_2) ) ;
f3 = b_2*(B_11*a_1*b_1+B_12*a_1*b_2+B_21*a_2*b_1+ B_22* a_2* b_2 - (B_12*a_1 + B_22*a_2) ) ;
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
variable_group a_1,a_2 ;
variable_group b_1,b_2 ;

Solutions in a 'linearProduct' directory and :
depth >= 0 satisfy ga = 0
depth >= 1 satisfy gb = 0
depth >= 2 satisfy f0 = 0
depth >= 3 satisfy f1 = 0
depth >= 4 satisfy f2 = 0
depth >= 5 satisfy f3 = 0
exploring tree in order depthFirst

################### Starting multiregeneration ####################

PROGRESS
Depth 0: 1
Depth 1: 1
Depth 2: 3
Depth 3: 3
Depth 4: 5
Depth 5: 5

----------------------------------------------------------------
| # smooth isolated solutions  | # of general linear equations |
| found                        | added with variables in group |
----------------------------------------------------------------
                               | 0  1
----------------------------------------------------------------
  5                              0  0  
Done.
```

### Solutions
While multiregeneration.py is running, it creates a directory called 
`run` where it stores the partial solution data. This data is 
organized in the folder `run/_completed_smooth_solutions`.
```bash
$ tree run/_completed_smooth_solutions/
run/_completed_smooth_solutions/
├── depth_0
│   └── solution_tracking_depth_0_gens_1_dim_1_2_varGroup_1_regenLinear_1_pointId_999166306418_123674091215
├── depth_1
│   └── solution_tracking_depth_1_gens_1_1_dim_1_1_varGroup_1_regenLinear_1_pointId_123674091215_571837852155
├── depth_2
│   ├── solution_tracking_depth_2_gens_1_1_1_dim_0_1_varGroup_1_regenLinear_1_pointId_571837852155_248959257075
│   ├── solution_tracking_depth_2_gens_1_1_1_dim_0_1_varGroup_1_regenLinear_1_pointId_571837852155_467837258827
│   └── solution_tracking_depth_2_gens_1_1_1_dim_1_0_varGroup_1_regenLinear_1_pointId_571837852155_713170692613
├── depth_3
│   ├── solution_vanishing_depth_3_gens_1_1_1_0_dim_0_1_pointId_248959257075_248959257075
│   ├── solution_vanishing_depth_3_gens_1_1_1_0_dim_0_1_pointId_467837258827_467837258827
│   └── solution_vanishing_depth_3_gens_1_1_1_0_dim_1_0_pointId_713170692613_713170692613
├── depth_4
│   ├── solution_tracking_depth_4_gens_1_1_1_0_1_dim_0_0_varGroup_1_regenLinear_1_pointId_248959257075_473775690656
│   ├── solution_tracking_depth_4_gens_1_1_1_0_1_dim_0_0_varGroup_1_regenLinear_1_pointId_248959257075_917556880335
│   ├── solution_tracking_depth_4_gens_1_1_1_0_1_dim_0_0_varGroup_1_regenLinear_1_pointId_467837258827_132778330808
│   ├── solution_tracking_depth_4_gens_1_1_1_0_1_dim_0_0_varGroup_1_regenLinear_1_pointId_467837258827_870108075393
│   └── solution_tracking_depth_4_gens_1_1_1_0_1_dim_0_0_varGroup_1_regenLinear_1_pointId_713170692613_601058697586
└── depth_5
    ├── solution_vanishing_depth_5_gens_1_1_1_0_1_0_dim_0_0_pointId_132778330808_132778330808
    ├── solution_vanishing_depth_5_gens_1_1_1_0_1_0_dim_0_0_pointId_473775690656_473775690656
    ├── solution_vanishing_depth_5_gens_1_1_1_0_1_0_dim_0_0_pointId_601058697586_601058697586
    ├── solution_vanishing_depth_5_gens_1_1_1_0_1_0_dim_0_0_pointId_870108075393_870108075393
    └── solution_vanishing_depth_5_gens_1_1_1_0_1_0_dim_0_0_pointId_917556880335_917556880335

6 directories, 18 files
```

The folder `depth_5` contains the isolated solutions to the whole 
system, which are:
```bash
$cat run/_completed_smooth_solutions/depth_5/*

3.027488683426075e-287 -4.713551932326410e-289
9.999999999999999e-01 0.000000000000000e+00
5.043949224142953e-15 5.031911447161615e-16
9.999999999999951e-01 -4.996003610813204e-16

1.000000000000000e+00 -1.110223024625157e-16
-5.091759685681027e-17 -2.225610541722674e-17
1.178176334919242e-13 -3.022904202283731e-13
9.999999999998821e-01 3.022027073029676e-13

1.999999999999998e-01 1.887379141862766e-15
8.000000000000002e-01 -1.915134717478395e-15
3.888888888888890e-01 4.163336342344337e-17
6.111111111111109e-01 -2.775557561562891e-17

8.544437010279772e-186 -1.499077989632200e-185
9.999999999999999e-01 0.000000000000000e+00
9.999999999998188e-01 -8.826273045769994e-15
1.810237935765253e-13 8.792840477452395e-15

1.000000000000000e+00 5.551115123125783e-17
-4.463139253907902e-17 -4.332714115960878e-17
1.000000000000009e+00 3.103073353827313e-14
-9.040395543972030e-15 -3.085170806852074e-14
```
We see that there is one totally mixed nash equilibrium (i.e. an 
equilibrium with no zero coordinates). If we only want the totally mixed 
Nash equilibria, then we could add the line 
`algebraicTorusVariableGroups = [0,1]` to `inputFile.py`.
