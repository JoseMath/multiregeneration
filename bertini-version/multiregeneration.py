#TODO: Think about the hypothesis that would
# ensure the following: if a point gets thrown out along the way,
# then that point

# Caveat: Bertini input file style assumptions
# # 'variable group ...;' is one line
# # 'hom_variable group ...;' is one line
# # function ...;  is one line
# # Lines after the second CONFIG not defining an equation or constant value
# # must begin with 'function', 'constant', 'hom_variable_group', or 'variable_group'

import shutil
import sys
import subprocess
import hashlib
import os
import random

# variables = [["x1", "x2"], ["y1", "y2"]]
# len(variables)
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
# Optional inputs # This can be specified in the inputFile
projectiveVariableGroups = []  # This can be specified in the inputFile
randomNumberGenerator = random.random

# TODO: Restart mode.
depth = 0  # Begin the computation at a different depth index


verbose = 1  # Integer that is larger if we want to print more
# Level 0 for nothing except errors
# Level 1 messages we would usually like printed
# Level 2 for debugging

#TODO: instead of setting global variables with an eval, read a json
# file to a python object
variables = None
functions = None
degrees = None
functionNames = None
l = None
r = None
startSolution = None
workingDirectory = "run"
logTolerance = -10
bertiniVariableGroupString = None

useBertiniInputStyle = False
bertiniTrackingOptionsText = ""
bertiniVariablesAndConstants = None
bertiniFunctionNames = None
bertiniEquations = None
revisedEquationsText = None
variableGroupText = None
def main():
    # Set global configuration variables in the inputFile
    global variables
    global functions
    global degrees
    global functionNames
    global l
    global r
    global startSolution
    global workingDirectory
    global logTolerance
    global verbose
    global projectiveVariableGroups
    global bertiniVariableGroupString


    global useBertiniInputStyle
    global bertiniVariablesAndConstants
    global bertiniFunctionNames
    global revisedEquationsText
    global variableGroupText
    global bertiniTrackingOptionsText
    setVariablesToGlobal = """
global variables
global functions
global degrees
global functionNames
global l
global r
global startSolution
global workingDirectory
global logTolerance
global verbose
global projectiveVariableGroups
global useBertiniInputStyle
"""

    exec(setVariablesToGlobal + open("inputFile.py").read())
# Our input will consist of four text files and a main input file.
# bertiniInput_variablesAndConstants
# bertiniInput_trackingOptions
# bertiniInput_equations
    try:
        with open("bertiniInput_variablesAndConstants", "r") as f:
            bertiniVariablesAndConstants = f.read()
        with open("bertiniInput_trackingOptions", "r") as f:
            bertiniTrackingOptionsText = f.read()
# TODO:       with open("bertiniInput_degrees", "r") as f:
#            bertiniDegrees = f.read()
        with open("bertiniInput_equations", "r") as f:
            bertiniEquations = f.read()
    except:
        print("Exiting due to incomplete input. Please include the following files:")
        print("\t" + "bertiniInput_variablesAndConstants")
        print("\t" + "bertiniInput_trackingOptions")
#            print("\t" + "bertiniInput_functionNames")
        print("\t" + "bertiniInput_equations")
        sys.exit(1)
# Set up variables
    variableGroupText = ""
    variables = []
    lines = bertiniVariablesAndConstants.splitlines()
    for i in range(len(lines)):
        variableGroupType = lines[i].split(" ")[0]
        if not (variableGroupType == "variable_group" or variableGroupType == "hom_variable_group"):
            print("Exiting because a variable group other that 'variable_group' or 'hom_variable_group' was declared.")
            sys.exit(1)
        if variableGroupType == "hom_variable_group":
            projectiveVariableGroups.append(i)
        variableGroupText+=lines[i]+"\n"
        variables.append(lines[i][lines[i].find(" "):].replace(" ","").replace(";", "").split(","))
    print("variables")
    print(variables)
    print("projectiveVariableGroups")
    print(projectiveVariableGroups)
    print("variableGroupText")
    print(variableGroupText)
