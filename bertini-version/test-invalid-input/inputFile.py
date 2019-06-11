logTolerance = -10
workingDirectory = "run"
variables = [["x"], ["y"]]
functions = ["x^2 + y^2 - 1"]
degrees = [[2, 2]]
functionNames = ["f1"]
# The next line has a dropped multiplication sign in the first product
l = [["(.2 + 1.2*I)x + (-.2 + .81*I)*y + 1"], ["(.49 - 1.0*I)*x + (.3 - .32*I)*y + .9*I"]]
r = [[None, "(.422 + 0.2*I)+(.123 + .234*I)*x","(.322 - 0.1*I)+(.15423 + .6314*I)*x"],[None, "(.322 - 1.1*I)+(.345 + .456*I)*y","(.122 + 1.01*I)+(.245 - .056*I)*y"]]
startSolution = "1.43901871347615 -2.13806242867528\n-.404632013550228 4.85729019730322"
# Circle in two variable groups
