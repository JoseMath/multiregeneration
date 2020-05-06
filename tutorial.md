---
abstract: |
  We introduce the multiregeneration software through the lens of
  solving polynomial systems and numerical algebraic geometry.
bibliography:
- tutorial.bib
title:  Multiregeneration Tutorial
---

Getting Started
===============

Input files
-----------

Say that we are given the following two polynomials in the variables
$x,y$. $$\begin{aligned}
    f_1 &= (x-1)(y-3)\\
    f_2 &= (x-2)(y-4)\end{aligned}$$ By inspection, we see that the set
of solutions consists of two points $\{ (1,4), (2,3)\}$. To solve the
system above using the multiregeneration software, let's change into the
folder "getting-started", which contains the following three files.\
**bertiniInput\_variables**

        variable_group x,y; 

**bertiniInput\_equations**

        function f1,f2;
        f1 = (x-1)*(y-3);
        f2 = (x-2)*(y-4);

**inputFile.py**

        degrees = [[2], [2]]

The first two files (those with the prefix "bertiniInput") are written
in the C-like syntax used by the Bertini software. In the
"bertiniInput\_variables\" file, the unknowns of our system of
polynomials are described as variable groups with one per line. In the
"bertiniInput\_equations\" file, our system of polynomials is described
by a line beginning with \"function\" to set the polynomials whose
common roots we aim to describe followed by one equation per line to
define the polynomials in an expression of the unknowns.

The last file, "inputFile.py", contains the additional data that this
program needs, namely degree information. The variable "degrees" must be
initialized to a list of lists, where the $j$'th element of the $i$'th
list is the degree of the $i$'th function in the $j$th "variable group."
For this example there is only one variable group consisting of $x,y$,
and each function has degree two in this variable group. Therefore we
use the python syntax to create a list of two lists, where the single
element of the first list is the degree of $f_1$ and the single element
of the second list is the degree of $f_2$.

For the expert user there are many Bertini options which can improve
performance. These can be added to the file
"bertiniInput\_trackingOptions", and one can refer to Appendix A of the
Bertini user manual for more details.

Bertini uses "I\" to denote $\sqrt{-1}$. The use of this symbol as a
variable is not allowed. To specify the value of a constant, say $c$ is
$2.2$, put in a single line in the "bertiniInput\_equations\" file "c =
2.2\".

Solving
-------

To solve the system, we use python2 to run the "multiregeneration.py"
script *from the "getting-started" folder*. The multiregeneration script
will look for input files in the directory from which it is run, so make
sure that you are in the directory with the system you wish to solve.

    python2 ../multiregeneration.py

If all goes well there will be a new directory called "run". If there
was an error, then the most likely cause is that there was an error in
one of the input files.

The solutions will be contained in the folder

    run/_completed_smooth_solutions/depth_1

The "depth" refers to how many equations have been solved so far. At
depth $n$ the first $n+1$ equations have been solved, so for this
example we look at depth 1. Later we will say more about why this is,
but for the moment, know that the solutions are always in the folder
corresponding to the last depth. Returning to our example, there are two
files that begin with "solution\_tracking\_\":

    solution_tracking_depth_1_gens_1_1_dim_0_varGroup_0_regenLinear_1
    _pointId_326664877375_788310760051

    solution_tracking_depth_1_gens_1_1_dim_0_varGroup_0_regenLinear_1
    _pointId_918720474422_183602510053 

The two file contain approximate complex values for the two solutions of
the initial system. For example the first file contains the following.

        1.999999999999996e+00 -4.107825191113079e-15
        3.000000000000000e+00 0.000000000000000e+00

The file can be read as $$\begin{aligned}
    x &= 1.999999999999996 \times 10^0 - (4.107825191113079 \times 
    10^{-15})i\\
    y &= 3.000000000000000 \times 10^0 + (0.0000000000000000 \times 
    10^{0})i\\\end{aligned}$$ which is approximately the solution
$(x,y) = (2, 3)$.

Multiple variable groups
========================

Multi-homogeneous Bézout's Theorem
----------------------------------

To motivate the notion of variable groups, we begin by stating the
following formulation of Bézout's Theorem.