# set up function names and revisedEquationsText
    revisedEquationsText = ""
    lines = bertiniEquations.splitlines()
    for i in range(len(lines)):
        functionLine = lines[i].split(" ")[0]
        if functionLine == "function":
            functionNames = lines[i][lines[i].find(" "):].replace(" ","").replace(";", "").split(",")
        else:
            revisedEquationsText += lines[i]+"\n"
    print("functionNames")
    print(functionNames)
    print("revisedEquationsText")
    print(revisedEquationsText)
# set degrees TODO


    #####################
# Make directory to store final solutions
    if os.path.isdir(workingDirectory):
        shutil.rmtree(workingDirectory)
    os.mkdir(workingDirectory)
    os.chdir(workingDirectory)
    os.mkdir("all_full_depth_solutions")

# print to screen system summary.
    if verbose > 0:
        print("\n################### Starting multiregeneration ####################\n")
        print("These variable groups have been selected:\n"+variableGroupText)
        print("Solutions in a 'linearProduct' directory and :")
        for c, f in enumerate(functionNames): # 0 is the depth we start with
            if c >= depth:
                print("depth > "+str(c)+" satisfy "+ f+" = 0")
# Determine random linear polynomials l[i][j]
    (l, startSolution) = getLinearsThroughPoint(variables)
    print(l)
    print(startSolution)
# Determine random linear polynomials r[i][j]
    r = []
    for i in range(len(variables)):
        r.append([])
        maxdeg= 0
        for s in range(len(functionNames)):
            maxdeg= max(maxdeg,degrees[s][i])
        print("%s is the maximum degree in variable group %s. "%(maxdeg,i))
        for d in range(maxdeg):
            r[i].append(getGenericLinearInVariableGroup(i))
        print("This is the last linear polynomial in r[%s]: \n%s" % (i,str(r[i][-1])))
# For the first node here are all the outedges
    print("For the first node here are all the outedges")
    for i in range(len(variables)):
        for j in range(degrees[0][i]):
            #TODO understand what is wrong here.
            print(projectiveVariableGroups)
            currentDimension=[(len(group) - 1 if (i in projectiveVariableGroups) else len(group)) for group in variables]
            print("currentDimension  #A#")
            print(currentDimension)
            for k in range(len(variables)):
                print(k)
                currentDimension[k] = len(variables[k])
                if k in projectiveVariableGroups:
                    currentDimension[k] = len(variables[k])-1
            print("currentDimension  #B#")
            print(currentDimension)
            useFunction=[False for f in functionNames]
            print(useFunction)
            regenerationLinearIndex=[i,j]
            regenerateAndTrack(depth,
                useFunction, # gens
                currentDimension,
                regenerationLinearIndex, # varGroup and regenLinear
                startSolution)

    os.chdir("..")

# used to get generic linears (A)
def getGenericLinearInVariableGroup(variableGroup):
    terms = []
    for var in variables[variableGroup]:
      terms.append("(%s + I*%s)*%s"%(str(randomNumberGenerator()),
        str(randomNumberGenerator()),
        var))
    if not variableGroup in projectiveVariableGroups:
      terms.append("(%s + I*%s)"%(str(randomNumberGenerator()),
        str(randomNumberGenerator())))
    return "+".join(terms)


# used to get generic linears (B)
def getLinearsThroughPoint(variables):
    spoint = []
    for i in range(len(variables)):
        spoint += [[]]
        for j in range(len(variables[i])):
            spoint[i]+=[[str(randomNumberGenerator()),str(randomNumberGenerator())]]
#    print(spoint)
    startSolution = ""
    for i in range(len(spoint)):
        for j in range(len(spoint[i])):
            startSolution+=spoint[i][j][0]+" "+spoint[i][j][1]
            startSolution+="\n"
    print(startSolution)
    ell = []
    for i in range(len(variables)):
        ell.append([])
        isAffGroup=1
        if i in projectiveVariableGroups:
            isAffGroup = 0
        terms = [None for x in range(len(variables[i])+isAffGroup-1)]
