<link rel="stylesheet" href="modest.css">
<style>
pre, code, pre code {
  max-height: 400px;
}
</style>
## Regenerating the twisted cubic

We will demonstrate how to compute a witness set for the saturation of 
an algebraic variety by an equation, using the user defined function 
`pruneByPoint`.

### Defining equations
The example we use is the twisted cubic. 

Consider the variety $X$ consisting of those points $[x_0:x_1:x_2:x_3] \in 
\mathbb{P}^3$ on which the following vanish.
$$
\begin{align*}
    f_1 &= x_1^2 - x_0x_2\\
    f_2 &= x_2^2 - x_1x_3\\
\end{align*}
$$

This variety is the union of the twisted cubic together with the line 
$x_1=x_2=0$. To obtain the twisted cubic, we can saturate the above 
variety by the extra line. 

To do this we define a function `pruneByPoint(bfePrime, i, PPi)` in 
`inputFile.py`. The inputs

The twisted cubic is not a *complete intersection* in the sense that it 
is codimension $2$ but it cannot be defined by only two equations. 
Geometrically, the first two equations define an algebraic set 
consisting of the twisted cubic together with the line $x_1=x_2=0$, and 
the third equation cuts away this extra line.

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
multiregeneration.py to display a progress update...

#### bertiniInput_variables
```c
hom_variable_group x_0, x_1, x_2, x_3;
```
#### bertiniInput_equations
```c
function f1, f2, f3;

f1 = x_1^2 - x_0*x_2;
f2 = x_2^2 - x_1*x_3;
f3 = x_0*x_3 - x_1*x_2;
```
#### bertiniInput_trackingOptions
```
SecurityLevel:1;
```

### Running multiregeneration.py

Make sure that the four files discussed above are in your currnet 
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

Solutions in a 'linearProduct' directory and :
depth >= 0 satisfy f1 = 0
depth >= 1 satisfy f2 = 0
depth >= 2 satisfy f3 = 0

Using start solution
0.208465534309 0.838096322231
-0.237964947646 0.40102539944
0.392192600852 -0.319508409516
0.375533564086 0.643435017932

Using dimension linears
l[0][0]
(0.720028495308+I*-0.851408408375)*((0.375533564086+I*0.643435017932)*x_0-(0.208465534309+I*0.838096322231)*x_3)+(0.48440294158+I*0.308951747675)*((0.375533564086+I*0.643435017932)*x_1-(-0.237964947646+I*0.40102539944)*x_3)+(-0.357313578768+I*0.495115632213)*((0.375533564086+I*0.643435017932)*x_2-(0.392192600852+I*-0.319508409516)*x_3)
l[0][1]
(-0.428538676915+I*0.0250937940779)*((0.375533564086+I*0.643435017932)*x_0-(0.208465534309+I*0.838096322231)*x_3)+(-0.610868370016+I*0.0271485946123)*((0.375533564086+I*0.643435017932)*x_1-(-0.237964947646+I*0.40102539944)*x_3)+(-0.95279658392+I*-0.253642041076)*((0.375533564086+I*0.643435017932)*x_2-(0.392192600852+I*-0.319508409516)*x_3)
l[0][2]
(0.929251263865+I*-0.00647030572172)*((0.375533564086+I*0.643435017932)*x_0-(0.208465534309+I*0.838096322231)*x_3)+(-0.96149927365+I*0.480429576293)*((0.375533564086+I*0.643435017932)*x_1-(-0.237964947646+I*0.40102539944)*x_3)+(-0.377714814048+I*0.164762291067)*((0.375533564086+I*0.643435017932)*x_2-(0.392192600852+I*-0.319508409516)*x_3)

Using degree linears
(-0.922909581578 + I*0.520281817425)*x_0+(-0.222559515157 + I*0.971260056134)*x_1+(0.441457019179 + I*0.421252304705)*x_2+(0.923740150129 + I*0.663831700427)*x_3
(0.517698381776 + I*-0.735750317496)*x_0+(-0.921836097918 + I*0.0895617802129)*x_1+(-0.358866235243 + I*-0.145384839885)*x_2+(0.0579076672446 + I*0.747067964401)*x_3
('exploring tree in order', 'depthFirst')

################### Starting multiregeneration ####################

PROGRESS
Depth 0: 2
Depth 1: 4
Depth 2: 3

----------------------------------------------------------------
| # smooth isolated solutions  | # of general linear equations |
| found                        | added with variables in group |
----------------------------------------------------------------
                               | 0
----------------------------------------------------------------
  3                              1  
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

The folder `depth_n` contains the data of a witness set collection for 
the system $f_0, \ldots, f_{n-1}$. We see that a witness set for the 
variety $f_1=f_2=0$ consists of four point, which is expected since $f_1 
= f_2 = 0$ describes a cubic curve together with a line. A witness set 
for the twisted cubic $f_1 = f_2 = f_3 = 0$ consists of one less point, 
since the extra line $x_1 = x_2 = 0$ is not included.

Therefore a witness system for the twisted cubic is given by the 
equations $f_1, f_2$, the linear equation `l[0][2]`
```
(0.929251263865+I*-0.00647030572172)*((0.375533564086+I*0.643435017932)*x_0-(0.208465534309+I*0.838096322231)*x_3)+(-0.96149927365+I*0.480429576293)*((0.375533564086+I*0.643435017932)*x_1-(-0.237964947646+I*0.40102539944)*x_3)+(-0.377714814048+I*0.164762291067)*((0.375533564086+I*0.643435017932)*x_2-(0.392192600852+I*-0.319508409516)*x_3)
```
and the following points.
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