Let $f_1, \ldots, f_N$ be polynomials with complex coefficients in $n$
variables, and let $d_1, \ldots, d_N$ denote their degrees. If
$\mathcal{V}(f_1, \ldots, f_N)$ is finite, then its size is at most
$d_1d_2 \ldots d_N$.

For now we will assume that our system has finitely many solutions.
Therefore the degrees $d_1, \ldots, d_n$ give an upper bound on the size
of the output. It is not hard to construct examples where the number of
solutions is exactly this bound, so in the case of general equations of
degrees $d_1, \ldots, d_n$ this worst case bound cannot be improved.

Here is a simple example to illustrate this bound. Consider the system
given by the two quadratic polynomials $$\begin{aligned}
    f_1 &= x^2 + xy + x - y\\
    f_2 &= y^2 + 4xy - 2y.\end{aligned}$$ We can verify as in the
previous section that this system has exactly $d_1d_2 = 4$ solutions.

Let us remove the $x^2$ and $y^2$ terms from the example above, and
consider a system given by the polynomials $$\begin{aligned}
    f_1 &= xy + x - y\\
    f_2 &= 4xy - 2y.\end{aligned}$$ The degrees $d_1$ and $d_2$ have not
changed, so the Bézout bound still predicts four solutions. However,
removing the square terms reduced the number of solutions to two. This
is a consequence of the Multi-homogeneous Bézout Theorem, which we state
below.

Say that for each $1 \leq i \leq k$ we have a group of variables
$\mathbf{x}_i = (x_{i,1}, \ldots, x_{i,n_i})$, for a total of $n := n_1 
+ \ldots + n_k$ variables. Let $f(\mathbf{x}_1, \ldots, 
\mathbf{x}_k)$ denote a polynomial in all $n$ variables. We define the
*multidegree* of $f$ to be the integer vector $\text{Deg}(f) = 
(\text{Deg}_1(f), \ldots, \text{Deg}_k(f))$ where $\text{Deg}_i(f)$ is
the degree of $f$ treating all variables except for $\mathbf{x}_i$ as
constants.

Let $f_1, \ldots, f_N$ be polynomials with complex coefficients in the
variables $\mathbf{x}_1, 
\ldots, \mathbf{x}_n$. Consider the formal expression $\prod_{s = 1}^N 
\sum_{i = 1}^{k} \text{Deg}_i(f_s) \alpha_i$ in indeterminants
$\alpha_1, 
\ldots, \alpha_k$, and let $B$ denote the coefficient of the monomial
$\alpha_1^{n_1}\ldots \alpha_k^{n_k}$. If
$\mathcal{V}(f_1, \ldots, f_N)$ is finite, than its size is at most $B$.

The number $B$ is called the *multi-homogeneous Bézout number*.

Returning to our example, let us define variable groups $\mathbf{x}_1 = 
(x), \mathbf{x}_2 = (y)$. Then $\text{Deg}(f_1) = (1,1)$ and
$\text{Deg}(f_2) = 
(1,1)$. From the expression
$$(\alpha_1 + \alpha_2)(\alpha_1 + \alpha_2) = \alpha_1^2 + 
   2\alpha_1\alpha_2 + \alpha_2^2$$ we see that $B = 2$. So if
$\mathcal{V}(f_1, f_2)$ is finite, its size is at most two. By grouping
the variables we have a better bound on the number of solutions.
Multiregeneration uses algorithms that take advantage of multivariable
group structure to improve performance.

Solving with multiple variable groups
-------------------------------------

When solving a polynomial system, if there is a variable group structure
that gives a low multi-homogeneous Bézout number, then this gives us
better guarantees about the number of solutions we will find. Moreover,
the program can take advantage of this extra structure to do less work.

For an example of how to use variable groups, change into the directory
called "multiple\_variable\_groups", which contains the following
files.\
**bertiniInput\_variables**

        variable_group x; 
        variable_group y; 

**bertiniInput\_equations**

        function f1,f2;
        f1 = x*y + x - y;
        f2 = 4*x*y - 2*y;

**inputFile.py**

        degrees = [[1,1], [1,1]]