#        print(terms)
        for j in range(len(variables[i])+isAffGroup-1):
            linearString=""
            for x in range(len(variables[i])+isAffGroup-1):
                if isAffGroup:
                    terms[x]="(%s+I*%s)*(%s-(%s+I*%s))"%(
                        str(randomNumberGenerator()),
                        str(randomNumberGenerator()),
                        str(variables[i][x]),
                        spoint[i][x][0],
                        spoint[i][x][1],
                        )
                else:
                    terms[x]="(%s+I*%s)*((%s+I*%s)*%s-(%s+I*%s)*%s)"%(
                        str(randomNumberGenerator()),
                        str(randomNumberGenerator()),
                        str(spoint[i][-1][0]), #real  part of last coordinate of spoint
                        str(spoint[i][-1][1]),  # imaginary part of last coordinate of spoint
                        str(variables[i][x]), # a variable in group i
                        str(spoint[i][x][0]),
                        str(spoint[i][x][1]),
                        str(variables[i][-1])) # last variable in group i
            #print(terms)
            linearString = "+".join(terms)
        #    print("Linear")
        #    print(linearString)
        #    print(" End Linear")
            ell[i].append(linearString)
    for i in range(len(variables)):
        print("\nThis is the first linear polynomial for variable group %s.\n "% i)
        print(ell[i][0])
    return (ell, startSolution)


# helper function to determine if a value is zero.
def isZero(s, logTolerance):
  if all([not str(i) in s for i in range(1, 10)]):
    return True
  return int(s.split("e")[1]) < logTolerance


# calls Bertini to evaluate a point.
def vanishes(dirName, functionName, point, logTolerance):
# a function that returns True if functionString defines a polynomial vanishing at point
    try:  # What is happening here?
        os.mkdir(dirName)
    except:
        print("Ope! Error opening directory '%s'"%dirName)
# Write input file for evaluation.
    print("Vanishes function")
    print(bertiniTrackingOptionsText)
    print(variableGroupText)
    print(revisedEquationsText)
    print(functionName)
    inputText = '''
CONFIG
  %s
  TrackType:-4;
END;
INPUT
  %s
  function evalF;
  %s
  evalF = %s;
END;
      ''' % (bertiniTrackingOptionsText, variableGroupText, revisedEquationsText, functionName)
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
    if not solutionsLines:
        print("Bertini error")
        sys.exit(1) # the one is for error and 0 is for everyhting is fine.
    value = solutionsLines[2].split(' ')

    isVanishing = isZero(value[0], logTolerance) and isZero(value[1],
        logTolerance)

    with open("isVanishing", "w") as isVanishingFile:
      isVanishingFile.write(str(isVanishing))

    os.chdir(cwd) #Can we move this right after the previous except?
    return isVanishing


# Makes the directory for each process.
def directoryName(depth, useFunction, currentDimension, varGroup,
    regenLinear, homotopyKind, point):
    dirName = "depth_%d_gens_%s_dim_%s_varGroup_%d_regenLinear_%d_homotopy_%s_pointId_%s"%(depth,
        "".join(map(lambda b: "1" if b else "0", useFunction)),
        "_".join(map(str, currentDimension)),
        varGroup,
        regenLinear,
        homotopyKind,
        (abs(hash(point)) % (10 ** 8)))
    return dirName


def solutionFileName(depth, useFunction, currentDimension, varGroup, regenLinear, point):
    solutionFileName = "all_full_depth_solutions/depth_%d_gens_%s_dim_%s_varGroup_%d_regenLinear_%d_pointId_%s"%(depth,
        "".join(map(lambda b: "1" if b else "0", useFunction)),
        "_".join(map(str, currentDimension)),
        varGroup,
        regenLinear,
        (abs(hash(point)) % (10 ** 8)))
    return solutionFileName


