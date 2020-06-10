Multiregeneration with regeneration graphs
=============================================================

This script implements the algorithm described in the paper 
[Multiregeneration for polynomial system 
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

Running an example
------------------

Here we include an example of how to run our implementation on the 
examples and tests that are included in this repository.

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

Now run the python script `multiregeneration.py` using python (version 2 
or 3) from the 
directory `CyclicRoots`.

```bash
python ../multiregeneration.py
```

You will see the following output
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
exploring tree in order depthFirst

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
[here](https://arxiv.org/abs/1912.04394), so 
solutions to the entire system will begin to appear before each 
regeneration level has finished.

As soon as you run the script, there will appear a folder called `run`, 
and the solutions at each regeneration level can be found in 
`run/_completed_smooth_solutions`. Therefore the solutions to the system 
in this example can be found in `run/_completed_smooth_solutions/depth_4`.

Example pages
-----------------
Here are several pages which demonstrate features and applications.

 - Examples of computing witness sets: [here](https://colinwcrowley.github.io/multiregeneration-tutorial/example-pages/HR-example-4-12/HR-example-4-12.html) and also [here](https://colinwcrowley.github.io/multiregeneration-tutorial/example-pages/example-1-3/example-1-3.html).
   
 - [A witness set for a noncomplete intersection](https://colinwcrowley.github.io/multiregeneration-tutorial/example-pages/twisted-cubic/twisted-cubic.html)

 - Excluding solutions with zero coordinates: [here](https://colinwcrowley.github.io/multiregeneration-tutorial/example-pages/nonzero-coordinates/nonzero-coordinates.html) and also [here.](https://colinwcrowley.github.io/multiregeneration-tutorial/example-pages/algebraic-torus-variable-groups/algebraic-torus-variable-groups.html)
 
 - [Satruating by an equation](https://colinwcrowley.github.io/multiregeneration-tutorial/example-pages/prune-by-point/prune-by-point.html)
 
 - [Computing multidegree coefficients in only certain dimensions](https://colinwcrowley.github.io/multiregeneration-tutorial/example-pages/target-dimensions/target-dimensions.html)

 - [An application to deep linear networks](https://colinwcrowley.github.io/multiregeneration-tutorial/example-pages/deep-linear-networks/deep-linear-networks.html)

 - [Computing Nash equilibria](https://colinwcrowley.github.io/multiregeneration-tutorial/example-pages/nash-equilibria/nash-equilibria.html)