The only differences when using multiple variable groups are the
declaration of multiple variable groups in "bertiniInput\_variables" and
the entries of the "degree" variable, which now contains the
multidegrees $\text{Deg}(f_1)$ and $\text{Deg}(f_2)$.

As before we run

    python2 ../multiregeneration.py

and look for the solution files in

    run/_completed_smooth_solutions/depth_1

where we find the two solution files.

Solving with homogeneous variable groups
========================================

In this section we demonstrate how to solve systems of homogeneous
polynomials over complex projective space, which is a central idea in
algebraic geometry. For a good introduction to projective space see
chapter 8 sections 1 and 2 of [@clo], or appendix A of [@st].

Consider the two homogeneous polynomials $$\begin{aligned}
   f_1 &= y^2z - x^3 + z^3 - xyz \\
   f_2 &= yz - x^2 + xy - xz + z^2. \end{aligned}$$ Observe that all
terms in the first equation are degree three, and all term is the second
equations are degree two, so these equations are indeed homogeneous of
degrees two and three. The common roots of these polynomials represent
the intersection of two curves in the projective plane. If you input
equations that are not homogeneous, and then try to solve them over
projective space it will cause errors, so watch out for this.

Change into the directory called "homogeneous-variable-groups", which
contains the following files.\
**bertiniInput\_variables**

       hom_variable_group x,y,z;

**bertiniInput\_equations**

       function f1,f2;
       f1 = y^2*z - x^3 + z^3 - x*y*z;
       f2 = y*z - x^2 + x*y - x*z + z^2;

**inputFile.py**

       degrees = [[3], [2]]

There are two notable differences: (1) our equations are homogeneous,
and (2) we have declared a "hom\_variable\_group".

After running the program

    python2 ../multiregeneration.py

the output in

    run/_completed_smooth_solutions/depth_1

will be give the homogeneous coordinates of the six solutions. Often,
these coordinates are scaled so that the max norm of its entries is one.

One can also better performance by having multiple homogeneous groups or
a mixture of homogeneous and affine groups.

Positive dimensional components
===============================

In this section we will introduce some of the language of algebraic
geometry and numerical algebraic geometry, so that we can describe how
the program handles the case where the solution set is infinite (i.e.
that it contains positive dimensional components).

Recall that a set $A \subset \mathbb{C}^n$ is *algebraic* or *Zariski
closed* if it is of the form $\mathcal{V}(f_1, \ldots, f_N)$ for
polynomials $f_i$. Similarly, a set $A \subset \mathbb{P}^n$ is
*algebraic* or *Zariski closed* if it is of the form
$\mathcal{V}(f_1, \ldots, f_N)$ for homogeneous polynomials $f_i$. If an
algebraic set is the union of finitly many algebraic proper subsets, the
it is *reducible*. An algebraic set that is not reducible is
*irreducible*. If $A$ is an algebraic set, then a maximal irreducible
algebraic subset of $A$ is called an *irreducible component of $A$*, or
simply a *component of $A$*.

The following fact is typically proven in a first commutative algebra or
algebraic geometry course.

Every algebraic set in $\mathbb{C}^n$ or $\mathbb{P}^n$ is the union of
finitely many irreducible components.

In the case where a polynomial system has infinitely many solutions, it
is often best to describe each component separately. As a simple
example, consider the system given by $$\begin{aligned}
   f_1 &= (y-x^2)(x-1) \\
   f_2 &= (y-x^2)(y).\end{aligned}$$

The solutions consist of a parabola and a point, which are the two
irreducible components. This system can be found in the
"positive-dimensional" folder. The following files contain the
solutions.

          solution_tracking_depth_1_gens_1_1_dim_0_varGroup_0_regenLinear_
          1_pointId_151979748598_138051236175

          solution_vanishing_depth_1_gens_1_0_dim_1_pointId_11020904120_
          11020904120

          solution_vanishing_depth_1_gens_1_0_dim_1_pointId_462642055403_
          462642055403

The coordinates of the isolated point are contained in the files whose
name contains the string "dim\_0". The other two files, whose names
contain the string "dim\_1" are two points on the one dimensional
parabola, which is the other irreducible component. Which two points of
the parabola were chosen, and why? To answer this question, we introduce
some language from numerical algebraic geometry [@BertiniBook; @SWBook].

