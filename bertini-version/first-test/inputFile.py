# A number is considered 0 if it's less than 10^logTolerance
logTolerance = -10

# Give a 2D list of variable names, where the first index is the 
# variable group
variables = [["x", "y"]]

# Give the fucntions is the target system...
functions = ["x^2 + y^2 - 1", "y - x^2"]

#...along with their degrees. i.e. degrees[s][i] = the degree of the 
# s'th function in the i'th variable group.
degrees = [[2], [2]]

# Give the funtions names to make the bertini files readable
functionNames = ["f1", "f2"]

# Give the dimension linear equations. This should be 2D list of generic 
# linear equations, such that l[i][j] is a linear equation in the 
# variables of group i, and the number of l[i][j] for fixed i is equal 
# to the number of variables in group i.
l = [["(2 + 1.2*I)*x + (-2 + 81*I)*y + 1", "(49 - I)*x + (3 - 32*I)*y + I"]]

#Give a common solution to all the l[i][j] in the format of a bertini 
# start file
startSolution = "1\n\n0\n-0.00775713 -0.0207183\n0.000933595 0.012438"

# Given the regeneration linear equations. This should be a 2D list of 
# generic linear equations, where r[i][d] is a linear equation in the 
# variables of group i, and the number of r[i][d] for fixed i is equal 
# to the maximum degree of any function in the target system in the 
# variables of group i. Additionally, r[i][0] should be 'None' for all 
# i. This is becaues we use one of the l[i] instead.
r = [[None, "(123 + 234*I)*x + (345 + 456*I)*y"]]

#Give the name of the directory where you would like the script to run 
# its homotopy continuations. If the specified directory already exists, 
# it will be deleted when the script is run.
workingDirectory = "run2"
