#TODO: Think about the hypothesis that would
# ensure the following: if a point gets thrown out along the way,
# then that point

# Caveat: Bertini input file style assumptions
# # 'variable group ...;' is one line
# # 'hom_variable group ...;' is one line
# # function ...;  is one line
# # Lines after the second CONFIG not defining an equation or constant value
# # must begin with 'function', 'constant', 'hom_variable_group', or 'variable_group'


import traceback
import shutil
import sys
import subprocess
import hashlib
import os
import random
import os.path
import multiprocessing as mp
from multiprocessing.sharedctypes import Value
from os import path
from Queue import PriorityQueue
# pip install networkx
#import networkx as nx # TODO
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
projectiveVariableGroups = []  # This can be specified in the inputFile # We don't need this nay more right?
algebraicTorusVariableGroups = []
nonzeroCoordinates = []
#randomNumberGenerator = random.random
def randomNumberGenerator():
    rho = random.uniform(-1,1)
    return rho
# TODO: Restart mode.
depth = 0  # Begin the computation at a different depth index
bfe = []
verbose = 0  # Integer that is larger if we want to print more
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
realDimensionLinears = False
targetDimensions = None

explorationOrder = "breadthFirst"

loadDimensionLinearsAndStartSolution = False
loadDegreeLinears = False

dimGroupAction = None
def dimGroupAction(bfePrime):
    return(False)

pointGroupAction = None
def pointGroupAction(bfePrime,i,PPi):
    return([PPi])

symmetric = False

pool = None
jobsInPool = Value('i', 0)
maxProcesses = mp.cpu_count()
queue = None

def decJobsInPool(out):
  global jobsInPool
  with jobsInPool.get_lock():
      if verbose > 1:
        print("attempting to decrement currentProcesse =",
            jobsInPool.value)
      jobsInPool.value-=1
      if verbose > 1:
        print("new vaule is jobsInPool = ", jobsInPool.value)