By a *hyperplane in $\mathbb{C}^n$*, we mean a variety of the form
$\mathcal{V}(a_0 + a_1x_1 + \ldots + a_nx_n)$ where one of
$a_1, \ldots, 
a_n$ is not zero. By a *hyperplane in $\mathbb{P}^n$* we mean a variety
of the form $\mathcal{V}(a_0x_0 + a_1x_1 
+ \ldots + a_nx_n)$ where one of $a_0, \ldots, a_n$ is not zero.
Intuitively, a *general hyperplane* is a hyperplane where the parameters
$a_i$ are chosen at random, and satisfy no special relations. The
program chooses "generic hyperplanes" by picking coefficients the
coefficients $a_i$ to be uniform random complex numbers with real and
imaginary parts in $(-1, 1)$. If coefficients are chosen randomly in
this way, then it is a fact that anything true of a "generic hyperplane"
will be true of a random hyperplane with probability one. For those
familiar with projective geometry who would like a more rigourous
definition of generic, see [@SWBook].

The following fact is often proved with the use of more powerful
theorems such as Bertini's theorem and Bezout's theorem, but we want to
get down to business, so we will take it for granted.

Let $X$ be an irreducible algebraic variety in $\mathbb{C}^n$ or
$\mathbb{P}^n$. Then there is unique number $d$ such that the
intersection of $X$ with $d$ generic hyperplanes is finite and nonempty.
Moreover, the size of the intersection does not depend on the choice of
generic hyperplanes.

The number $d$ we define to be the *dimension of $X$*, and the number
size of the intersection is the *degree of $X$*. [^1]

Returning to the example above, the two points on the parabola which
were outputed were the intersection of the parabola with one generic
hyperplane. As we would expect, the fact that there are two of them
means that the parabola has degree two. One of the main ideas in
numerical algebraic geometry is that many questions about a $d$
dimensional irreducible variety in $\mathbb{C}^n$ or $\mathbb{P}^n$ can
be answered by knowing the its intersection with $d$ generic
hyperplanes. This intersection is called a *witness set for $X$*.

Tips for large computations
===========================

One of the main advantages of numerical methods for solving polynomial
systems (over Gröbner basis methods for instance) is that they are very
parallelizable. To use multiple processors to solve a system, we can set
the "maxProcesses" variable in "inputFile.py".

**inputFile.py**

       degrees = [[3], [2]]
       maxProcesses = 4

Adding more processes will only speed up the calculation if the number
you choose is less than or equal to the number of CPU cores on your
computer, and in fact adding more processes than you have cores will
slow things down.

If you do not have enough time or space to find all of the solution to a
particular system, then it can sometimes still be worth it to find as
many solutions as you can. If this is the case, the it is recommended to
use the following option in "inputFile.py" **inputFile.py**

       degrees = [[3], [2]]
       explorationOrder = "depthFirst"

Setting this option will not decrease the time it takes for the program
to finish, however it will increase the number of solutions found after
any given time. Here is a vague explanation as to why: The nature of the
algorithm is that "solutions at depth $n$" lead to "solutions at depth
$n+1$." The solutions at the last depth are the actual solutions to the
system. In this way, the program first populates one depth with
solutions, and then moves to the next. Setting the exploration order to
"depthFirst" will ensure that if a solution is found at depth $n$, then
it is immediately used to find a solution at depth $n+1$, before looking
for other solutions at depth $n$. The result is that the maximum number
full depth solutions are found after any given time.

In the directory "large" there is a system of 10 polynomials, all of
degree $(1,1)$ with respect to variable groups $x_0, \ldots, x_4$ and
$y_0, \ldots, y_4$. This computation should take on the order of 30
seconds, so you can experiment with parallel processing, depth first
order, and using multiple variable groups versus a single variable
group.

[^1]: For those farmiliar with algebraic geometry, the degree of a
    variety in $\mathbb{C}^n$ or $\mathbb{P}^n$ is not an isomorphism
    invariant, since it depends on the embedding.