# performs a homotopy
def homotopy(dirName, functionNames, startFunctionString, targetFunctionString, startSolutionsList,ellText,rText):
    try:
        os.mkdir(dirName)
    except:
        print("Ope! Error opening directory '%s'"%dirName)
# Write input file.
    print("Homotopy")
    inputText = '''
CONFIG
    %s
    ParameterHomotopy : 2;
END;
INPUT
    %s
    parameter Tpath ;
    function %s;
    %s
    %s
    %s
    HF = Tpath*(%s)+(1-Tpath)*(%s);
END;
    '''%(bertiniTrackingOptionsText,
          variableGroupText,
          ",".join(functionNames),
          revisedEquationsText,
          ellText,
          rText,
          startFunctionString,
          targetFunctionString)
    inputFile = open("%s/input"%dirName, "w")
    inputFile.write(inputText)
    inputFile.close()
# write start file
    startBody = ""
    for sol in startSolutionsList:
        startBody += "\n\n%s"%(sol)
    startText = "%d%s"%(len(startSolutionsList), startBody)
    startFile = open("%s/start"%dirName, "w")
    startFile.write(startText)
    startFile.close()
# write start parameters
    startFile = open("%s/start_parameters"%dirName, "w")
    startFile.write("1\n1 0")
    startFile.close()
# write target parameters
    startFile = open("%s/final_parameters"%dirName, "w")
    startFile.write("1\n0 0")
    startFile.close()
