Multiregeneration with regeneration graphs
=============================================================

Purpose
=======

This script has two main purposes: to implement multihomogenious 
regeneration as described [here](https://www3.nd.edu/~jhauenst/preprints/hrMultiHom.pdf), and to implement a "Depth First" 
version of regeneration as described [here](https://arxiv.org/abs/1912.04394).

Our implementation is written in python, and uses Bertini to track 
individual paths.

Bertini is a general-purpose solver, written in C, that was created by
Daniel J. Bates, Jonathan D. Hauenstein, Andrew J. Sommese, and Charles W. Wampler
 for research about polynomial continuation. For more information see
https://bertini.nd.edu/

Getting Started
===============

Input files
-----------

Say that we are given the following two polynomials in the variables
<img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/0acac2a2d5d05a8394e21a70a71041b4.svg?invert_in_darkmode" align=middle width=25.350096749999988pt height=14.15524440000002pt/>. <p align="center"><img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/a8546fc93b1c9e52664a8bdf30f5ee4e.svg?invert_in_darkmode" align=middle width=137.57593905pt height=41.09589pt/></p> By inspection, we see that the set
of solutions consists of two points <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/7c7e75ec4386aa242a1d739aef7ce8be.svg?invert_in_darkmode" align=middle width=96.80377244999998pt height=24.65753399999998pt/>. To solve the
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
polynomials are described as variable groups with one per line. In
the"bertiniInput\_equations\" file, our system of polynomials is
described by a line beginning with \"function\" to set the polynomials
whose common roots we aim to describe followed by one equation per line
to define the polynomials in an expression of the unknowns.

The last file, "inputFile.py", contains the additional data that this
program needs, namely degree information. The variable "degrees" must be
initialized to a list of lists, where the <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/36b5afebdba34564d884d347484ac0c7.svg?invert_in_darkmode" align=middle width=7.710416999999989pt height=21.68300969999999pt/>'th element of the <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/77a3b857d53fb44e33b53e4c8b68351a.svg?invert_in_darkmode" align=middle width=5.663225699999989pt height=21.68300969999999pt/>'th
list is the degree of the <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/77a3b857d53fb44e33b53e4c8b68351a.svg?invert_in_darkmode" align=middle width=5.663225699999989pt height=21.68300969999999pt/>'th function in the <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/36b5afebdba34564d884d347484ac0c7.svg?invert_in_darkmode" align=middle width=7.710416999999989pt height=21.68300969999999pt/>th "variable group."
For this example there is only one variable group consisting of <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/0acac2a2d5d05a8394e21a70a71041b4.svg?invert_in_darkmode" align=middle width=25.350096749999988pt height=14.15524440000002pt/>,
and each function has degree two in this variable group. Therefore we
use the python syntax to create a list of two lists, where the single
element of the first list is the degree of <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/5872d29d239f95cc7a5f43cfdd14fdae.svg?invert_in_darkmode" align=middle width=14.60053319999999pt height=22.831056599999986pt/> and the single element
of the second list is the degree of <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/f6366b38f9364f745b5400c328e938d3.svg?invert_in_darkmode" align=middle width=14.60053319999999pt height=22.831056599999986pt/>.

For the expert user there are many Bertini options which can improve
performance. These can be added to the file
"bertiniInput\_trackingOptions", and one can refer to Appendix A of the
Bertini user manual for more details.

Bertini uses "I\" to denote <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/a753db8bcd2d8599b554045e8852f53c.svg?invert_in_darkmode" align=middle width=34.70331479999999pt height=27.14148359999999pt/>. The use of this symbol as a
variable is not allowed. To specify the value of a constant, say <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/3e18a4a28fdee1744e5e3f79d13b9ff6.svg?invert_in_darkmode" align=middle width=7.11380504999999pt height=14.15524440000002pt/> is
<img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/783bf12b35ef49c9c5622d4d6cd6cb2c.svg?invert_in_darkmode" align=middle width=21.00464354999999pt height=21.18721440000001pt/>, put in a single line in the"bertiniInput\_equations\" file \"c =
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
depth <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/55a049b8f161ae7cfeb0197d75aff967.svg?invert_in_darkmode" align=middle width=9.86687624999999pt height=14.15524440000002pt/> the first <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/3f18d8f60c110e865571bba5ba67dcc6.svg?invert_in_darkmode" align=middle width=38.17727759999999pt height=21.18721440000001pt/> equations have been solved, so for this
example we look at depth 1. Later we will say more about why this is,
but for the moment, know that the solutions are always in the folder
corresponding to the last depth. Returning to our example, there are two
files that begin with \"solution\_tracking\_\":

    solution_tracking_depth_1_gens_1_1_dim_0_varGroup_0_regenLinear_1
    _pointId_326664877375_788310760051

    solution_tracking_depth_1_gens_1_1_dim_0_varGroup_0_regenLinear_1
    _pointId_918720474422_183602510053 

The two file contain approximate complex values for the two solutions of
the initial system. For example the first file contains the following.

        1.999999999999996e+00 -4.107825191113079e-15
        3.000000000000000e+00 0.000000000000000e+00

The file can be read as <p align="center"><img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/af751d5a3b6112fb019da16f167275f9.svg?invert_in_darkmode" align=middle width=446.63427764999994pt height=45.0083832pt/></p> which is approximately the solution
<img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/47b80a618b130bf5f48b356048ba79e6.svg?invert_in_darkmode" align=middle width=96.58287704999998pt height=24.65753399999998pt/>.

Multiple variable groups
========================

Multi-homogeneous Bézout's Theorem
----------------------------------

To motivate the notion of variable groups, we begin by stating the
following formulation of Bézout's Theorem.

Let <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/cd0dbc1dbf6b80466712fc8698e882a2.svg?invert_in_darkmode" align=middle width=71.64601124999999pt height=22.831056599999986pt/> be polynomials with complex coefficients in <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/55a049b8f161ae7cfeb0197d75aff967.svg?invert_in_darkmode" align=middle width=9.86687624999999pt height=14.15524440000002pt/>
variables, and let <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/6a3e4b17560c15d926c4aa03ab53fcd1.svg?invert_in_darkmode" align=middle width=72.66196409999998pt height=22.831056599999986pt/> denote their degrees. If
<img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/b681649ca92452570df58d02400620d7.svg?invert_in_darkmode" align=middle width=96.67806719999999pt height=24.65753399999998pt/> is finite, then its size is at most
<img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/61d49f1f9651f19f0d07d2bbc3e57459.svg?invert_in_darkmode" align=middle width=76.72028099999999pt height=22.831056599999986pt/>.

For now we will assume that our system has finitely many solutions.
Therefore the degrees <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/bc5965d673c6b387f9096b3dc608e7bb.svg?invert_in_darkmode" align=middle width=69.14182604999998pt height=22.831056599999986pt/> give an upper bound on the size
of the output. It is not hard to construct examples where the number of
solutions is exactly this bound, so in the case of general equations of
degrees <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/bc5965d673c6b387f9096b3dc608e7bb.svg?invert_in_darkmode" align=middle width=69.14182604999998pt height=22.831056599999986pt/> this worst case bound cannot be improved.

Here is a simple example to illustrate this bound. Consider the system
given by the two quadratic polynomials <p align="center"><img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/940204230129b6b0df5ec9dc289f9356.svg?invert_in_darkmode" align=middle width=150.4715058pt height=44.095144499999996pt/></p> We can verify as in the
previous section that this system has exactly <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/db40869e34f6cdd00852404f7b7231ae.svg?invert_in_darkmode" align=middle width=61.99768739999999pt height=22.831056599999986pt/> solutions.

Let us remove the <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/6177db6fc70d94fdb9dbe1907695fce6.svg?invert_in_darkmode" align=middle width=15.94753544999999pt height=26.76175259999998pt/> and <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/78c9c8b66beb94081ec0e836309fe394.svg?invert_in_darkmode" align=middle width=15.201753599999991pt height=26.76175259999998pt/> terms from the example above, and
consider a system given by the polynomials <p align="center"><img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/972e2afbe6ff738a776d9c114f33712a.svg?invert_in_darkmode" align=middle width=113.61086714999999pt height=39.2694126pt/></p> The degrees <img src="https://rawgit.com/JoseMath/multiregeneration/master/svgs/90085a0c43d72e4deebf6ed4a8d9e014.svg?invert_in_darkmode" align=middle width=15.10851044999999pt height=22.831056599999986pt/> and <img src="https://rawgit.com/JoseMath/multiregeneration/master/svgs/25eda7b7741f869a00061a631b356db9.svg?invert_in_darkmode" align=middle width=15.10851044999999pt height=22.831056599999986pt/> have not
changed, so the Bézout bound still predicts four solutions. However,
removing the square terms reduced the number of solutions to two. This
is a consequence of the Multi-homogeneous Bézout Theorem, which we state
below.

Say that for each <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/1ce2fb578a72066c5c8124421dd55874.svg?invert_in_darkmode" align=middle width=66.79306589999999pt height=22.831056599999986pt/> we have a group of variables
<img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/c9aecbb3d9054e7a3051abda5d853d50.svg?invert_in_darkmode" align=middle width=144.11216159999998pt height=24.65753399999998pt/>, for a total of
<img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/a85fa5fca807f70fddaea96d1bf5ffb4.svg?invert_in_darkmode" align=middle width=130.08534659999998pt height=19.1781018pt/> variables. Let
<img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/b15282228bdd581d099d7400dab13d7b.svg?invert_in_darkmode" align=middle width=94.5488973pt height=24.65753399999998pt/> denote a polynomial in all <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/55a049b8f161ae7cfeb0197d75aff967.svg?invert_in_darkmode" align=middle width=9.86687624999999pt height=14.15524440000002pt/>
variables. We define the *multidegree* of <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/190083ef7a1625fbc75f243cffb9c96d.svg?invert_in_darkmode" align=middle width=9.81741584999999pt height=22.831056599999986pt/> to be the integer vector
<img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/3e039e77f400c61dcaad1bb5756d3d54.svg?invert_in_darkmode" align=middle width=238.7501226pt height=24.65753399999998pt/> where
<img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/649a2ebc5b1e95686eb3a3072ad85959.svg?invert_in_darkmode" align=middle width=56.15787704999999pt height=24.65753399999998pt/> is the degree of <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/190083ef7a1625fbc75f243cffb9c96d.svg?invert_in_darkmode" align=middle width=9.81741584999999pt height=22.831056599999986pt/> treating all variables except for
<img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/c416d0c6d8ab37f889334e2d1a9863c3.svg?invert_in_darkmode" align=middle width=14.628015599999989pt height=14.611878600000017pt/> as constants.

Let <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/cd0dbc1dbf6b80466712fc8698e882a2.svg?invert_in_darkmode" align=middle width=71.64601124999999pt height=22.831056599999986pt/> be polynomials with complex coefficients in the
variables <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/e6c8d3482b3a50dbb3fd4d2739e9b446.svg?invert_in_darkmode" align=middle width=71.9841309pt height=14.611878600000017pt/>. Consider the formal
expression <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/735d801595720a3295074cfe1a8d9c65.svg?invert_in_darkmode" align=middle width=160.72431374999996pt height=32.51169900000002pt/>
in indeterminants <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/3445997631efceda377433cd8f11951e.svg?invert_in_darkmode" align=middle width=72.20119829999999pt height=14.15524440000002pt/>, and let <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/61e84f854bc6258d4108d08d4c4a0852.svg?invert_in_darkmode" align=middle width=13.29340979999999pt height=22.465723500000017pt/> denote the
coefficient of the monomial <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/5d34898f3aa652bee4674a562f725c26.svg?invert_in_darkmode" align=middle width=75.66410444999998pt height=24.721402200000004pt/>. If
<img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/b681649ca92452570df58d02400620d7.svg?invert_in_darkmode" align=middle width=96.67806719999999pt height=24.65753399999998pt/> is finite, than its size is at most <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/61e84f854bc6258d4108d08d4c4a0852.svg?invert_in_darkmode" align=middle width=13.29340979999999pt height=22.465723500000017pt/>.

The number <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/61e84f854bc6258d4108d08d4c4a0852.svg?invert_in_darkmode" align=middle width=13.29340979999999pt height=22.465723500000017pt/> is called the *multi-homogeneous Bézout number*.

Returning to our example, let us define variable groups
<img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/c7e5ded4c508466e0f705e68cfe6fff9.svg?invert_in_darkmode" align=middle width=129.45935639999996pt height=24.65753399999998pt/>. Then <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/11b9500afd6bdbcb2309018f86069a41.svg?invert_in_darkmode" align=middle width=114.73748054999999pt height=24.65753399999998pt/>
and <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/d6e4908b3a91db100e2ddd4b42632fd2.svg?invert_in_darkmode" align=middle width=114.73748054999999pt height=24.65753399999998pt/>. From the expression
<p align="center"><img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/4c1c9096d3b2050c4addceb60928ce47.svg?invert_in_darkmode" align=middle width=278.49311324999996pt height=18.312383099999998pt/></p> we see that <img src="https://rawgit.com/JoseMath/multiregeneration/master/svgs/ba2666287058f70b75413ec2a3158822.svg?invert_in_darkmode" align=middle width=43.43024399999999pt height=22.465723500000017pt/>. So if
<img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/8701f762347d1b4b5816867f4bfe6415.svg?invert_in_darkmode" align=middle width=62.36094149999999pt height=24.65753399999998pt/> is finite, its size is at most two. By grouping
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
multidegrees <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/8b0b8d1d2c1311608d3199b51ab43a5c.svg?invert_in_darkmode" align=middle width=56.290114649999985pt height=24.65753399999998pt/> and <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/31789fdf30d096c13369898cf1727ea8.svg?invert_in_darkmode" align=middle width=56.290114649999985pt height=24.65753399999998pt/>.

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

Consider the two homogeneous polynomials <p align="center"><img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/eb450da52163e9339b7827aa83a08023.svg?invert_in_darkmode" align=middle width=207.60621915pt height=44.095144499999996pt/></p> Observe that all
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

Recall that a set <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/06bae592415119199e06adc37111ae5e.svg?invert_in_darkmode" align=middle width=54.244631099999985pt height=22.648391699999998pt/> is *algebraic* or *Zariski
closed* if it is of the form <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/b681649ca92452570df58d02400620d7.svg?invert_in_darkmode" align=middle width=96.67806719999999pt height=24.65753399999998pt/> for
polynomials <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/9b6dbadab1b122f6d297345e9d3b8dd7.svg?invert_in_darkmode" align=middle width=12.69888674999999pt height=22.831056599999986pt/>. Similarly, a set <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/bcacf8f00348d64dce7d814cc1af184a.svg?invert_in_darkmode" align=middle width=52.418138849999984pt height=22.648391699999998pt/> is
*algebraic* or *Zariski closed* if it is of the form
<img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/b681649ca92452570df58d02400620d7.svg?invert_in_darkmode" align=middle width=96.67806719999999pt height=24.65753399999998pt/> for homogeneous polynomials <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/9b6dbadab1b122f6d297345e9d3b8dd7.svg?invert_in_darkmode" align=middle width=12.69888674999999pt height=22.831056599999986pt/>. If an
algebraic set is the union of finitly many algebraic proper subsets, the
it is *reducible*. An algebraic set that is not reducible is
*irreducible*. If <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/53d147e7f3fe6e47ee05b88b166bd3f6.svg?invert_in_darkmode" align=middle width=12.32879834999999pt height=22.465723500000017pt/> is an algebraic set, then a maximal irreducible
algebraic subset of <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/53d147e7f3fe6e47ee05b88b166bd3f6.svg?invert_in_darkmode" align=middle width=12.32879834999999pt height=22.465723500000017pt/> is called an *irreducible component of <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/53d147e7f3fe6e47ee05b88b166bd3f6.svg?invert_in_darkmode" align=middle width=12.32879834999999pt height=22.465723500000017pt/>*, or
simply a *component of <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/53d147e7f3fe6e47ee05b88b166bd3f6.svg?invert_in_darkmode" align=middle width=12.32879834999999pt height=22.465723500000017pt/>*.

The following fact is typically proven in a first commutative algebra or
algebraic geometry course.

Every algebraic set in <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/4397b563e5324f31e1f31a0dcb1c00dd.svg?invert_in_darkmode" align=middle width=19.998202949999992pt height=22.648391699999998pt/> or <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/d8e98e1639f3daca858dc2d68421687f.svg?invert_in_darkmode" align=middle width=18.17170904999999pt height=22.648391699999998pt/> is the union of
finitely many irreducible components.

In the case where a polynomial system has infinitely many solutions, it
is often best to describe each component separately. As a simple
example, consider the system given by <p align="center"><img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/5746d0db2e2154867c61fe102c9cc2dd.svg?invert_in_darkmode" align=middle width=146.12617799999998pt height=45.0083832pt/></p>

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

By a *hyperplane in <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/4397b563e5324f31e1f31a0dcb1c00dd.svg?invert_in_darkmode" align=middle width=19.998202949999992pt height=22.648391699999998pt/>*, we mean a variety of the form
<img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/6c6d75a4d4047338d19732e05cd6994c.svg?invert_in_darkmode" align=middle width=188.5384215pt height=24.65753399999998pt/> where one of
<img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/3bbd86a79d3cdca44791221c948bb6df.svg?invert_in_darkmode" align=middle width=69.40820699999999pt height=14.15524440000002pt/> is not zero. By a *hyperplane in <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/d8e98e1639f3daca858dc2d68421687f.svg?invert_in_darkmode" align=middle width=18.17170904999999pt height=22.648391699999998pt/>* we
mean a variety of the form
<img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/1ff5560132498da4e64fefe152400d70.svg?invert_in_darkmode" align=middle width=205.30786979999996pt height=24.65753399999998pt/> where one of
<img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/62a111d7caf4ea664b513ad2e16b130a.svg?invert_in_darkmode" align=middle width=69.40820699999999pt height=14.15524440000002pt/> is not zero. Intuitively, a *general hyperplane* is a
hyperplane where the parameters <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/65ed4b231dcf18a70bae40e50d48c9c0.svg?invert_in_darkmode" align=middle width=13.340053649999989pt height=14.15524440000002pt/> are chosen at random, and satisfy
no special relations. The program chooses "generic hyperplanes" by
picking coefficients the coefficients <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/65ed4b231dcf18a70bae40e50d48c9c0.svg?invert_in_darkmode" align=middle width=13.340053649999989pt height=14.15524440000002pt/> to be uniform random complex
numbers with real and imaginary parts in <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/a91e9fd592317527078e69a240fb943b.svg?invert_in_darkmode" align=middle width=49.31516864999999pt height=24.65753399999998pt/>. If coefficients are
chosen randomly in this way, then it is a fact that anything true of a
"generic hyperplane" will be true of a random hyperplane with
probability one. For those familiar with projective geometry who would
like a more rigourous definition of generic, see [@SWBook].

The following fact is often proved with the use of more powerful
theorems such as Bertini's theorem and Bezout's theorem, but we want to
get down to business, so we will take it for granted.

Let <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/cbfb1b2a33b28eab8a3e59464768e810.svg?invert_in_darkmode" align=middle width=14.908688849999992pt height=22.465723500000017pt/> be an irreducible algebraic variety in <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/4397b563e5324f31e1f31a0dcb1c00dd.svg?invert_in_darkmode" align=middle width=19.998202949999992pt height=22.648391699999998pt/> or
<img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/d8e98e1639f3daca858dc2d68421687f.svg?invert_in_darkmode" align=middle width=18.17170904999999pt height=22.648391699999998pt/>. Then there is unique number <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/2103f85b8b1477f430fc407cad462224.svg?invert_in_darkmode" align=middle width=8.55596444999999pt height=22.831056599999986pt/> such that the
intersection of <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/cbfb1b2a33b28eab8a3e59464768e810.svg?invert_in_darkmode" align=middle width=14.908688849999992pt height=22.465723500000017pt/> with <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/2103f85b8b1477f430fc407cad462224.svg?invert_in_darkmode" align=middle width=8.55596444999999pt height=22.831056599999986pt/> generic hyperplanes is finite and nonempty.
Moreover, the size of the intersection does not depend on the choice of
generic hyperplanes.

The number <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/2103f85b8b1477f430fc407cad462224.svg?invert_in_darkmode" align=middle width=8.55596444999999pt height=22.831056599999986pt/> we define to be the *dimension of <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/cbfb1b2a33b28eab8a3e59464768e810.svg?invert_in_darkmode" align=middle width=14.908688849999992pt height=22.465723500000017pt/>*, and the number
size of the intersection is the *degree of <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/cbfb1b2a33b28eab8a3e59464768e810.svg?invert_in_darkmode" align=middle width=14.908688849999992pt height=22.465723500000017pt/>*. [^1]

Returning to the example above, the two points on the parabola which
were outputed were the intersection of the parabola with one generic
hyperplane. As we would expect, the fact that there are two of them
means that the parabola has degree two. One of the main ideas in
numerical algebraic geometry is that many questions about a <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/2103f85b8b1477f430fc407cad462224.svg?invert_in_darkmode" align=middle width=8.55596444999999pt height=22.831056599999986pt/>
dimensional irreducible variety in <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/4397b563e5324f31e1f31a0dcb1c00dd.svg?invert_in_darkmode" align=middle width=19.998202949999992pt height=22.648391699999998pt/> or <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/d8e98e1639f3daca858dc2d68421687f.svg?invert_in_darkmode" align=middle width=18.17170904999999pt height=22.648391699999998pt/> can
be answered by knowing the its intersection with <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/2103f85b8b1477f430fc407cad462224.svg?invert_in_darkmode" align=middle width=8.55596444999999pt height=22.831056599999986pt/> generic
hyperplanes. This intersection is called a *witness set for <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/cbfb1b2a33b28eab8a3e59464768e810.svg?invert_in_darkmode" align=middle width=14.908688849999992pt height=22.465723500000017pt/>*.

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
algorithm is that "solutions at depth <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/55a049b8f161ae7cfeb0197d75aff967.svg?invert_in_darkmode" align=middle width=9.86687624999999pt height=14.15524440000002pt/>" lead to "solutions at depth
<img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/3f18d8f60c110e865571bba5ba67dcc6.svg?invert_in_darkmode" align=middle width=38.17727759999999pt height=21.18721440000001pt/>." The solutions at the last depth are the actual solutions to the
system. In this way, the program first populates one depth with
solutions, and then moves to the next. Setting the exploration order to
"depthFirst" will ensure that if a solution is found at depth <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/55a049b8f161ae7cfeb0197d75aff967.svg?invert_in_darkmode" align=middle width=9.86687624999999pt height=14.15524440000002pt/>, then
it is immediately used to find a solution at depth <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/3f18d8f60c110e865571bba5ba67dcc6.svg?invert_in_darkmode" align=middle width=38.17727759999999pt height=21.18721440000001pt/>, before looking
for other solutions at depth <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/55a049b8f161ae7cfeb0197d75aff967.svg?invert_in_darkmode" align=middle width=9.86687624999999pt height=14.15524440000002pt/>. The result is that the maximum number
full depth solutions are found after any given time.

In the directory "large" there is a system of 10 polynomials, all of
degree <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/6a8b4ac498753592cf18e12e85ace491.svg?invert_in_darkmode" align=middle width=36.52973609999999pt height=24.65753399999998pt/> with respect to variable groups <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/5210ef143b785833f37f2a934d9dabc9.svg?invert_in_darkmode" align=middle width=69.2463981pt height=14.15524440000002pt/> and
<img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/da386a261e5d84de3c4e2948434faa4b.svg?invert_in_darkmode" align=middle width=66.57528405pt height=14.15524440000002pt/>. This computation should take on the order of 30
seconds, so you can experiment with parallel processing, depth first
order, and using multiple variable groups versus a single variable
group.

[^1]: For those farmiliar with algebraic geometry, the degree of a
    variety in $\mathbb{C}^n$ or $\mathbb{P}^n$ is not an isomorphism
    invariant, since it depends on the embedding.


Example
-------

For a more complete description on how to use this software, see the tutorial [here](https://github.com/colinwcrowley/multiregeneration-tutorial).

Say that we are given the following two polynomials in the variables
<img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/0acac2a2d5d05a8394e21a70a71041b4.svg?invert_in_darkmode" align=middle width=25.350096749999988pt height=14.15524440000002pt/>. <p align="center"><img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/a8546fc93b1c9e52664a8bdf30f5ee4e.svg?invert_in_darkmode" align=middle width=137.57593905pt height=41.09589pt/></p> By inspection, we see that the set
of solutions consists of two points <img src="https://rawgit.com/JoseMath/multiregeneration/None/svgs/7c7e75ec4386aa242a1d739aef7ce8be.svg?invert_in_darkmode" align=middle width=96.80377244999998pt height=24.65753399999998pt/>. To solve the
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
