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
import os.path
from os import path
# variables = [["x1", "x2"], ["y1", "y2"]]
# len(variables)
# degrees = [[2, 0], [0,2]] # degree of the s'th function in the i'th variable group
# n = [len(l) for l in variables]
# maxDegree = [2, 2] # the largest degree of any function in the ith variable group
# G = ["f1", "f2"]
# tolerance = 1e-10
# # The l_i,j  are the dimention linears in the variables i the i'th group
# l = [["234*x2 - x1 - 234.2341", "x2 + 2*x1 - 1231"], ["19*y2 - y1 - 1123.235",
#     "y2 + 393*y1 - 12"]]
# # The r_i,d are the regeneration linears in the i'th variable group.
# # For fixed i, there are maxDegree[i] - 1
# r = [[None, "x1 - 2*x2 + 2.1"], [None, "5*y1 + y2 - 25"]] #So that the
# # indexing matches the write up, we want the r to start at 1.


### Configuration ###
# Optional inputs # This can be specified in the inputFile
projectiveVariableGroups = []  # This can be specified in the inputFile
#randomNumberGenerator = random.random
def randomNumberGenerator():
    rho = random.uniform(-1,1)
    return rho
# TODO: Restart mode.
depth = 0  # Begin the computation at a different depth index
bfe = []
verbose = 1  # Integer that is larger if we want to print more
# Level 0 for nothing except errors
# Level 1 messages we would usually like printed
# Level 2 for debugging

