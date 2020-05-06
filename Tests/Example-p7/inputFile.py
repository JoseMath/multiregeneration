# A number is considered 0 if it's less than 10^logTolerance
logTolerance = -10

# Give a 2D list of variable names, where the first index is the
# variable group in bertiniInput_variables

# The fucntions to solve are in bertiniInput_equations, but the degrees are here
# i.e. degrees[s][i] = the degree of the s'th function in the i'th variable group.
degrees = [[3], [2]]

#Give the name of the directory where you would like the script to run
# its homotopy continuations. If the specified directory already exists,
# it will be deleted when the script is run.
workingDirectory = "run"

verbose = 1
