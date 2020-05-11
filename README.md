Multiregeneration with regeneration graphs
=============================================================

This script implements the algorithm described in the paper 
[Regeneration graphs for polynomial system 
solving](https://arxiv.org/abs/1912.04394), which finds all smooth and 
isolated complex solutions to a square system of polynomial equations. 

A tutorial on how to use this software can be found [here](https://github.com/colinwcrowley/multiregeneration-tutorial).

Our implementation has two main purposes: 

 - The first purpose is to implement a multihomogenious regeneration 
   algorithm as described [here](https://www3.nd.edu/~jhauenst/preprints/hrMultiHom.pdf). 

 - The second purpose is to implement a "Depth First" version of 
   regeneration, which is novel in our approach.

Our implementation is written in python, and uses Bertini to track 
individual paths.

Bertini is a general-purpose solver, written in C, that was created by
Daniel J. Bates, Jonathan D. Hauenstein, Andrew J. Sommese, and Charles W. Wampler
 for research about polynomial continuation. For more information see
https://bertini.nd.edu/.

Running examples
----------------

Here we include an example of how to run our implementation on the 
examples and test that are included in this repository.

After cloning this repository, change into the directory 
`CyclicRoots`. Included in this directory are the following four 
files:`inputFile.py`, `bertiniInput_variables`, `bertiniInput_equations`,
and `bertiniInput_trackingOptions`.

 - The file `inputFile.py` is written in python. The python script 
   `multiregeneration.py` needs to know the multidegrees of the 
   equations to solve, which should be defined in `inputFile.py`. For 
   this example, each equation has multidegree `(1,1,1,1,1)`. 
   Our implementation supports multiple processes, and the number of 
   processes used can be specified via the variable `maxProcesses`.
   The variable `verbose`, which can be set to one to 
   produce a progress update graphic, and set to zero to prevent 
   anything from printing.

 - The file `bertiniInput_equations` should contain the declaration of 
   several functions, and the definition of those functions, in the same 
   syntax that is used to define functions in Bertini.

 - The file `bertiniInput_variables` should contain the declaration of 
   several variable group in the same 
   syntax that is used to define them in Bertini. Our script works with 
   either affine or projective variable groups. In this example, each 
   variable is its own group.

 - The file `bertiniInput_trackingOptions` need not be included, 
   and contains options which will be passed to Bertini when it tracks 
   each path.

Now run the python script `multiregeneration.py` using python2 from the 
directory `CyclicRoots`.

```bash
python2 ../multiregeneration.py
```

Note that our script only works with python version 2, so make sure that 
use use that and not a different version of python.

You will see the followint output
```
################### Setup multiregeneration ####################

These variable groups have been selected:
variable_group x0;
variable_group x1;
variable_group x2;
variable_group x3;
variable_group x4;

Solutions in a 'linearProduct' directory and :
depth >= 0 satisfy f0 = 0
depth >= 1 satisfy f1 = 0
depth >= 2 satisfy f2 = 0
depth >= 3 satisfy f3 = 0
depth >= 4 satisfy f4 = 0

Using start solution
0.175979100512 0.0825147051053
-0.5435463831 -0.230414218757
-0.00197023304276 -0.453423608565
0.123956054991 0.318785398772
0.348452718562 0.565381663207

Using dimension linears
l[0][0]
(-0.0999627977332+I*0.849388083618)*(x0-(0.175979100512+I*0.0825147051053))
l[1][0]
(-0.241672517105+I*0.0596239238783)*(x1-(-0.5435463831+I*-0.230414218757))
l[2][0]
(-0.847001857551+I*0.860355744611)*(x2-(-0.00197023304276+I*-0.453423608565))
l[3][0]
(0.3380664192+I*0.781912837974)*(x3-(0.123956054991+I*0.318785398772))
l[4][0]
(-0.773638560574+I*-0.870334688591)*(x4-(0.348452718562+I*0.565381663207))

Using degree linears
(-0.731921310143 + I*0.257198955602)*x0+(-0.998773532849 + I*-0.420511605004)
(0.071867153673 + I*-0.0700419949032)*x1+(-0.109716126039 + I*-0.70848225598)
(-0.152686515584 + I*-0.434657524026)*x2+(0.0706917737894 + I*-0.290226307158)
(-0.353225306789 + I*0.324872307361)*x3+(-0.0104252166896 + I*0.826363723515)
(0.0513386900364 + I*-0.292984355599)*x4+(-0.474476845325 + I*-0.194325610374)
('exploring tree in order', 'depthFirst')

################### Starting multiregeneration ####################

PROGRESS
Depth 0: 5
Depth 1: 15
Depth 2: 45
Depth 3: 90
Depth 4: 70

----------------------------------------------------------------
| # smooth isolated solutions  | # of general linear equations |
| found                        | added with variables in group |
----------------------------------------------------------------
                               | 0  1  2  3  4
----------------------------------------------------------------
  70                             0  0  0  0  0
Done.
```
The table at the bottom of the output indicates how many smooth isolated 
solutions are found on components of each multidegree, that is, how many 
solutions are there after adding random linear equations with variables 
in certain groups. In this example there are zero random linear 
equations added, so each solution that is found is a solution to the 
original system.

The default is to explore the tree in a "depth first" fashion as describe 
in section 4 of [our paper](https://arxiv.org/abs/1912.04394), so 
solutions to the entire system will begin to appear before each 
regeneration level has finished.

As soon as you run the script, there will appear a folder called `run`, 
and the solutions at each regeneration level can be found in 
`run/_completed_smooth_solutions`. Therefore the solutions to the system 
in this example can be found in `run/_completed_smooth_solutions/depth_4`.


