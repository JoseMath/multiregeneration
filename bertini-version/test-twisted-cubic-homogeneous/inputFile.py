variables = [["x", "y", "z", "w"]]
# Maximal minors
# x y z
# y z w
functions = ["x*z-y^2", "y*w-z^2", "x*w-y*z"]
degrees = [[2], [2], [2]]
functionNames = ["f1","f2","f3"]
l = [["(1.14+1.02*I)*(x-2*y)+(0.14-2.02*I)*(3*y-z)+(2.14+0.07*I)*(z-5*w)","(1.14-2.02*I)*(3*y-z)+.34*(z-5*w)","(0.14+0.07*I)*(z-5*w)+(2.14-1.02*I)*(x-2*y)"]]
r = [[None, "(.422 + 0.2*I)*(x+.1*y+.3*I*z+.2*z+I*w)+(.123 + .234*I)*x", "(.322 - 0.1*I)(2*x+.3*w+.1*I*z+.2*I+w)+(.15423 + .6314*I)*w"]]
logTolerance = -10
workingDirectory = "run"
startSolution ="1.0 0.0\n0.5 0.0\n1.5 0.0\n0.0 0.0"
projectiveVariableGroups = [0]