# Change directory to call Bertini.
    os.chdir(dirName)
    try:
        bertiniCommand = "bertini input"
        process = subprocess.Popen(bertiniCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
    except:
        print("There the command `bertini input` exited with the\
            following' error. Make sure you have bertini installed.")
        print(error)
# Check to see if there are nonsingular_solutions
    if not os.path.isfile("nonsingular_solutions"):
      print("Exiting because could  not find 'nonsingular_solutions'.\
          Bertini gave the following output.\n\n")
      print(repr(output))
      sys.exit(1)
    solutionsFile = open("nonsingular_solutions", "r")
    solutionsLines = solutionsFile.readlines()
    solutionsFile.close()
    out = ""
    for i in range(2, len(solutionsLines)):
        out+="\n%s"%solutionsLines[i]
    os.chdir("..")
    return out


# Takes P to Q by calling homotopy()
def regenerate(depth, useFunction, currentDimension, regenerationLinearIndex, point):
    regenerationSystem = []
    regenerationSystemFunctionNames = []
    currentIndexInSystem = -1
    regenerationSystemTargetIndex = 0
    for i in range(len(functionNames)):
        if useFunction[i]:
            regenerationSystem.append(functionNames[i])
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
    startFunctionString="l_%s_%s" %(regenerationLinearIndex[0],currentDimension[regenerationLinearIndex[0]]-1)
    print("startFunctionString")
    print(startFunctionString)
    targetFunctionString="r_%s_%s" %(regenerationLinearIndex[0],regenerationLinearIndex[1])
    print("targetFunctionString")
    print(targetFunctionString)
    print("before regeneratedPoint")
    ellText = "\n % ellText\n"
    for i in range(len(currentDimension)):
        for j in range(currentDimension[i]):
            ellText += "l_%s_%s" %(i,j)+" = "+l[i][j]+" ; \n"
    print("ellText\n"+ellText)
    rText = "\n % rText\n"
    for i in range(len(degrees[0])):
        for j in range(degrees[depth][i]):
            print(j)
            rText += "r_%s_%s" %(i,j)+" = "+r[i][j]+" ; \n"
    print("rText\n"+rText)
    regeneratedPoint = homotopy(dirName,
            regenerationSystemFunctionNames,
            startFunctionString,
            targetFunctionString,
            [point],
            ellText,
            rText )
    return regeneratedPoint

#NOTE: You can keep track of the codimension in each factor, and give up
# on a solution if you can tell that the codimension will already be too
# small.


def regenerateAndTrack(depth, useFunction, currentDimension, regenerationLinearIndex, point):
    if any([d < 0 for d in currentDimension]):
      return
## Step 1. Check if point is in the next hypersurface.
    checkVanishesDirName = directoryName(depth, useFunction,
        currentDimension, regenerationLinearIndex[0],
        regenerationLinearIndex[1], "eval", point)
    if vanishes(checkVanishesDirName, functionNames[depth], point, logTolerance):
        print("Passed: Vanishes--vanished")
        if depth+1 is len(functionNames):
            with open(solutionFileName(depth, useFunction, currentDimension,
                regenerationLinearIndex[0],
                 regenerationLinearIndex[1], point), "w") as solutionFile:
                solutionFile.write(point)
            return
        regenerateAndTrack(depth + 1, useFunction, currentDimension,
            regenerationLinearIndex, point)
        return
    print("Passed: Vanishes--did not vanish")
## Step 2: regenerate new point.
    regeneratedPoint = regenerate(depth, useFunction, currentDimension, regenerationLinearIndex, point)
    print(regeneratedPoint)
    print("Passed: Regenerate")
    if regeneratedPoint is "": #if not smooth we assume the string will be empty TODO: check bertini documentation if this is actually true.
      return
# Step 3: set up linaer product and system
    print("STEP 3 ####")
    print(currentDimension)
    dirName = directoryName(depth, useFunction, currentDimension,
        regenerationLinearIndex[0], regenerationLinearIndex[1],
        "linearProduct", point)
    print("Passed: directoryName in step 3.")
    linearProduct = "(1)"
    print("Degrees %s" % (degrees[depth]))
    for i in range(len(variables)):
        for j in range(degrees[depth][i]):
            print("LinearProduct factor %s %s"%(i, j))
            linearProduct += "*(r_%s_%s)"%(i, j)
    print("LP %s" % linearProduct)
    # make a system of equations to track the linear product to f_D
    linearProductHomotopySytemNames = ["HF"]
    for i in range(0, depth):
        if useFunction[i]:
            linearProductHomotopySytemNames.append(functionNames[i])
    for i in range(len(variables)):
        for j in range(currentDimension[i]):
            print(i,j)
            if not (i == regenerationLinearIndex[0] and j == currentDimension[i]-1):
                linearProductHomotopySytemNames.append("l_%d_%d"%(i,j))
    print("linearProductHomotopySytemNames")
    print(linearProductHomotopySytemNames)
# Step 4. Now we prepare the linears we wil need in our beritni input file
    ellText = "\n % ellText\n"
    for i in range(len(currentDimension)):
        for j in range(currentDimension[i]):
            ellText += "l_%s_%s" %(i,j)+" = "+l[i][j]+" ; \n"
    print("ellText\n"+ellText)
    rText = "\n % rText\n"
    for i in range(len(degrees[0])):
        for j in range(degrees[depth][i]):
            print(j)
            rText += "r_%s_%s" %(i,j)+" = "+r[i][j]+" ; \n"
    print("rText\n"+rText)
# Step 5. now we track
    trackedPoint = homotopy(dirName,
            linearProductHomotopySytemNames,
            linearProduct,
            functionNames[depth],
            [regeneratedPoint],ellText,rText)
    if not trackedPoint: # if it's singular the string will be empty
        return
    if depth+1 is len(functionNames):
        with open(solutionFileName(depth, useFunction, currentDimension,
            regenerationLinearIndex[0], regenerationLinearIndex[1],
            trackedPoint), "w") as solutionFile:
            solutionFile.write(trackedPoint)
        return
    for i in range(len(variables)):
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
                regenerateAndTrack(depth+1, newUseFunction, newCurrentDimension, [i,j], trackedPoint)
                sys.exit(0)



if __name__== "__main__":
  main()