#TODO: instead of setting global variables with an eval, read a json
# file to a python object
variables = None
fNames = None
degrees = None
G = []
l = None
r = None
B= None
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
    global depth
    global bfe
    global fNames
    global degrees
    global B
    global G
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
global depth
global bfe
global fNames
global degrees
global B
global G
global l
global r
global startSolution
global workingDirectory
global logTolerance
global verbose
global projectiveVariableGroups
global useBertiniInputStyle
"""

    # exec(setVariablesToGlobal + open("inputFile.py").read())
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
            print("found bertiniInput_equations")
    except:
        print("Exiting due to incomplete input. Please include the following files:")
        print("\t" + "bertiniInput_variablesAndConstants")
        print("\t" + "bertiniInput_trackingOptions")
#            print("\t" + "bertiniInput_G")
        print("\t" + "bertiniInput_equations")
        # sys.exit(1)
# Set up variables
    variableGroupText = ""
    variables = []
    lines = bertiniVariablesAndConstants.splitlines()
    for i in range(len(lines)):
        variableGroupType = lines[i].split(" ")[0]
        if not (variableGroupType == "variable_group" or variableGroupType == "hom_variable_group"):
            print("Exiting because a variable group other that 'variable_group' or 'hom_variable_group' was declared.")
            # sys.exit(1)
        if variableGroupType == "hom_variable_group":
            projectiveVariableGroups.append(i)
        variableGroupText+=lines[i]+"\n"
        variables.append(lines[i][lines[i].find(" "):].replace(" ","").replace(";", "").split(","))
    bfe=[]
    for i in range(len(variables)):
        isProjectiveGroup = 0
        if i in projectiveVariableGroups:
            isProjectiveGroup = 1
        bfe.append(len(variables[i])-isProjectiveGroup)
    print("Ambient space dimension ")
    print(bfe)
    print("variables")
    print(variables)
    print("projectiveVariableGroups")
    print(projectiveVariableGroups)
    print("variableGroupText")
    print(variableGroupText)
# set up function names and revisedEquationsText
    revisedEquationsText = ""
    lines = bertiniEquations.splitlines()
    fNames=[]
    for i in range(len(lines)):
        functionLine = lines[i].split(" ")[0]
        if functionLine == "function":
            fNames += lines[i][lines[i].find(" "):].replace(" ","").replace(";", "").split(",")
        else:
            revisedEquationsText += lines[i]+"\n"
    print("G")
    print(G)
    print("revisedEquationsText")
    print(revisedEquationsText)
    exec(setVariablesToGlobal + open("inputFile.py").read())
# set degrees TODO


    #####################
# Make directory to store final solutions
    if os.path.isdir(workingDirectory):
        shutil.rmtree(workingDirectory)
    os.mkdir(workingDirectory)
    os.chdir(workingDirectory)
    os.mkdir("all_full_depth_solutions")
    os.mkdir("_truncated_singular_solutions")
    os.mkdir("_saturated_solutions")


# print to screen system summary.
    if verbose > 0:
        print("\n################### Setup multiregeneration ####################\n")
        print("These variable groups have been selected:\n"+variableGroupText)
        print("Solutions in a 'linearProduct' directory and :")
        for c, f in enumerate(fNames): # 0 is the depth we start with
            if c >= depth:
                print("depth > "+str(c)+" satisfy "+ f+" = 0")
# Determine random linear polynomials l[i][j]
    (l, startSolution) = getLinearsThroughPoint(variables)
    print(startSolution)
# Determine random linear polynomials r[i][j]
    r = []
    for i in range(len(variables)):
        r.append([])
        maxdeg= 0
        for s in range(len(fNames)):
            maxdeg= max(maxdeg,degrees[s][i])
        print("%s is the maximum degree in variable group %s. "%(maxdeg,i))
        for d in range(maxdeg):
            r[i].append(getGenericLinearInVariableGroup(i))
    if B== None:
        B=len(fNames)  # TODO: check that this is not off by one.
        print("B is set to %d" % B)
    if verbose > 0:
        print("\n################### Starting multiregeneration ####################\n")
    completedSmoothSolutions="_completed_smooth_solutions"
    os.mkdir(completedSmoothSolutions)
    for i in range(depth, depth+len(fNames)):
        os.mkdir(completedSmoothSolutions+"/depth_%s"% i)
# branch node outline
    print(depth,bfe)
    print("bfe %s" %bfe)
    outlineRegenerate(depth, G, B, bfe, startSolution)

def outlineRegenerate(depth,G,B,bfe,P):
    if len(degrees)!=len(fNames):
        print("Error: length of degree list does not coincide with the number of polynomials in the system. ")
    print("We begin: depth %s G %s B %s bfe %s P %s" %(depth,G,B,bfe,hashPoint(P)))
#    print("Degrees %s" % degrees)
    label = "unknown"
    if depth<B and depth < len(fNames):
        # determine isVanishes value.
#        print("bfe %s" %bfe)
        dirVanish = directoryNameIsVanishing(depth, P)
        M = degrees[depth]
        try:
            os.mkdir(dirVanish)
        except:
            pass
        isVanishes="unknown"
        isVanishes=isEvaluateZero(dirVanish,depth,P)
#        print(isVanishes)
        if not(isVanishes):
            print("Branch out")
            for i in range(len(bfe)):
                if bfe[i]>0:
                    bfePrime = list(bfe)
                    bfePrime[i] = bfe[i]-1
                    for j in range(M[i]):
                        label="unknown"
#                        print("We parentHomotopy at depth %s variable group %s degree %s and point %s" %(depth,i,j,hashPoint(P)))
                        dirTracking = directoryNameTracking(depth, G, bfePrime, i, j, P)
#                        print(dirTracking)
                        if not os.path.exists(dirTracking):
                                os.makedirs(dirTracking)
                        (P,label) = branchHomotopy(dirTracking, depth, G, bfePrime, i, j,M, P)
                        if label=="smooth":
                            completedSmoothSolutions = "_completed_smooth_solutions"
                            solText = "\n"
                            solName = directoryNameTrackingSolution(depth, G, bfePrime, i, j, P)
                            for line in P:
                                solText += line+"\n"
                            startFile = open(completedSmoothSolutions+"/depth_%s/%s" %(depth,solName), "w")
                            startFile.write(solText)
                            startFile.close()
                            outlineRegenerate(depth+1,G+[True],B,bfePrime,P)
                        # elif label=="singular":
                        #     print(" We prune because the endpoint is singular")
                        # elif label=="infinity":
                        #     print(" We prune because the endpoint is at infinity")
                        else:
                            print(" label is %s at directory %s" % (label,dirTracking))
                    else:
                        print("We prune at depth %s variable group %s" %(depth,i))
                        label="prune"
        elif isVanishes: # isVanishes is true
            print("We  oneEdgeHomotopy at depth %s" %depth)
            if label!="error":
                completedSmoothSolutions = "_completed_smooth_solutions"
                print("vanishes!")
                solName = directoryNameImmediateSolution(depth, P)
                solText = "\n"
                for line in P:
                    solText += line+"\n"
                print(completedSmoothSolutions+"/depth_%s/%s" %(depth,solName))
                startFile = open(completedSmoothSolutions+"/depth_%s/%s" %(depth,solName), "w")
                startFile.write(solText)
                startFile.close()
            outlineRegenerate(depth+1,G+[False],B,bfe,P)
        else:
            print("isVanishes should be True or False and not %s" %isVanishes)
    else:
        print("We reached depth %s" %depth)
#    return("success2")


def hashPoint(P):
    return(abs(hash("_".join(P))) % (10 ** 8))
#    return(random.randint(1,1000000)+abs(hash("_".join(P))) % (10 ** 8))


def isEvaluateZero(dirVanish,depth,P):
    fTarget = fNames[depth]
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
      ''' % (bertiniTrackingOptionsText, variableGroupText, revisedEquationsText, fTarget)
    inputFile = open("%s/inputEval" % dirVanish, "w")
    inputFile.write(inputText)
    inputFile.close()
# Write start file for evaluation.inputPQ
    startText = "1\n\n"
    for line in P:
        startText += line+"\n"
    startFile = open("%s/start" % dirVanish, "w")
    startFile.write(startText)
    startFile.close()
# Get current working directory to run Bertini.
    cwd = os.getcwd()
    os.chdir(dirVanish)
    # print("Try bertini inputEval..")
    try:
        bertiniCommand = "bertini inputEval"
        process = subprocess.Popen(bertiniCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        # print("..success likely")
    except:
        print("Error: could not evaulate %s using Bertini." % fTarget)
        isVanishing="error"
# Open the Bertini output file named 'function' and determine if this is zero.
    # print("Try loading bertini output file 'function'...")
    try:
        solutionsFile = open("function", "r")
        solutionsLines = solutionsFile.readlines()
        solutionsFile.close()
        # print("..success likely")
    except:
        print("Ope! Error opening file 'function'")
#    if not solutionsFile:
        print("Bertini error likely: check bertiniInput_...")
#        sys.exit(1) # the one is for error and 0 is for everyhting is fine.
        isVanishing="error"
    value = solutionsLines[2].split(' ')
    # print("Value of the function at the point: %s" % value)
    isVanishing = isZero(value[0], logTolerance) and isZero(value[1], logTolerance)
    with open("isVanishing", "w") as isVanishingFile:
      isVanishingFile.write(str(isVanishing))
    os.chdir("..")
    return(isVanishing)

#
#     if isVanishing:
#         label = "smooth"
# #        print("1. Label %s" % label)
#         nsFile = open("%s/nonsingular_solutions"%dirTracking, "w")
#         nsFile.write(startText)
#         nsFile.close()
#         P=list(point)

bertiniParameterHomotopyTwoTemplate='''
CONFIG
%s
ParameterHomotopy : 2;
END;
INPUT
%s
parameter Tpath ;
function HF;
function %s;
%s
%s
%s
HF = Tpath*(%s)+(1-Tpath)*(%s);
END;
        '''


def writePStart(P,fn):
    startText = "1\n\n"
    for line in P:
        startText += line+"\n"
    startFile = open(fn, "w")
    startFile.write(startText)
    startFile.close()
    return()

def writeParameters():
    parametersFile = open("start_parameters", "w")
    parametersFile.write("1\n1 0")
    parametersFile.close()
    parametersFile = open("final_parameters", "w")
    parametersFile.write("1\n0 0")
    parametersFile.close()
    return()




def branchHomotopy(dirTracking,depth, G, bfePrime, vg, rg, M, P):
    label="unknown"
    os.chdir(dirTracking)
    label = "Missing"
    m=M[vg]
    vg=str(vg)
    rg=str(rg)
    fTarget=fNames[depth]
    HG = []
    for i in range(len(G)): # Change to enumerate
        if G[i]:
            HG.append(fNames[i])
    for i in range(len(bfePrime)):
        for j in range(bfePrime[i]):
#            print("l_%d_%d"%(i,j))
            HG.append("l_%d_%d"%(i,j))
    ellText = "\n % ellText\n"
    for i in range(len(bfe)):
        for j in range(bfe[i]):
            # print("l_%d_%d" % (i,j))
            ellText += "l_%d_%d" % (i,j)+" = "+l[i][j]+" ; \n"
#    ellText += "l_%s_%d" % (vg, bfePrime[eval(vg)]) +" = "+l[eval(vg)][bfePrime[eval(vg)]]+" ; \n"
#    print(bfePrime,ellText)
    rText = "\n % rText\n"
    for i in range(len(bfe)):
        for j in range(M[i]):
            # print("r_%s_%s" %(i,j))
            rText += "r_%s_%s" %(i,j)+" = "+r[i][j]+" ; \n"
    # startText = "1\n\n"
    # for line in P:
    #     startText += line+"\n"
    # startFile = open("start", "w")
    # startFile.write(startText)
    # startFile.close()
    # startFile = open("P", "w") #
    # startFile.write(startText)#
    # startFile.close()#
    # write start parameters
    # startParametersFile = open("start_parameters", "w")
    # startParametersFile.write("1\n1 0")
    # startParametersFile.close()
    # # write target parameters
    # finalParametersFile = open("final_parameters", "w")
    # finalParametersFile.write("1\n0 0")
    # finalParametersFile.close()
    writePStart(P,"start")
    writePStart(P,"P")
    writeParameters()
    ## Now we do PQ
    sfPQ="l_%s_%d" %(vg,bfePrime[eval(vg)])
    tfPQ="r_%s_%s" %(vg,rg)
    inputTextPQ = bertiniParameterHomotopyTwoTemplate %(bertiniTrackingOptionsText,
                  variableGroupText,
                  ",".join(HG),
                  revisedEquationsText,
                  ellText,
                  rText,
                  sfPQ,
                  tfPQ)
    inputPQFile = open("inputPQ", "w")
    inputPQFile.write(inputTextPQ)
    inputPQFile.close()
    # print("Try to call bertini inputPQ .. ")
    # print("label %s", label)
    successPQ=False
    errorCountPQ=0
    while not(errorCountPQ>3 or (successPQ==True)):
        label="unknown"
        try:
            bertiniCommand = "bertini inputPQ"
            process = subprocess.Popen(bertiniCommand.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
        except:
            errorCountPQ=errorCountPQ+1
            print("There the command `bertini input` exited with the\
                following' error. Make sure you have bertini installed.")
            print("error (branch PQ): %s" %dirTracking)
            label = "error"
        if label != "error" and path.exists("nonsingular_solutions"):
            with open('nonsingular_solutions') as f:
            	foundQ = eval(f.readline()) # first line is number of solutions and should be one or zero.
            if foundQ==1:
                label = "foundQ"
                successPQ=True
            else:
                errorCountPQ+=1
        else:
            errorCountPQ += 1
            label="error"
            print("error (Count %d) (Branch) nonsingular_solutions does not exist in %s" %(errorCountPQ,dirTracking))
### Now we go from Q to p.
    # print("Rename")
#  write bertini-input file for Homotopy Q to P
    if label == "foundQ":
        os.rename("nonsingular_solutions", 'start')
        linearProduct = "(1)"
        for i in range(len(bfePrime)):
            for j in range(M[i]):
                linearProduct += "*(r_%s_%s)"%(str(i), str(j))
        inputTextQP = bertiniParameterHomotopyTwoTemplate % (bertiniTrackingOptionsText,
                  variableGroupText,
                  ",".join(HG),
                  revisedEquationsText,
                  ellText,
                  rText,
                  linearProduct,  #start function
                  fNames[depth])  # target function
        inputQP = open("inputQP", "w")
        inputQP.write(inputTextQP)
        inputQP.close()
        try:
            bertiniCommand = "bertini inputQP"
            process = subprocess.Popen(bertiniCommand.split(), stdout=subprocess.PIPE)  #What is going on here?
#                process = subprocess.Popen(bertiniCommand, stdout=subprocess.PIPE)  #What is going on here?
            output, errors = process.communicate()
        except:
            print("error (branch QP): %s" %dirTracking)
            label = "error"
        if label != "error" and path.exists("nonsingular_solutions"):
            with open("nonsingular_solutions") as f_in:
                P = (line.rstrip() for line in f_in)
                P = list(line for line in P if line)
            # with open('nonsingular_solutions') as f:
            #     P = f.read().splitlines(True)
#        	smoothP = eval(P[0]) # first line is number of solutions and should be one or zero.
            # print("smoothP is %s" % smoothP)
            if len(P)>1:
                label = "smooth"
                del P[:1]
#                print(len(P))
            else:
                label = "error"
        else:
            label = "error"
            print("error (Branch) nonsingular_solutions does not exist in %s or label=error" %dirTracking)
    os.chdir("..")
    #os.chdir(cwd)
    return (P, label)






#    regenerateSolving(depth, G, B, bfe, startSolution,"smooth")


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
    startSolution = []
    for i in range(len(spoint)):
        for j in range(len(spoint[i])):
            startSolution+=[spoint[i][j][0]+" "+spoint[i][j][1]]
#    print(startSolution)
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
#    for i in range(len(variables)):
#        print("\n The are %s ells in group %s .\n "% (len(ell[i]),i))
#        print("\nThis is the first linear polynomial for variable group %s.\n "% i)
#        print(ell[i][0])
    return (ell, startSolution)


# helper function to determine if a value is zero.
def isZero(s, logTolerance):
  if all([not str(i) in s for i in range(1, 10)]):
    return True
  return int(s.split("e")[1]) < logTolerance


#
# # Makes the directory for each process.
# def directoryName(depth, G, bfe, varGroup, regenLinear, homotopyKind, point):
# #    print("This is G: %s" % G)
#     useFunction = "_".join(map(lambda b: "1" if b else "0", G+[1]))
# #    print(useFunction)
#     dirName = "depth_%d_gens_%s_dim_%s_varGroup_%d_regenLinear_%d_homotopy_%s_pointId_%s"%(depth,
#         useFunction,
#         "_".join(map(str, bfe)),
#         varGroup,
#         regenLinear,
#         "all", # formerly homotopyKind. Now we keep it all in one directory
#         (abs(hash("_".join(point))) % (10 ** 8))
#         #(abs(hash(point)) % (10 ** 8))
#         )
# #    print((abs(hash(point)) % (10 ** 8)))
# #    print(abs(hash("_".join(point))) % (10 ** 8))
#     return dirName
#




def directoryNameIsVanishing(depth, P):
#    print(useFunction)
    dirName = "homotopy_vanishing_depth_%s_pointId_%s"%(depth,hashPoint(P))
    return dirName


def directoryNameImmediateSolution(depth, P):
#    print(useFunction)
    dirName = "solution_vanishing_depth_%s_pointId_%s"%(depth,hashPoint(P))
    return dirName


# Makes the directory for each process.
def directoryNameTracking(depth, G, bfe, varGroup, regenLinear, P):
#    print("This is G: %s" % G)
    useFunction = "_".join(map(lambda b: "1" if b else "0", G+[1]))
#    print(useFunction)
    dirName = "homotopy_tracking_depth_%d_gens_%s_dim_%s_varGroup_%d_regenLinear_%d_pointId_%s"%(depth,
        useFunction,
        "_".join(map(str, bfe)),
        varGroup,
        regenLinear,
        hashPoint(P)
        )
    return dirName


def directoryNameTrackingSolution(depth, G, bfe, varGroup, regenLinear, P):
#    print("This is G: %s" % G)
    useFunction = "_".join(map(lambda b: "1" if b else "0", G+[1]))
#    print(useFunction)
    dirName = "solution_tracking_depth_%d_gens_%s_dim_%s_varGroup_%d_regenLinear_%d_pointId_%s"%(depth,
        useFunction,
        "_".join(map(str, bfe)),
        varGroup,
        regenLinear,
        hashPoint(P)
        )
    return dirName



def directoryNameTracking(depth, G, bfe, varGroup, regenLinear, P):
#    print("This is G: %s" % G)
    useFunction = "_".join(map(lambda b: "1" if b else "0", G+[1]))
#    print(useFunction)
    dirName = "homotopy_tracking_depth_%d_gens_%s_dim_%s_varGroup_%d_regenLinear_%d_pointId_%s"%(depth,
        useFunction,
        "_".join(map(str, bfe)),
        varGroup,
        regenLinear,
        hashPoint(P)
        )
    return dirName

# TODO: directory to store completed solutions, singular solutions, saturated saturated solutions, etc.



#
#
# # A parent homotopy takes a point P to  pPrime
# def parentHomotopy(depth, G, bfePrime, vg, m, fNames, dirName,point):
#     vg=str(vg)
#     fTarget=fNames[depth]
#     M = list(degrees[depth])
#     # print("bfe:  %s" % bfe)
#     # print("G at start of parentHomotopy: %s " % G)
#     try:  # What is happening here?
# #        print("Try opening directory: %s" % dirName)
#         os.mkdir(dirName)
# #        print("Succesful!")
#     except:
#         print("Ope! Error opening directory during vanishes() '%s'"%dirName)
# ## Step 1. Check if point is in the next hypersurface.
#     label = "Missing"
# #    print("evaluating point at %s " % fNames[depth])
# # Write input file for evaluation.
# #    print("Vanishes function")
# #    print(bertiniTrackingOptionsText)
# #    print(variableGroupText)
# #    print(revisedEquationsText)
#     inputText = '''
# CONFIG
#   %s
#   TrackType:-4;
# END;
# INPUT
#   %s
#   function evalF;
#   %s
#   evalF = %s;
# END;
#       ''' % (bertiniTrackingOptionsText, variableGroupText, revisedEquationsText, fTarget)
#     inputFile = open("%s/inputEval"%dirName, "w")
#     inputFile.write(inputText)
#     inputFile.close()
# # Write start file for evaluation.
#     startText = "1\n\n"
#     for line in point:
#         startText += line+"\n"
#     startFile = open("%s/start"%dirName, "w")
#     startFile.write(startText)
#     startFile.close()
# # Get current working directory to run Bertini.
#     cwd = os.getcwd()
#     os.chdir(dirName)
#     # print("Try bertini inputEval..")
#     try:
#         bertiniCommand = "bertini inputEval"
#         process = subprocess.Popen(bertiniCommand.split(), stdout=subprocess.PIPE)
#         output, error = process.communicate()
#         # print("..success likely")
#     except:
#         print("Ope! could not evaulate %s using Bertini." % fTarget)
# # Open the Bertini output file named 'function' and determine if this is zero.
#     # print("Try loading bertini output file 'function'...")
#     try:
#         solutionsFile = open("function", "r")
#         solutionsLines = solutionsFile.readlines()
#         solutionsFile.close()
#         # print("..success likely")
#     except:
#         print("Ope! Error opening file 'function'")
# #    if not solutionsFile:
#         print("Bertini error likely: check bertiniInput_...")
# #        sys.exit(1) # the one is for error and 0 is for everyhting is fine.
#     value = solutionsLines[2].split(' ')
#     # print("Value of the function at the point: %s" % value)
#     isVanishing = isZero(value[0], logTolerance) and isZero(value[1], logTolerance)
#     with open("isVanishing", "w") as isVanishingFile:
#       isVanishingFile.write(str(isVanishing))
#     os.chdir(cwd)
#     # print("isVanishing is %s"  % isVanishing)
#     if isVanishing:
#         label = "smooth"
# #        print("1. Label %s" % label)
#         nsFile = open("%s/nonsingular_solutions"%dirName, "w")
#         nsFile.write(startText)
#         nsFile.close()
#         P=list(point)
#     else:
#         if max(bfePrime) < 1: # if bfe is the zero vector.
#             # print("nonsolution")
#             label = "nonsolution"
# #            print("2. Label %s" % label)
#         else:
#             ###  set up Homotopy P to Q
#             # write start parameters
#             startFile = open("%s/start_parameters"%dirName, "w")
#             startFile.write("1\n1 0")
#             startFile.close()
#         # write target parameters
#             startFile = open("%s/final_parameters"%dirName, "w")
#             startFile.write("1\n0 0")
#             startFile.close()
#         # set up system
#             # print("\n"+dirName)
#             HG = []
#             for i in range(len(G)):
#                 if G[i]:
#                     HG.append(fNames[i])
# #            print("1. HG is %s" % HG)
# #            print("1. G is %s" % G)
#             for i in range(len(bfePrime)):
#                 for j in range(bfePrime[i]):
# #                    print("l_%d_%d"%(i,j))
#                     HG.append("l_%d_%d"%(i,j))
# #            print("2. HG is %s" % HG)
# #            print("2. G is %s" % G)
#             startFunctionString="l_%s_%d" %(vg,bfePrime[eval(vg)])
#             targetFunctionString="r_%s_%d" %(vg,m)
#         #    print("before regeneratedPoint")
#             ellText = "\n % ellText\n"
#             rText = "\n % rText\n"
#             for i in range(len(bfePrime)):
#                 for j in range(bfePrime[i]):
#                     ellText += "l_%d_%d" % (i,j)+" = "+l[i][j]+" ; \n"
#                 for j in range(M[i]):
#                     rText += "r_%s_%s" %(i,j)+" = "+r[i][j]+" ; \n"
#             ellText += "l_%s_%d" % (vg, 1+bfePrime[eval(vg)]) +" = "+l[eval(vg)][1+bfePrime[eval(vg)]]+" ; \n"
#             # print(ellText)
#         #    print("rText\n"+rText)
#             # print(" HG is %s" % ",".join(HG))
#             # print("startFunctionString: %s" % startFunctionString)
#             # print("targetFunctionString %s" % targetFunctionString)
# ###  write bertini-input file for Homotopy P to Q
#             inputText = '''
# CONFIG
#     %s
#     ParameterHomotopy : 2;
# END;
# INPUT
#     %s
#     parameter Tpath ;
#     function HF;
#     function %s;
#     %s
#     %s
#     %s
#     HF = Tpath*(%s)+(1-Tpath)*(%s);
# END;
# Homotopy from P to Q
#             '''%(bertiniTrackingOptionsText,
#                   variableGroupText,
#                   ",".join(HG),
#                   revisedEquationsText,
#                   ellText,
#                   rText,
#                   startFunctionString,
#                   targetFunctionString)
# #            print("\nTry to write inputPQ")
#             inputFile = open("%s/inputPQ"%dirName, "w")
#             inputFile.write(inputText)
#             inputFile.close()
#         #  write bertini-input file for Homotopy Q to P
#             linearProduct = "(1)"
#             for i in range(len(bfePrime)):
#                 for j in range(M[i]):
#             # print("LinearProduct factor %s %s"%(i, j))
#                     linearProduct += "*(r_%s_%s)"%(str(i), str(j))
#             # print("LP %s" % linearProduct)
#             startFunctionString=linearProduct
#             targetFunctionString=fNames[depth]
#             # print("LP startFunctionString: %s" % startFunctionString)
#             # print("LP targetFunctionString %s" % targetFunctionString)
# # Step 5. now we track from Q to P.
#             inputText = '''
# CONFIG
#     %s
#     ParameterHomotopy : 2;
# END;
# INPUT
#     %s
#     parameter Tpath ;
#     function HF ;
#     function %s;
#     %s
#     %s
#     %s
#     HF = Tpath*(%s)+(1-Tpath)*(%s);
# END;
# Homotopy from Q to P.
#             '''%(bertiniTrackingOptionsText,
#                   variableGroupText,
#                   ",".join(HG),
#                   revisedEquationsText,
#                   ellText,
#                   rText,
#                   startFunctionString,
#                   targetFunctionString)
#             # print("\nTry to write inputQP")
#             inputFile = open("%s/inputQP" % dirName, "w")
#             inputFile.write(inputText)
#             inputFile.close()
#         # Change directory to call Bertini.
#             os.chdir(dirName)
#             # print("Try to call bertini inputPQ .. ")
#             try:
#                 bertiniCommand = "bertini inputPQ"
#                 process = subprocess.Popen(bertiniCommand.split(), stdout=subprocess.PIPE)
#                 output, error = process.communicate()
#                 # print("..likely successful. ")
#             except:
#                 print("There the command `bertini input` exited with the\
#                     following' error. Make sure you have bertini installed.")
#                 print(error)
#         # Check to see if there are nonsingular_solutions
# # https://stackoverflow.com/questions/1904394/read-only-the-first-line-of-a-file
#             #https://www.guru99.com/python-check-if-file-exists.html
#             # https://stackoverflow.com/questions/28737292/how-to-check-text-file-exists-and-is-not-empty-in-python
#             # print("Try to understand solutions")
#             with open('nonsingular_solutions') as f:
#             	foundQ = eval(f.readline()) # first line is number of solutions and should be one or zero.
#             if foundQ==1:
#                 solutionsFile = open("nonsingular_solutions", "r")
#                 solutionsLines = solutionsFile.readlines()
#                 solutionsFile.close()
#                 label = "foundQ"
#             else:
#                 print("Exiting because could  not find 'nonsingular_solutions'. Bertini gave the following output.\n\n")
#                 print(repr(output))
#                 sys.exit(1)  #TODO: figure out what this does.
#         ### Now we go from Q to p.
#             # print("Move nonsingular solutions to start solutions and call bertini..")
#         #  Call Bertini.
#             # print(dirName)
#             os.rename("nonsingular_solutions", 'start')
# #            print("Try to call bertini inputQP")
#             try:
#                 bertiniCommand = "bertini inputQP"
#                 process = subprocess.Popen(bertiniCommand.split(), stdout=subprocess.PIPE)  #What is going on here?
# #                process = subprocess.Popen(bertiniCommand, stdout=subprocess.PIPE)  #What is going on here?
#                 output, error = process.communicate()
#                 # print("..likely successful")
#             except:
#                 print("There the command `bertini input` exited with the\
#                     following' error. Make sure you have bertini installed.")
#                 print(error)
#         # Check to see if there are nonsingular_solutions
#             # print("Try to open nonsingular_solutions..")
#             with open('nonsingular_solutions') as f:
#                 P=f.read().splitlines(True)
#             	smoothP = eval(P[0]) # first line is number of solutions and should be one or zero.
#                 # print("smoothP is %s" % smoothP)
#                 if smoothP==1:
#                     label="smooth"
#                     del P[:2]
# #                    print(P)
#                 else:
#                     # print("..try to open singular_solutions instead..")
#                     with open('singular_solutions') as sf:
#                         P=sf.read().splitlines(True)
#             	        singularP = eval(P[0]) # first line is number of solutions and should be one or zero.
#                         # print(3)
#                         if singularP==1:
#                             label="singular"
#                             del P[:2]
#                         else:
#                             # print("..labeled as infinity.")
#                             P=[]
#                             label="infinity"
#             os.chdir("..")
#             # isVanishing = isZero(value[0], logTolerance) and isZero(value[1], logTolerance)
#             # with open("isVanishing", "w") as isVanishingFile:
#             #   isVanishingFile.write(str(isVanishing))
#             os.chdir(cwd)
#     return (isVanishing, P, label)
#
#
#

# def regenerateSolving(depth, G, B, bfe, point,label):
#     print("###### start a regenerateSolving")
#     print("bfe %s" % bfe)
#     print(depth,B,len(fNames))
#     if depth>B or depth+1>len(fNames):
#         print("complete (depth too large)")
#         # isCompleteFile = open("%s/isComplete"%dirName, "w")
#         # isCompleteFile.write("complete")
#         # isCompleteFile.close()
#         # label=label
#         # os.chdir(workingDirectory)
#         # csDir = "_completed_smooth_solutions/gens_%s_dim_%s_varGroup_%d_regenLinear_%d_pointId_%s"%(
#         #     "".join(map(lambda b: "1" if b else "0", G)),
#         #     "_".join(map(str, bfe)),
#         #     varGroup,
#         #     regenLinear,
#         #     (abs(hash(point)) % (10 ** 8)))
#     else:
#         print("Going to track...")
#         fTarget = fNames[depth]
#         M = list(degrees[depth])
#         for i in range(len(M)):
#             print("Prior to inner loop: depth %s , bfe %s, vg %s" % (depth,bfe,i))
#             if bfe[i]>0:
#                 for j in range(M[i]):
#                     P = list(point)
#                     print("Prior parent: depth %s , bfe %s, vg %s, degree %s" % (depth,bfe,i,j))
# # parallel
#                     # child_pid = os.fork()
#                     # print("child_pid")
#                     # print(child_pid)
#                     # if child_pid == 0:
#                     #     bfePrime=bfe
#                     #     bfePrime[i]=bfePrime[i]-1
#                     #     print(fNames,depth,bfePrime,i,j)
#                     #     P = point
#                     #     #TODO: remove the reduant argument in directory name
#                     #     print("bfePrime %s " % bfePrime)
#                     #     dirName = directoryName(depth, G, bfePrime, i, j, "delete", P)
#                     #     print("directory name before parentHomotopy %s" %dirName)
#                     #     print("G before parentHomotopy %s" %G)
#                     #     print(depth, G, bfePrime, i, j, fNames[depth], dirName, P)
#                     #     (isVanishing,P,label) = parentHomotopy(depth, G, bfePrime, i, j, fNames, dirName, P)
#                     #     print("  #####    leaving to start another")
#                     #     if depth< len(fNames) and depth < B:
#                     #         regenerateSolving(depth+1,G+[not(isVanishing)],B,bfePrime,P,label)
# # end parallel part
# # serial
#                     #TODO: remove the reduant argument in directory name
#                     bfePrime = list(bfe)
#                     print(bfe)
#                     bfePrime[i]=bfePrime[i]-1
#                     print(bfe,bfePrime)
#                     dirName = directoryName(depth, G, bfePrime, i, j, "delete", P)
# #                    print("directory name before parentHomotopy %s" %dirName)
# #                    print("G before parentHomotopy %s" %G)
# #                    print(depth, G, bfePrime, i, j, fNames[depth], dirName, P)
#                     (isVanishing,P,label) = parentHomotopy(depth, G, bfePrime, i, j, fNames, dirName, P)
#                     if label=="smooth":
# #                        os.mkdir("_completed_smooth_solutions/depth_%s"% i)
#                         startText = "1\n\n"
#                         for line in P:
#                             startText += line+"\n"
#                         startFile = open("_completed_smooth_solutions/depth_%s/%s" %(depth,dirName), "w")
#                         startFile.write(startText)
#                         startFile.close()
#                     print("  #####    leaving to start another % s" %bfePrime)
#                     if depth< len(fNames) and depth < B:
#                         print("depth is small %s" % depth)
#                         regenerateSolving(depth+1, list(G)+[not(isVanishing)], B, bfePrime, P, label)
#             else:
#                 print("bfe %s is too small in variable group %s" %(bfe,i))
# end serial part
        #   sys.exit(0)




if __name__== "__main__":
  main()
