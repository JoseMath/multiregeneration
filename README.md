Bertini version of multiregeneration with regeneration graphs
=============================================================

Purpose
-------

This script has two main purposes: to implement multihomogenious 
regeneration as described [here](https://www3.nd.edu/~jhauenst/preprints/hrMultiHom.pdf), and to implement a "Depth First" 
version of regeneration as described [here](https://arxiv.org/abs/1912.04394).

Our implementation is written in python, and uses Bertini to track 
individual paths.

Bertini is a general-purpose solver, written in C, that was created by
Daniel J. Bates, Jonathan D. Hauenstein, Andrew J. Sommese, and Charles W. Wampler
 for research about polynomial continuation. For more information see
https://bertini.nd.edu/

Example
-------

For a more complete description on how to use this software, see the tutorial [here](https://github.com/colinwcrowley/multiregeneration-tutorial).

Say that we are given the following two polynomials in the variables
$x,y$. $$\begin{aligned}
    f_1 &= (x-1)(y-3)\\
    f_2 &= (x-2)(y-4)\end{aligned}$$ By inspection, we see that the set
of solutions consists of two points $\{ (1,4), (2,3)\}$. To solve the
system above using the multiregeneration software, let's change into the
folder "getting-started", which contains the following three files.\

Input format
------------

A complete input for our software consists of three files named 
`inputFile.py`, `bertiniInput_variables`, and `bertiniInput_equations` 
in the same directory.

 - The file `inputFile.py` is written in python. The python script 
   `multiregeneration.py` needs to know the multidegrees of the 
   equations to solve, which should be defined in `inputFile.py`. See, 
   for example, `Tests/Example-p10a`.

 - The file `bertiniInput_equations` should contain the declaration of 
   several functions, and the definition of those functions, in the same 
   syntax that is used to define functions in Bertini.

 - The file `bertiniInput_variables` should contain the declaration of 
   several variable group in the same 
   syntax that is used to define them in Bertini. Our script works with 
   either affine or projective variable groups.

In addition, the user can include a file `bertiniInput_trackingOptions`, 
which will be passed to Bertini when it tracks each path.
