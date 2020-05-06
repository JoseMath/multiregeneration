Multiregeneration with regeneration graphs
=============================================================

This script implements the algorithm described in the paper 
[Regeneration graphs for polynomial system 
solving](https://arxiv.org/abs/1912.04394), which finds all smooth and 
isolated complex solutions to a square system of polynomial equations. 

A tutorial on how to use this software can be found here [here](https://github.com/colinwcrowley/multiregeneration-tutorial).

Our implementaion has two main purposes: 

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


<!-- Input format -->
<!-- ------------ -->

<!-- A complete input for our software consists of three files named --> 
<!-- `inputFile.py`, `bertiniInput_variables`, and `bertiniInput_equations` --> 
<!-- in the same directory. -->

<!--  - The file `inputFile.py` is written in python. The python script --> 
<!--    `multiregeneration.py` needs to know the multidegrees of the --> 
<!--    equations to solve, which should be defined in `inputFile.py`. See, --> 
<!--    for example, `Tests/Example-p10a`. -->

<!--  - The file `bertiniInput_equations` should contain the declaration of --> 
<!--    several functions, and the definition of those functions, in the same --> 
<!--    syntax that is used to define functions in Bertini. -->

<!--  - The file `bertiniInput_variables` should contain the declaration of --> 
<!--    several variable group in the same --> 
<!--    syntax that is used to define them in Bertini. Our script works with --> 
<!--    either affine or projective variable groups. -->

<!-- In addition, the user can include a file `bertiniInput_trackingOptions`, --> 
<!-- which will be passed to Bertini when it tracks each path. -->
