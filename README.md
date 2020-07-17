Multiregeneration with regeneration graphs
=============================================================

This script implements the algorithm described in the paper 
[Multiregeneration for polynomial system 
solving](https://arxiv.org/abs/1912.04394), which finds all smooth and 
isolated complex solutions to a square system of polynomial equations. 

A tutorial on how to use this software can be found [here](https://github.com/colinwcrowley/multiregeneration-tutorial).

Our implementation has two main purposes: 

 - The first purpose is to implement a multihomogeneous regeneration 
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
`CyclicRoots`. This directory contains the n=5 case of the Cyclic 
n-Roots problem, which is a common benchmark in computer algebra. (See 
e.g. [here](https://homepages.math.uic.edu/~adrovic/jmm13a.pdf).)

Included in this directory are the following four 
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

Solutions are found in run/_completed_smooth_solutions and:
depth >= 0 satisfy f0 = 0
depth >= 1 satisfy f1 = 0
depth >= 2 satisfy f2 = 0
depth >= 3 satisfy f3 = 0
depth >= 4 satisfy f4 = 0

Exploring tree in order depthFirst

################### Starting multiregeneration ####################

PROGRESS
Depth 0: 5
Depth 1: 15
Depth 2: 45
Depth 3: 70
Depth 4: 70

------------------------------------------------------------------
| # of smooth isolated solutions | # of general linear equations |
| found                          | added with variables in group |
------------------------------------------------------------------
                                 | 0  1  2  3  4
----------------------------------------------------------------
  70                               0  0  0  0  0
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

 - Examples of computing witness sets: [here](https://josemath.github.io/multiregeneration/example-pages/HR-example-4-12/HR-example-4-12.html) and also [here](https://josemath.github.io/multiregeneration/example-pages/example-1-3/example-1-3.html).
   
 - [A witness set for a noncomplete intersection](https://josemath.github.io/multiregeneration/example-pages/twisted-cubic/twisted-cubic.html)

 - Excluding solutions with zero coordinates: [here](https://josemath.github.io/multiregeneration/example-pages/nonzero-coordinates/nonzero-coordinates.html) and also [here.](https://josemath.github.io/multiregeneration/example-pages/algebraic-torus-variable-groups/algebraic-torus-variable-groups.html)
 
 - [Saturating by an equation](https://josemath.github.io/multiregeneration/example-pages/prune-by-point/prune-by-point.html)
 
 - [Computing multidegree coefficients in only certain dimensions](https://josemath.github.io/multiregeneration/example-pages/target-dimensions/target-dimensions.html)

 - [An application to deep linear networks](https://josemath.github.io/multiregeneration/example-pages/deep-linear-networks/deep-linear-networks.html)

 - [Computing Nash equilibria](https://josemath.github.io/multiregeneration/example-pages/nash-equilibria/nash-equilibria.html)

 - [Depth first for real solutions](https://josemath.github.io/multiregeneration/depth-first-real/depth-first-real.html)

Contributing an example page
----------------------------

The example pages are written in the easy to learn markup language
[Markdown](https://www.markdownguide.org/basic-syntax), and then 
converted into html via [Pandoc](https://pandoc.org/). 

To create your own example page, follow these seven steps. 
The first three steps involve Markdown and you can take a look at the ``.md`` files in the other examples to get a better idea of how it works.
If you get stuck at steps 4-6, then feel free to jump to step 7. Afterwhich, we can try to help.

  1. [Fork](https://docs.github.com/en/enterprise/2.13/user/articles/fork-a-repo) this repository.
  2. Create a new folder in the directory `example-pages`.
  ```bash
  $ cd example-pages/
  $ mkdir our-new-example
  ```

  3. Create a markdown file in the new directory, and copy the 
     `modest.css` (we welcome other stylesheet choices as well) to this directory.
  ```
  $ cp twisted-cubic/modest.css our-new-example
  $ cd our-new-example
  $ vim our-new-example.md #Open a new file with your favorite editor.
  ```

  4. In the `.md` file you created, add the following text to get started. 
  The first few lines before `## Our new example` will style this page 
  to look like the others.

  ```markdown
  <link rel="stylesheet" href="modest.css">
  <style>
  pre, code, pre code {
    max-height: 400px;
  }
  </style>

  ## Our new example

  #### Authors: Your name

  We demonstrate how to solve the following neat polynomial system...

  Here is an example of using latex syntax $$e^{2 \pi i} = 1$$.
  ```
  
  5. Download and install [Pandoc](https://pandoc.org/). Then use pandoc 
     to convert the `.md` file into a `.html` file.
    ```bash
    $ pandoc our-new-example.md -s --mathjax -o our-new-example.html
    ```
    To read more about Pandoc, see the demos page (in particular example 17) [here](https://pandoc.org/demos.html).
  6. Once you see a file named `our-new-example.html`, you can open it 
     in your web browser to check how the page looks. You can now continue to edit 
     the `.md` file, and when you are done, convert it to html using 
     Pandoc.
  7. Once you are happy with the example page, commit your changes, and 
     send us a pull request.