def main():
    # Set global configuration variables in the inputFile
    global variables
    global depth
    global bfe # bold font e
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
    global algebraicTorusVariableGroups
    global nonzeroCoordinates
    global bertiniVariableGroupString


    global useBertiniInputStyle
    global bertiniVariablesAndConstants
    global bertiniFunctionNames
    global revisedEquationsText
    global variableGroupText
    global bertiniTrackingOptionsText

    global maxProcesses

    global explorationOrder

    global targetDimensions # a list of multidimensions
    global realDimensionLinears

    global loadDimensionLinearsAndStartSolution
    global loadDegreeLinears
    global dimGroupAction
    global pointGroupAction

    global symmetric
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
global algebraicTorusVariableGroups
global nonzeroCoordinates
global useBertiniInputStyle
global maxProcesses
global realDimensionLinears
global targetDimensions
global explorationOrder
global symmetric
global loadDimensionLinearsAndStartSolution
global loadDegreeLinears
global dimGroupAction
global pointGroupAction
"""
# exec(setVariablesToGlobal + open("inputFile.py").read())
# Our input will consist of four text files and a main input file.
# bertiniInput_variables
# bertiniInput_trackingOptions
# bertiniInput_equations
    try:
        with open("bertiniInput_variables", "r") as f:
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
        print("\t" + "bertiniInput_variables")
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
    if verbose > 1:
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
    if verbose > 1:
        print("G")
        print(G)
        print("revisedEquationsText")
        print(revisedEquationsText)

    exec(setVariablesToGlobal + open("inputFile.py").read())
# set degrees TODO


# print to screen system summary.
    if verbose > 0:
        print("\n################### Setup multiregeneration ####################\n")
        print("These variable groups have been selected:\n"+variableGroupText)
        print("Solutions in a 'linearProduct' directory and :")
        for c, f in enumerate(fNames): # 0 is the depth we start with
            if c >= depth:
                print("depth > "+str(c)+" satisfy "+ f+" = 0")
# Determine random linear polynomials l[i][j] and start solution
    if loadDimensionLinearsAndStartSolution:
        l = []
        for i in range(len(variables)):
            with open("dimensionLinears_%s" %i, "r") as f:
                A = (line.rstrip() for line in f)
                A = list(line for line in A if line)
            l.append(A)
        with open("startSolution", "r") as f:
            startSolution = (line.rstrip() for line in f)
            startSolution = list(line for line in startSolution if line)
    elif realDimensionLinears:
        (l, startSolution) = getRealValuedLinearsThroughPoint(variables)
    else:
        (l, startSolution) = getLinearsThroughPoint(variables)
    if verbose > 0:
        print("\nUsing start solution")
        for i in startSolution:
            print(i)
        print("\nUsing dimesion linears")
        for i in range(len(variables)):
            for j in range(len(l[i])):
                print("l[%s][%s]"%(i,j))
                print(l[i][j])
    # Determine random linear polynomials r[i][j] degree linears
    r = []
    if not loadDegreeLinears:
        for i in range(len(variables)):
            r.append([])
            maxdeg= 0
            for s in range(len(fNames)):
                maxdeg= max(maxdeg,degrees[s][i])
            print("%s is the maximum degree in variable group %s. "%(maxdeg,i))
            print(getGenericLinearInVariableGroup(i))
            for d in range(maxdeg):
                r[i].append(getGenericLinearInVariableGroup(i))
    elif loadDegreeLinears:
        #TODO: check that the degrees, types, and number of variables match
        # across all variable groups.
        for i in range(len(variables)):
            maxdeg= 0
            for s in range(len(fNames)):
                maxdeg= max(maxdeg,degrees[s][i])
            print("%s is the maximum degree in variable group %s. "%(maxdeg,i))
            with open("degreeLinears_%s" %i, "r") as f:
                A = (line.rstrip() for line in f)
                A = list(line for line in A if line)
            r.append(A)
    if verbose > 0:
        print("Using degree linears")
    for i in range(len(variables)):
        for j in range(len(r[i])):
            print("r[%s][%s]"%(i,j))
            print(r[i][j])
    if B== None:
        B=len(fNames)  # TODO: check that this is not off by one.
        print("B is set to %d" % B)
    if verbose > 0:
        print("exploring tree in order", explorationOrder)
        #    return(random.randint(1,1000000)+abs(hash("_".join(P))) % (10 ** 8))

    if verbose > 0:
        print("\n################### Starting multiregeneration ####################\n")
    #####################
# Make directory to store final solutions
    if os.path.isdir(workingDirectory):
        shutil.rmtree(workingDirectory)
    os.makedirs(workingDirectory)
    os.chdir(workingDirectory)
    os.makedirs("all_full_depth_solutions")
    os.makedirs("_truncated_singular_solutions")
    os.makedirs("_saturated_solutions")
    completedSmoothSolutions="_completed_smooth_solutions"
    os.makedirs(completedSmoothSolutions)
    for i in range(depth, depth+len(fNames)):
        os.makedirs(completedSmoothSolutions+"/depth_%s"% i)
# branch node outline

    global queue
    queue = mp.Manager().Queue() # a messege queue for the child
    #processes to comunication with this one
    priorityQueue = PriorityQueue() # where this process, which is the
    #queue manager, stores the jobs that need to be done

    priorityQueue.put((0,[depth, G, B, bfe, startSolution]))

    pool = mp.Pool(maxProcesses)

    with jobsInPool.get_lock():
      jobsInPool.value = 0

    #This loop looks for messeges from the child processes in the queue,
    # then puts them in the priority queue. When there is space for more
    # jobs, explore nodes in the priority queue.
    while True:
        if priorityQueue.empty() and queue.empty() and jobsInPool.value is 0:
            break
        if not queue.empty():
            job = queue.get()
            if explorationOrder is "breadthFirst":
                priority = job[0]
                priorityQueue.put((priority,job)) #depth is first in tuple, will process lower depth jobs first
            elif explorationOrder is "depthFirst":
                priority = -1*job[0]
                priorityQueue.put((priority,job))
            else:
                print("Error: explorationOrder should be 'breadthFirst' or 'depthFirst', not '%s'"%explorationOrder)
                sys.exit(1)
        if not priorityQueue.empty() and jobsInPool.value < maxProcesses:
            with jobsInPool.get_lock():
                if verbose > 1:
                  print("queue size =", queue.qsize(), "priorityQueue size",
                      priorityQueue.qsize(), "jobsInPool =",
                      jobsInPool.value)
                jobsInPool.value+=1
                args = priorityQueue.get()[1]
                if verbose > 1:
                  print("dequeued node", args)
                pool.apply_async(processNode, (args,), callback=decJobsInPool)
                if verbose > 1:
                  print("queue size =", queue.qsize(), "priorityQueue size",
                      priorityQueue.qsize(), "jobsInPool =",
                      jobsInPool.value)

    pool.close()
    print("Done.")


def processNode(args): # a wrapper funcion to catch error. This is
#                           stupid, but it's a way to see when there is
#                           an error in one of the child processes.
  try:
    outlineRegenerate(args[0], args[1], args[2], args[3], args[4])
  except Exception as e:
    print("There was an error in a child process.")
    print(e)
    print(traceback.format_exc())

def outlineRegenerate(depth,G,B,bfe,P):
    if len(degrees)!=len(fNames):
        print("Error: length of degree list does not coincide with the number of polynomials in the system. ")

    label = "unknown"
    # if depth isn't too large then
    if depth < B and depth < len(fNames):
        # # (1) we create a directory to test if the next polynomial vanishes at point P.
        dirVanish = directoryNameIsVanishing(depth, P)
        M = degrees[depth]
        try:
            os.makedirs(dirVanish)
        except:
            pass
        if verbose > 1:
          print("directory before isEvaluateZero is", os.getcwd())
        isVanishes="unknown"
        # # (2) evaluate the next polynomial at the point P to to determine isVanishes (Boolean)
        isVanishes=isEvaluateZero(dirVanish,depth,P)
        if verbose > 1:
          print("directory after isEvaluateZero is", os.getcwd())
        # # (3) if the next polynomial does not vanish at P then we need to branch with edges with weight one.
        if not(isVanishes):
            startHash=hashPoint(P)
            if verbose > 1:
              print("Branch out")
            for i in range(len(bfe)):
                bfePrime = list(bfe)
                bfePrime[i] = bfe[i]-1
                prune = bfe[i] is 0
                if targetDimensions:
                    canReach = []
                    for dim in targetDimensions:
                        b1 = all(dim[i] <= bfePrime[i] for i in range(len(dim)))
                        b2 = sum(bfePrime) - sum(dim) <= len(fNames)-depth
                        canReach.append(b1 and b2)
                    prune = not any(canReach)
                # dimGroupAction returns False as the default.
                # Redfine this function in inputFile.py as you like.
                if not prune:
                    prune = dimGroupAction(bfePrime)
                if not prune:
                    for j in range(M[i]):
                        label="unknown"
#                        print("We parentHomotopy at depth %s variable group %s degree %s and point %s" %(depth,i,j,hashPoint(P)))
                        dirTracking = directoryNameTracking(depth, G, bfePrime, i, j, P)
#                        print(dirTracking)
                        if not os.path.exists(dirTracking):
                                os.makedirs(dirTracking)
                        if verbose > 1:
                          print("directory before branchHomotopy is", os.getcwd())
                        (PPrime,label) = branchHomotopy(dirTracking, depth, G, bfePrime,bfe, i, j, M, P)
                        if verbose > 1:
                          print("directory after branchHomotopy is", os.getcwd())
                        # TODO: Check if this agrees with our vision of what the code should do.
                        count = 0
                        if len(algebraicTorusVariableGroups)>0 and len(PPrime)>0: # Prune if not in the algebraic torus based on algebraicTorusVariableGroups
                            for a in range(len(variables)):
                                for b in range(len(variables[a])):
                                    if (a in algebraicTorusVariableGroups):
#                                        print(count)
#                                        print(PPrime[count])
                                        if coordinateLineIsZero(PPrime[count], logTolerance): # What should the logTolerance be here?
                                            label="prune"
                                    count = count +1;
                        # Check if coordinates are nonzero
                        count = 0
                        if len(nonzeroCoordinates)>0 and len(PPrime)>0: # Prune if not in the algebraic torus based on algebraicTorusVariableGroups
                            for i in range(len(variables)):
                                for j in range(len(variables[i])):
                                    if (count in nonzeroCoordinates):
                                        if coordinateLineIsZero(PPrime[count], logTolerance): # What should the logTolerance be here?
                                            label="prune"
                                    count = count +1;
                        if label=="smooth" and len(PPrime)>1:
                            completedSmoothSolutions = "_completed_smooth_solutions"
                            # TODO: have a group action to find additional solutions
                            PPi=[]
                            for i in range(len(variables)):
                                ppGroup = []
                                for j in range(len(variables[i])):
                                    ppGroup.append(PPrime[count])
                                    count = count +1;
                                PPi.append(ppGroup)
                            #print("PPi")
                            #print(PPi)
                            LP = pointGroupAction(bfePrime,i,PPi)
                            for PPi in LP:
                                #print("ppi2")
                                #print(PPi)
                                PPrime = []
                                for i in range(len(PPi)):
                                    for j in range(len(PPi[i])):
                                        PPrime.append(PPi[i][j])
                                #print(PPrime)
                                #print(len(PPrime))
                                solText = "\n"
                                for line in PPrime:
                                    solText += line+"\n"
                                solName = directoryNameTrackingSolution(depth, G, bfePrime, i, j, PPrime, startHash)
                                try:
                                  startFile = open(completedSmoothSolutions+"/depth_%s/%s" %(depth,solName), "w")
                                  startFile.write(solText)
                                  startFile.close()
                                  if verbose > 1:
                                    print("wrote file",
                                        completedSmoothSolutions+"/depth_%s/%s"
                                        %(depth,solName),
                                        "at node",
                                        [depth,G,B,bfe,P])
                                except:
                                  print("error writing file",
                                      completedSmoothSolutions+"/depth_%s/%s"
                                      %(depth,solName))
                                if verbose > 1:
                                  print("queueing node",
                                      [depth+1,G+[True],B,bfePrime,PPrime])
                                queue.put([depth+1,G+[True],B,bfePrime,PPrime])
                        # elif label=="singular":
                        #     print(" We prune because the endpoint is singular")
                        # elif label=="infinity":
                        #     print(" We prune because the endpoint is at infinity")
                        else:
                          if verbose > 1:
                            print(" label is %s at directory %s" % (label,dirTracking))
                else:
                  if verbose > 1:
                    print("We prune at depth %s variable group %s" %(depth,i))
                  label="prune"
        # # (4) if the next polynomial vanishes at P then we need to branch with edges with weight zero.
        elif isVanishes: # isVanishes is true
            if label!="error":
                completedSmoothSolutions = "_completed_smooth_solutions"
                if verbose > 1:
                  print("vanishes!")
                solName = directoryNameImmediateSolution(depth, G, bfe, P)
                solText = "\n"
                for line in P:
                    solText += line+"\n"
                if verbose > 1:
                  print(completedSmoothSolutions+"/depth_%s/%s" %(depth,solName))
                try:
                  startFile = open(completedSmoothSolutions+"/depth_%s/%s" %(depth,solName), "w")
                  startFile.write(solText)
                  startFile.close()
                  if verbose > 1:
                    print("wrote file", completedSmoothSolutions+"/depth_%s/%s"
                        %(depth,solName))
                except:
                  print("error writing file",
                      completedSmoothSolutions+"/depth_%s/%s"
                      %(depth,solName))
            if verbose > 1:
                print("queueing node", [depth+1,G+[False],B,bfe,P])
            queue.put([depth+1,G+[False],B,bfe,P])
        else:
          if verbose > 1:
              print("isVanishes should be True or False and not %s" %isVanishes)
    else:
      if verbose > 1:
          print("We reached depth %s" %depth)
#    return("success2")


def hashPoint(P):
    return(abs(hash("_".join(P))) % (10 ** 12))
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
    os.chdir(cwd)
    return(isVanishing)


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




def branchHomotopy(dirTracking,depth, G, bfePrime,bfe, vg, rg, M, P):
    if verbose > 1:
      print("function 'branchHomotopy' starting in directory",
          os.getcwd())
    label="unknown"
    cwd = os.getcwd()
    if verbose > 1:
      print("changing to directory", dirTracking)
    os.chdir(dirTracking)
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
            HG.append("l_%d_%d"%(i,j))
    ellText = "\n % ellText\n"
    for i in range(len(bfe)):
        for j in range(bfe[i]):
            ellText += "l_%d_%d" % (i,j)+" = "+l[i][j]+" ; \n"
    # print(bfe,ellText)
#    ellText += "l_%s_%dl_" % (vg, bfePrime[eval(vg)]) +" = "+l[eval(vg)][bfePrime[eval(vg)]]+" ; \n"
    rText = "\n % rText\n"
    for i in range(len(bfe)):
        for j in range(M[i]):
            rText += "r_%s_%s" %(i,j)+" = "+r[i][j]+" ; \n"
    if len(P)<2:
        print(" ##### error %s" %dirTracking)
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
    successPQ=False
    errorCountPQ=0
    foundQ =0
    while not(errorCountPQ>1 or (successPQ==True)): # We give Bertini one chance to find Q.
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
            print(errorCountPQ)
            print(label)
            label="error"
            print(bfe,bfePrime,i)
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
                PPrime = (line.rstrip() for line in f_in)
                PPrime = list(line for line in PPrime if line)
            # with open('nonsingular_solutions') as f:
            #     P = f.read().splitlines(True)
#        	smoothP = eval(P[0]) # first line is number of solutions and should be one or zero.
            # print("smoothP is %s" % smoothP)
            if len(PPrime)>1:
                label = "smooth"
                if verbose > 1:
                  print(len(PPrime))
                del PPrime[:1]
            else:
                PPrime=[]
                if verbose > 1:
                  print(PPrime)
                label = "error"
        else:
            label = "error"
            PPrime =[]
            print("error (Branch) nonsingular_solutions does not exist in %s or label=error" %dirTracking)
    else:
        if verbose > 1:
          print(" could not find Q.")
        PPrime =[]
        label="error"
    if len(PPrime)>1:
        if verbose > 1:
          print(dirTracking)
          print("Node (Depth %d, dim %s, vg %s, deg %s, point %s)--\n--Node (Depth %d, dim %s, vg %s, deg %s. point %s)" %
            (depth, bfe, str(vg), str(rg), str(hashPoint(P)),
            depth, bfePrime, str(vg), str(rg), str(hashPoint(PPrime))
            ))
    if verbose > 1:
      print("changing back to", cwd)
    os.chdir(cwd)
    return (PPrime, label)





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

# used for the symmetric case, where the coefficients need to be the same
# accross variable groups. Takes a list of coefficients as input.
def getSymGenericLinearInVariableGroup(variableGroup, coefficients):
    terms = []
    seed = 0
    if variableGroup in projectiveVariableGroups and len(coefficients) < 2*len(variables[variableGroup]):
        print("Error: not enough coefficients given")
        sys.exit(0)
    elif variableGroup not in projectiveVariableGroups and len(coefficients) < 2*len(variables[variableGroup])+2:
        print("Error: not enough coefficients given")
        sys.exit(0)
    for var in variables[variableGroup]:
        terms.append("(%s + I*%s)*%s"%(coefficients[seed], coefficients[seed+1], var))
        seed += 2
    if not variableGroup in projectiveVariableGroups:
      terms.append("(%s + I*%s)"%(coefficients[seed], coefficients[seed+1]))
      seed+=2
    return "+".join(terms)

# used to get generic linears (B)
def getLinearsThroughPoint(variables):
    spoint = []
    for i in range(len(variables)):
        spoint += [[]]
        for j in range(len(variables[i])):
            spoint[i]+=[[str(randomNumberGenerator()),str(randomNumberGenerator())]]
    startSolution = []
    for i in range(len(spoint)):
        for j in range(len(spoint[i])):
            startSolution+=[spoint[i][j][0]+" "+spoint[i][j][1]]
    ell = []
    for i in range(len(variables)):
        ell.append([])
        isAffGroup=1
        if i in projectiveVariableGroups:
            isAffGroup = 0
        terms = [None for x in range(len(variables[i])+isAffGroup-1)]
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
            linearString = "+".join(terms)
            ell[i].append(linearString)
    return (ell, startSolution)

def getRealValuedLinearsThroughPoint(variables):
    spoint = []
    for i in range(len(variables)):
        spoint += [[]]
        for j in range(len(variables[i])):
            spoint[i]+=[[str(randomNumberGenerator()),str(0.0)]]
    startSolution = []
    for i in range(len(spoint)):
        for j in range(len(spoint[i])):
            startSolution+=[spoint[i][j][0]+" "+spoint[i][j][1]]
    ell = []
    for i in range(len(variables)):
        ell.append([])
        isAffGroup=1
        if i in projectiveVariableGroups:
            isAffGroup = 0
        terms = [None for x in range(len(variables[i])+isAffGroup-1)]
        for j in range(len(variables[i])+isAffGroup-1):
            linearString=""
            for x in range(len(variables[i])+isAffGroup-1):
                if isAffGroup:
                    terms[x]="(%s)*(%s-(%s))"%(
                        str(randomNumberGenerator()),
                        str(variables[i][x]),
                        spoint[i][x][0]
                        )
                else:
                    terms[x]="(%s)*((%s)*%s-(%s)*%s)"%(
                        str(randomNumberGenerator()),
                        str(spoint[i][-1][0]), #real  part of last coordinate of spoint
                        str(variables[i][x]), # a variable in group i
                        str(spoint[i][x][0]),
                        str(variables[i][-1])) # last variable in group i
            linearString = "+".join(terms)
            ell[i].append(linearString)
    return (ell, startSolution)



def getLinearsThroughSymmetricPoint(variables):
    spoint = [[]]
    for j in range(len(variables[0])):
        spoint[0]+=[[str(randomNumberGenerator()),str(randomNumberGenerator())]]
    for i in range(1, len(variables)):
        spoint += [[]]
        for j in range(len(variables[i])):
            spoint[i]+=[[spoint[0][j][0],spoint[0][j][1]]]
    startSolution = []
    for i in range(len(spoint)):
        for j in range(len(spoint[i])):
            startSolution+=[spoint[i][j][0]+" "+spoint[i][j][1]]
    ell = []
    for i in range(len(variables)):
        ell.append([])
        isAffGroup=1
        if i in projectiveVariableGroups:
            isAffGroup = 0
        terms = [None for x in range(len(variables[i])+isAffGroup-1)]
        for j in range(len(variables[i])+isAffGroup-1):
            linearString=""
            coefficients = []
            coefficients.append([str(randomNumberGenerator()), str(randomNumberGenerator())])
            for x in range(1, len(variables[i])+isAffGroup-1):
                coefficients.append([coefficients[0][0], coefficients[0][1]])

            for x in range(len(variables[i])+isAffGroup-1):
                if isAffGroup:
                    terms[x]="(%s+I*%s)*(%s-(%s+I*%s))"%(
                        coefficients[x][0],
                        coefficients[x][1],
                        str(variables[i][x]),
                        spoint[i][x][0],
                        spoint[i][x][1],
                        )
                else:
                    terms[x]="(%s+I*%s)*((%s+I*%s)*%s-(%s+I*%s)*%s)"%(
                        coefficients[x][0],
                        coefficients[x][1],
                        str(spoint[i][-1][0]), #real  part of last coordinate of spoint
                        str(spoint[i][-1][1]),  # imaginary part of last coordinate of spoint
                        str(variables[i][x]), # a variable in group i
                        str(spoint[i][x][0]),
                        str(spoint[i][x][1]),
                        str(variables[i][-1])) # last variable in group i
            linearString = "+".join(terms)
            ell[i].append(linearString)
    return (ell, startSolution)

def nonDecreasing(l):
    return all(l[i] <= l[i+1] for i in range(len(l)-1))
def firstIsMin(l):
    return l[0] == min(l)
# helper function to determine if a value is zero.
def isZero(s, logTolerance):
  if all([not str(i) in s for i in range(1, 10)]):
    return True
  return int(s.split("e")[1]) < logTolerance

def coordinateLineIsZero(s,logTolerance):
    value = s.split(' ')
    return(isZero(value[0], logTolerance) and isZero(value[1], logTolerance))


def directoryNameIsVanishing(depth, P):
#    print(useFunction)
    dirName = "homotopy_vanishing/depth_%s/pointId_%s"%(depth,hashPoint(P))
    return dirName

#
# def directoryNameImmediateSolution(depth, P):
# #    print(useFunction)
#     dirName = "solution_vanishing_depth_%s_pointId_%s"%(depth,hashPoint(P))
#     return dirName


def directoryNameImmediateSolution(depth, G, bfe, P):
    useFunction = "_".join(map(lambda b: "1" if b else "0", G+[0]))
    hashP=hashPoint(P)
    dirName = "solution_vanishing_depth_%d_gens_%s_dim_%s_pointId_%s_%s"%(depth,
        useFunction,
        "_".join(map(str, bfe)),
        hashP,
        hashP
        )
    return dirName

# Makes the directory for each process.
def directoryNameTracking(depth, G, bfe, varGroup, regenLinear, P):
#    print("This is G: %s" % G)
    useFunction = "_".join(map(lambda b: "1" if b else "0", G+[1]))
#    print(useFunction)
    dirName = "homotopy_tracking/depth_%d/gens_%s/dim_%s/varGroup_%d/regenLinear_%d/pointId_%s"%(depth,
        useFunction,
        "_".join(map(str, bfe)),
        varGroup,
        regenLinear,
        hashPoint(P)
        )
    return dirName


def directoryNameTrackingSolution(depth, G, bfe, varGroup, regenLinear, P, startHash):
#    print("This is G: %s" % G)
    useFunction = "_".join(map(lambda b: "1" if b else "0", G+[1]))
#    print(useFunction)
    dirName = "solution_tracking_depth_%d_gens_%s_dim_%s_varGroup_%d_regenLinear_%d_pointId_%s_%s"%(depth,
        useFunction,
        "_".join(map(str, bfe)),
        varGroup,
        regenLinear,
        startHash,
        hashPoint(P)
        )
    return dirName



def directoryNameTracking(depth, G, bfe, varGroup, regenLinear, P):
#    print("This is G: %s" % G)
    useFunction = "_".join(map(lambda b: "1" if b else "0", G+[1]))
#    print(useFunction)
    dirName = "homotopy_tracking/depth_%d/gens_%s/dim_%s/varGroup_%d/regenLinear_%d/pointId_%s"%(depth,
        useFunction,
        "_".join(map(str, bfe)),
        varGroup,
        regenLinear,
        hashPoint(P)
        )
    return dirName

# TODO: directory to store completed solutions, singular solutions, saturated saturated solutions, etc.


if __name__== "__main__":
  main()
