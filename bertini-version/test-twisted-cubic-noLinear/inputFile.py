variables = [["x", "y", "z", "w"]]
# Maximal minors
# x y z
# y z w
functions = ["x*z-y^2", "y*w-z^2", "x*w-y*z"]
degrees = [[2], [2], [2]]
functionNames = ["f1","f2","f3"]
l = []
#l = [['(1+I*2)*((0.874544969163+I*0.909060010885)*x-(0.944555315441+I*0.944555315441)*w)+(1+I*2)*((0.874544969163+I*0.909060010885)*y-(0.832169245205+I*0.832169245205)*w)+(1+I*2)*((0.874544969163+I*0.909060010885)*z-(0.229320460489+I*0.229320460489)*w)', '(1+I*2)*((0.874544969163+I*0.909060010885)*x-(0.944555315441+I*0.944555315441)*w)+(1+I*2)*((0.874544969163+I*0.909060010885)*y-(0.832169245205+I*0.832169245205)*w)+(1+I*2)*((0.874544969163+I*0.909060010885)*z-(0.229320460489+I*0.229320460489)*w)', '(1+I*2)*((0.874544969163+I*0.909060010885)*x-(0.944555315441+I*0.944555315441)*w)+(1+I*2)*((0.874544969163+I*0.909060010885)*y-(0.832169245205+I*0.832169245205)*w)+(1+I*2)*((0.874544969163+I*0.909060010885)*z-(0.229320460489+I*0.229320460489)*w)']]
#r = [[None, "(.422 + 0.2*I)*(x+.1*y+.3*I*z+.2*z+I*w)+(.123 + .234*I)*x", "(.322 - 0.1*I)(2*x+.3*w+.1*I*z+.2*I+w)+(.15423 + .6314*I)*w"]]
logTolerance = -10
workingDirectory = "run"
startSolution ="0.944555315441 0.909060010885\n0.832169245205 0.959263990142\n0.229320460489 0.331928838032\n0.874544969163 0.477120977156"
projectiveVariableGroups = [0]
