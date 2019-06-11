#TODO: 1. have a intermediate steps dir where you do all the
# homotopies. Check for it and delete it at the beginning of each run
# 2. Do the projective case. 3. Think about the hypothesis that would
# ensure the following: if a point ...

import shutil
import sys
import subprocess
import hashlib
import os

# variables = [["x1", "x2"], ["y1", "y2"]]
# len(variables)
# variablesString = "x1, x2, y1, y2"
# functions = ["x1^2 + x2^2 - 1", "y1^2 + y2^2 - 1"]
# degrees = [[2, 0], [0,2]] # degree of the s'th function in the i'th variable group
# n = [len(l) for l in variables]
# maxDegree = [2, 2] # the largest degree of any function in the ith variable group
# functionNames = ["f1", "f2"]
# tolerance = 1e-10
# # The l_i,j  are the dimention linears in the variables i the i'th group
# l = [["234*x2 - x1 - 234.2341", "x2 + 2*x1 - 1231"], ["19*y2 - y1 - 1123.235",
#     "y2 + 393*y1 - 12"]]
# # The r_i,d are the regeneration linears in the i'th variable group.
# # For fixed i, there are maxDegree[i] - 1
# r = [[None, "x1 - 2*x2 + 2.1"], [None, "5*y1 + y2 - 25"]] #So that the
# # indexing matches the write up, we want the r to start at 1.

# Can we have our file names consist of strings likes _class_index
# where class takes a value in {depth, dim, group, deg, type, prune}
# and the respective class_index are in  NN, n_\bullet, [k], NN, {smooth, singular, infinity, {0,1}}


### Configuration ###
projectiveVariableGroups = [] # This can be specified in the inputFile
exec(open("inputFile.py").read())

flatVariablesList = [item for sublist in variables for item in sublist]
variablesString = ",".join(flatVariablesList)
bertiniVariableGroupString = ""
for c, value in enumerate(variables):
    if c in projectiveVariableGroups:
        bertiniVariableGroupString+="hom_variable_group "+",".join(value)+" ;\n"
    else:
        bertiniVariableGroupString+="variable_group "+",".join(value)+" ;\n"
print(bertiniVariableGroupString)
#####################

# variables = inputFile.variables
# functions = inputFile.functions
# degrees = inputFile.degrees
# functionNames = inputFile.functionNames
# l = inputFile.l
# r = inputFile.r
# startSolution = inputFile.startSolution

# Jose thinks startSolution should be a file name rather than a list of numbers.

def isZero(s, logTolerance):
  if all([not str(i) in s for i in range(1, 10)]):
    return True
  return int(s.split("e")[1]) < logTolerance

def vanishes(dirName, variablesString, functionString, point, logTolerance):
# a function that returns True if functionString defines a polynomial vanishing at point
# What is going on with the comments below?
    # currentVariable = 0
    # evalString = function
    # for z in point.splitlines():
    #     if len(z) > 1:
    #         evalString = evalString.replace(variablesList[currentVariable],
    #                 "(%sj)"%(z.replace(" ", " + ")))
    # evalString = evalString.replace("^", "**")
    # return eval(evalString)

    try:  # What is happening here?
        os.mkdir(dirName)
    except:
        print("Ope! Error opening directory '%s'"%dirName)
# Write input file for evaluation.
# TODO: replace variable_group %s with a list of variable groups from variables
# and indicate if hom_variable_group or variable_group
# TODO: change the ``f" in the Bertini input file to a nonstandard notation so it doesn't conflict with a user choice.
    inputText = '''
CONFIG
    TrackType:-4;
END;
INPUT
    %s
    function f;
    f = %s;
END;
        ''' % (bertiniVariableGroupString, # use variable groups
                functionString)
    inputFile = open("%s/input"%dirName, "w")
    inputFile.write(inputText)
    inputFile.close()

# Write start file for evaluation.
# Why don't we copy this file from nonsingular_solutions?
# I don't think we should be writing start files. We should be copying them around directories.
    startText = "1\n\n"+point # The first one is because we always track one solution per process.
    startFile = open("%s/start"%dirName, "w")
    startFile.write(startText)
    startFile.close()

# Get current working directory to run Bertini.
    cwd = os.getcwd()
    os.chdir(dirName)
    try:
        bertiniCommand = "bertini input"
        process = subprocess.Popen(bertiniCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
    except:
        print(error) # Need a description of this error.
# Open the Bertini output file named 'function' and determine if this is zero.
    try:
        solutionsFile = open("function", "r")
        solutionsLines = solutionsFile.readlines()
        solutionsFile.close()
    except:
        print("Ope! Error opening file 'function'")
    # TODO return true of false for zero of nonzero  # isn't this already done?
    value = solutionsLines[2].split(' ')

    isVanishing = isZero(value[0], logTolerance) and isZero(value[1],
        logTolerance)

    with open("isVanishing", "w") as isVanishingFile:
      isVanishingFile.write(str(isVanishing))

    os.chdir(cwd) #Can we move this right after the previous except?
    return isVanishing

def directoryName(depth, useFunction, currentDimension, varGroup,
    regenLinear, homotopyKind, point):
# Makes the directory for each process.
    dirName = "depth_%d_gens_%s_dim_%s_varGroup\
_%d_regenLinear_%d_homotopy_%s\
_pointId_%s"%(depth,
            "".join(map(lambda b: "1" if b else "0", useFunction)),
            "_".join(map(str, currentDimension)),
            varGroup,
            regenLinear,
            homotopyKind,
            (abs(hash(point)) % (10 ** 8)))
    return dirName


def homotopy(dirName, variablesString, functionNames, functionsList, indexToTrack, targetFunctionString, startSolutionsList):
# Now write Bertini-input files and call a homotopy.
    body = ""
    for i in range(len(functionsList)):
        if i is not indexToTrack:
            body+="\n %s = %s;"%(functionNames[i], functionsList[i])
        elif i is indexToTrack:
            body+="\n %s = s*(%s) + (1-s)*(%s);"%(functionNames[i],
                    functionsList[i], targetFunctionString)

    try: # Jose moved this before defining inputText.
        os.mkdir(dirName)
    except:
        print("Ope! Error opening directory '%s'"%dirName)

# TODO: replace variable %s with a list of variable groups from variables
# and indicate if hom_variable_group or variable_group
# Write input file.
    inputText = '''
CONFIG
    UserHomotopy: 2;
END;
INPUT
    %s
    function %s;
    pathvariable t;
    parameter s;
    s = t;
    %s
END;
''' % (bertiniVariableGroupString,
                ",".join(functionNames),body)
    inputFile = open("%s/input"%dirName, "w")
    inputFile.write(inputText)
    inputFile.close()

# Write start file.
    startBody = ""
    for sol in startSolutionsList:
        startBody += "\n\n%s"%(sol)
    startText = "%d%s"%(len(startSolutionsList), startBody)

    startFile = open("%s/start"%dirName, "w")
    startFile.write(startText)
    startFile.close()

# Change directory to call Bertini? What is happening here?
    os.chdir(dirName)
    try:
        bertiniCommand = "bertini input"
        process = subprocess.Popen(bertiniCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
    except:
        print(error)  # TODO: error description
# Check to see if there are nonsingular_solutions
    try:
        solutionsFile = open("nonsingular_solutions", "r")
        solutionsLines = solutionsFile.readlines()
        solutionsFile.close()
    except:  # Should this be an error?
        print("Ope! Error opening file '%s/nonsingular_solutions'"%dirName)

    out = ""
    for i in range(2, len(solutionsLines)):
        out+="\n%s"%solutionsLines[i]

    os.chdir("..")

    return out


def regenerate(depth, useFunction, currentDimension, regenerationLinearIndex, point):
    # Performs the regeneration homotopy.
    regenerationSystem = []
    regenerationSystemFunctionNames = []
    currentIndexInSystem = -1
    regenerationSystemTargetIndex = 0
    for i in range(len(functions)):
        if useFunction[i]:
            regenerationSystem.append(functions[i])
            regenerationSystemFunctionNames.append(functionNames[i])
            currentIndexInSystem+=1
    for i in range(len(variables)):

        for j in range(currentDimension[i]):
            regenerationSystem.append(l[i][j])
            regenerationSystemFunctionNames.append("l_%d_%d"%(i,j))
            currentIndexInSystem += 1

        if i is regenerationLinearIndex[0]:
        # If the current variable group is the target one
            regenerationSystemTargetIndex = currentIndexInSystem
            # Then the target l to get rid of is the last one in that
            # variable group

    dirName = directoryName(depth, useFunction, currentDimension,
        regenerationLinearIndex[0], regenerationLinearIndex[1], "regen",
        point)

    print("regenerating point = %s"%point)
    regeneratedPoint = homotopy(dirName,
            variablesString,
            regenerationSystemFunctionNames,
            regenerationSystem,
            regenerationSystemTargetIndex,
            r[regenerationLinearIndex[0]][regenerationLinearIndex[1]],
            [point])

    return regeneratedPoint

# print(regenerate([False, False], [2,2], [0,0], "0\n\n0 0\n1 0\n0 0\n1 0"))

# 0,1,0,1

#NOTE: You can keep track of the codimension in each factor, and give up
# on a solution if you can tell that the codimension will already be too
# small.

def regenerateAndTrack(depth, useFunction, currentDimension, regenerationLinearIndex, point):
    if depth >= len(functions):
        return

    checkVanishesDirName = directoryName(depth, useFunction,
        currentDimension, regenerationLinearIndex[0],
        regenerationLinearIndex[1], "eval", point)

    if vanishes(checkVanishesDirName, variablesString,
            functions[depth],
            point, logTolerance):
        regenerateAndTrack(depth + 1, useFunction, currentDimension,
                regenerationLinearIndex, point)
        return

    if regenerationLinearIndex[1] is not 0:
        regeneratedPoint = regenerate(depth, useFunction, currentDimension, regenerationLinearIndex, point)
    else:
        regeneratedPoint = point

    # TODO: if regenerated point is singular, throw it out

    #track the regenerated point to the target function
    dirName = directoryName(depth, useFunction, currentDimension,
        regenerationLinearIndex[0], regenerationLinearIndex[1],
        "linearProduct", point)

    i = regenerationLinearIndex[0]
    linearProduct = "(%s)"%l[i][currentDimension[i]-1]
    for j in range(1, degrees[depth][i]):
        linearProduct += "*(%s)"%r[i][j]

    # make a system of equations to track the linear product to f_D
    linearProductHomotopySytem = [linearProduct]
    linearProductHomotopySytemNames = [functionNames[depth]]

    for i in range(0, depth):
        if useFunction[i]:
            linearProductHomotopySytem.append(functions[i])
            linearProductHomotopySytemNames.append(functionNames[i])
    for i in range(len(variables)):
        for j in range(currentDimension[i]): #exclude the last one
            # because we are using the linear product instead
            if not (i is regenerationLinearIndex[0] and j is
                    currentDimension[i]-1):
                linearProductHomotopySytem.append(l[i][j])
                linearProductHomotopySytemNames.append("l_%d_%d"%(i,j))

    print("tracking point = %s"%point)
    trackedPoint = homotopy(dirName,
            variablesString,
            linearProductHomotopySytemNames,
            linearProductHomotopySytem,
            0,
            functions[depth],
            [regeneratedPoint])

    for i in range(len(variables)):
        if currentDimension[i] is not 0: #TODO: replace this with a condition
            # that depends on the expexcted multidimension
            if depth+1 < len(functions):
                for j in range(degrees[depth+1][i]):

                    newUseFunction = []
                    for b in useFunction:
                        newUseFunction.append(b)
                    newUseFunction[depth] = True

                    newCurrentDimension = []
                    for d in currentDimension:
                        newCurrentDimension.append(d)
                    newCurrentDimension[i] = currentDimension[i]-1

                    child_pid = os.fork()
                    if child_pid == 0:
                        regenerateAndTrack(depth+1, newUseFunction,
                                newCurrentDimension, [i,j], trackedPoint)
                        print("\nprocess terminating at edge")
                        sys.exit(0)


def main():
    if os.path.isdir(workingDirectory):
        shutil.rmtree(workingDirectory)

    os.mkdir(workingDirectory)
    os.chdir(workingDirectory)

    for i in range(len(variables)):
        for j in range(len(variables[i])):
            regenerateAndTrack(0, [False for f in functions],
                    [len(group) for group in variables], [i,j], startSolution)

    os.chdir("..")

if __name__== "__main__":
  main()
