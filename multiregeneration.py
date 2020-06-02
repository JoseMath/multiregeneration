#For exiting on errors, and printing the progress graphic
import sys

#For formatting and printing Bertini exceptions
import traceback

#For sleeping the process which updates the progress graphic
import time

#For counting solutions when generating the progress graphic
from collections import Counter

#For deleting directories
import shutil

#For starting a subprocess which runs bertini
import subprocess

#For generating "pointIDs" to append to filenames
import hashlib

#For basic file manipulation
import os

#For generating random linear equations
import random

#For managing a pool of processes which track paths
import multiprocessing as mp
from multiprocessing.sharedctypes import Value

#For managing the order in which edges are explored
from queue import PriorityQueue


### Configuration ###
# Optional inputs # This can be specified in the inputFile

projectiveVariableGroups = []

# Example: [0,2] sets the implementation to disregard solutions
# with a zero as a coordinate in the 0th or 2nd variable group.
algebraicTorusVariableGroups = []


#Example: [0,3] sets the implementation to disregard
#solutions with a zero in the 0th or 3rd coordinate.
nonzeroCoordinates = []

# All random comlex numbers that we generate
# have real and imaginary part uniform random in
# (-1, 1)
def randomNumberGenerator():
    rho = random.uniform(-1,1)
    return rho

# Begin the computation at a different depth index
depth = 0

# This will be initialized to a list of integers
# representing the multidimension of the ambient
# product of projective space.
bfe = []

# Integer that is larger if we want to print more
# information to be printed
verbose = 0
# Level 0 for nothing except errors
# Level 1 messages we would usually like printed
# Level 2 for debugging


#The following variable will be initialized to the following values:

# A list of "variable groups", where each variable group is a list of
# variable names
variables = None

# A list of names for the given polynomial functions, to be used by
# Bertini. E.g. ["f1","f2"]
fNames = None

# A 2D list such that degrees[s][i] is the degree of the s'th function
# in the i'th variable group
degrees = None

# A list of booleans which determine if the i'th equation is used # JIR: sentence incomplete
G = []

# A 2D list of random linear equations, where l[i][j] has variables in
# group i
l = None

# A 2D list of random linear equations, where r[i][a] has variables in
# group i
r = None

# An integer, such that only the first B equations are used #JIR: Sentence incomplete
B= None

# A solution to the equations contained in l # JIR: But l is None
startSolution = None

# The subdirectory where the data of the computation will be stored
workingDirectory = "run"

# Any number with absolute value less than 10^logTolerance is considered to be zero
logTolerance = -10

# Initialized to the contents of bertiniInput_trackingOptions
# and passed to each bertini call
bertiniTrackingOptionsText = ""

# Initialized to the contents of bertiniInput_variables
# and used to set up the variable groups
bertiniVariables = None

# Initialized to the contents of bertiniInput_equations
bertiniEquations = None

# Initialized to the defining equations of the functions
# in bertiniInput_equation (i.e. does not include the declarations
# of functions.
revisedEquationsText = None

# Passed as the variable groups in each bertini call
variableGroupText = None

# Initialized by user to a list of relevant multidimensions
targetDimensions = None

# Can be changed by user to "breadthFirst"
explorationOrder = "depthFirst"

# Can be changed by user to True, and then
# the variables 'startSolutions' and 'l' are
# set by the user
loadDimensionLinearsAndStartSolution = False

# Can be changed by user to True, and then
# the variable 'r' is set by the user
loadDegreeLinears = False

def pruneByDimension(bfePrime):
    return(False)

# Define a function that returns true if a point should be 'thrown 
# away'. The coordinates of the point are stored in a 2D list of strings 
# PPi.

# For example:
# Say there is one homogeneous variable group, and you would like to 
# throw a point away if it's second or third coordinate is zero. (This 
# could also be accomplished via 'nonzeroCoordinate')

# def pruneByPoint(bfePrime, i, PPi):
#     # The complex coordinates (in variable group 0) of the point PPi
#     coordinates = \
#         [complex(s.replace(" -","-").replace(" ", "+") +"j") for \
#         s in PPi[0]]

#     # If either x_1=0 or x_2=0 is satisfied to within a 
#     # tolerance of 1e-16, then the point will lie on the 'extra' 
#     # component, and should be pruned.

#     if abs(coordinates[1]) < 1e-16  or \
#             abs(coordinates[2]) < 1e-16:
#       return True
#     else:
#       return False

def pruneByPoint(bfePrime,i,PPi):
    return False

# We use the 'multiprocessing' python module. There is
# a pool of processes of size maxProcesses, each of which
# removes jobs from 'queue', does them, and then adds any resulting new 
# jobs to the queue as well. The variable 'jobsInPool' keeps track of 
# how many jobs are in 'queue' so that multiregeneration.py knows when 
# the algorithm has terminated.
pool = None
jobsInPool = Value('i', 0)
maxProcesses = mp.cpu_count()
queue = None

# Safely decrements the variable 'jobsInPool', which is shared amoung 
# multiple processes.
def decJobsInPool(out):
  global jobsInPool
  with jobsInPool.get_lock():
      if verbose > 1:
        print("attempting to decrement currentProcesse =",
            jobsInPool.value)
      jobsInPool.value-=1
      if verbose > 1:
        print("new value is jobsInPool = ", jobsInPool.value)

def main():

    # We make these variables global so that inputFile.py can set them.
    # After this they are never modified.
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

    # See the initialization above for an example of how to use this 
    # variable
    global algebraicTorusVariableGroups

    global bertiniVariableGroupString


    global bertiniVariables
    global revisedEquationsText
    global variableGroupText
    global bertiniTrackingOptionsText

    global maxProcesses

    global explorationOrder

    global targetDimensions # a list of multidimensions

    global loadDimensionLinearsAndStartSolution
    global loadDegreeLinears
    global pruneByDimension
    global pruneByPoint

    # We read in the users configuration by evaluating the following 
    # string appended with the file 'inputFile.py'. 
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
global maxProcesses
global targetDimensions
global explorationOrder
global loadDimensionLinearsAndStartSolution
global loadDegreeLinears
global pruneByDimension
global pruneByPoint
"""
    # Read in the user's input frim the files 'bertiniInput_*'
    try:
        with open("bertiniInput_variables", "r") as f:
            bertiniVariables = f.read().strip()
        if os.path.exists("bertiniInput_trackingOptions"):
            with open("bertiniInput_trackingOptions", "r") as f:
                bertiniTrackingOptionsText = f.read().strip()
        else:
            bertiniInput_trackingOptions = ""
        with open("bertiniInput_equations", "r") as f:
            bertiniEquations = f.read().strip()
    # If anything goes wrong with reading in this input, then exit
    except:
        print("Exiting due to incomplete input. Please include the following files:")
        print("\t" + "bertiniInput_variables")
        print("\t" + "bertiniInput_trackingOptions")
        print("\t" + "bertiniInput_equations")

    # Set the string variableGroupText which is passed to bertini
    variableGroupText = ""

    # Set the list variable which is used by multiregeneration.py
    variables = []
    lines = bertiniVariables.splitlines()
    for i in range(len(lines)):
        variableGroupType = lines[i].split(" ")[0]
        if not (variableGroupType == "variable_group" or variableGroupType == "hom_variable_group"):
            print("Exiting because a variable group other that 'variable_group' or 'hom_variable_group' was declared.")
        if variableGroupType == "hom_variable_group":
            projectiveVariableGroups.append(i)
        variableGroupText+=lines[i]+"\n"
        variables.append(lines[i][lines[i].find(" "):].replace(" ","").replace(";", "").split(","))
    # Initialize bfe to the dimension of the ambient product of 
    # projective spaces.

    bfe=[]
    for i in range(len(variables)):
        isProjectiveGroup = 0
        if i in projectiveVariableGroups:
            isProjectiveGroup = 1
        bfe.append(len(variables[i])-isProjectiveGroup)
    # Show 
    if verbose > 1:
        print("Ambient space dimension ")
        print(bfe)
        print("variables")
        print(variables)
        print("projectiveVariableGroups")
        print(projectiveVariableGroups)
        print("variableGroupText")
        print(variableGroupText)

    # A string which stores the defining equations of the user inputed 
    # functions
    revisedEquationsText = ""

    lines = bertiniEquations.splitlines()

    # A list which stores the user inputed names of the functions
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

    #We read in the user's input from 'inputFile.py' by executing the 
    #following 
    exec(setVariablesToGlobal + open("inputFile.py").read())


# print to screen system summary.
    if verbose > 0:
        print("\n################### Setup multiregeneration ####################\n")
        print("These variable groups have been selected:\n"+variableGroupText)
        print("Solutions in a 'linearProduct' directory and :")
        for c, f in enumerate(fNames): # 0 is the depth we start with
            if c >= depth:
                print("depth >= "+str(c)+" satisfy "+ f+" = 0")
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
    else:
        (l, startSolution) = getLinearsThroughPoint(variables)
    if verbose > 0:
        print("\nUsing start solution")
        for i in startSolution:
            print(i)
        print("\nUsing dimension linears")
        for i in range(len(variables)):
            for j in range(len(l[i])):
                print("l[%s][%s]"%(i,j))
                print(l[i][j])
    # Determine random linear polynomials r[i][j] degree linears
    r = []
    # Populate the 2D list 'r' with random linear equations, unless the 
    # user has specified their own
    if not loadDegreeLinears:
        for i in range(len(variables)):
            r.append([])
            maxdeg= 0
            for s in range(len(fNames)):
                maxdeg= max(maxdeg,degrees[s][i])
            for d in range(maxdeg):
                r[i].append(getGenericLinearInVariableGroup(i))
    elif loadDegreeLinears:
        for i in range(len(variables)):
            maxdeg= 0
            for s in range(len(fNames)):
                maxdeg= max(maxdeg,degrees[s][i])
            with open("degreeLinears_%s" %i, "r") as f:
                A = (line.rstrip() for line in f)
                A = list(line for line in A if line)
            r.append(A)
    # Display the linear equations to the user
    if verbose > 0:
        print("\nUsing degree linears")
        for i in range(len(variables)):
            for j in range(len(r[i])):
                print(r[i][j])
    # The variable B specifies how many of the inputed equations to use. 
    # If the user has not specified a value, then assume that all 
    # equations are to be used.
    if B== None:
        B=len(fNames)
        if verbose > 1:
            print("B is set to %d" % B)
    if verbose > 0:
        print("exploring tree in order", explorationOrder)

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
    queue = mp.Manager().Queue() # a message queue for the child
    #processes to comunication with this one
    global priorityQueue
    priorityQueue = PriorityQueue() # where this process, which is the
    #queue manager, stores the jobs that need to be done

    priorityQueue.put((0,[depth, G, B, bfe, startSolution]))

    # One extra process for the progress updater
    if verbose >= 1:
        pool = mp.Pool(maxProcesses+1)
    else:
        pool = mp.Pool(maxProcesses)

    with jobsInPool.get_lock():
      jobsInPool.value = 0

    if verbose >= 1:
      pool.apply_async(updateProgressInfo)


    #This loop looks for messages from the child processes in the queue,
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


    pool.terminate()
    pool.close()
    if verbose >=1:
      updateProgressDisplay(cursorLeftAtBotten=True)
      print("Done.")


# A wrapper function around 'outlineRegenerate', which catches errors in 
# subprocesses.
def processNode(args): 
  try:
    outlineRegenerate(args[0], args[1], args[2], args[3], args[4])
  except Exception as e:
    print("There was an error in a child process.")
    print(e)
    print(traceback.format_exc())

# The function which each worker process calls. The input consists of:

# depth = The number of user inputed equations that the point P 
# satisfies

# G = A witness system. (i.e. a subset of the first 'depth' many 
# equations which suffice to specify the irreducible component of P on 
# the variety defined by the first 'depth' many equations.)

# B = The number of user inputed equations to consider.

# bfe = The dimension of the irreducible component of P on the variety 
# defined by the first 'depth' many equations.

# P = The coordinates of a point
def outlineRegenerate(depth,G,B,bfe,P):
    if len(degrees)!=len(fNames):
        print("Error: length of degree list does not coincide with the number of polynomials in the system.")

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
                # pruneByDimension returns False as the default.
                # Redfine this function in inputFile.py as you like.
                if not prune:
                    prune = pruneByDimension(bfePrime)
                if not prune:
                    for j in range(M[i]):
                        if verbose > 1:
                            print("M[i] = %d, j = %d"%(M[i],j))
                        label="unknown"
#                        print("We parentHomotopy at depth %s variable group %s degree %s and point %s" %(depth,i,j,hashPoint(P)))
                        dirTracking = directoryNameTracking(depth, G, bfePrime, i, j, P)
                        if not os.path.exists(dirTracking):
                                os.makedirs(dirTracking)
                        if verbose > 1:
                          print("directory before branchHomotopy is", os.getcwd())
                        if verbose > 1:
                            print("Calling branch homotopy with vg = %d, rg = %d, M[vg] = %d"%(i,j,M[i]))
                        # For each i and j, the function 'branchHomotopy' track the two 
                        # path necessary
                        (PPrime,label) = branchHomotopy(dirTracking, depth, G, bfePrime,bfe, i, j, M, P)
                        if verbose > 1:
                          print("directory after branchHomotopy is", os.getcwd())
                        count = 0
                        if len(algebraicTorusVariableGroups)>0 and len(PPrime)>0: # Prune if not in the algebraic torus based on algebraicTorusVariableGroups
                            for a in range(len(variables)):
                                for b in range(len(variables[a])):
                                    if (a in algebraicTorusVariableGroups):
                                        if coordinateLineIsZero(PPrime[count], logTolerance): # What should the logTolerance be here?
                                            label="prune"
                                    count = count +1;


                        # Check if coordinates are nonzero
                        count = 0
                        # Prune if not in the algebraic torus based on algebraicTorusVariableGroups
                        if len(nonzeroCoordinates)>0 and len(PPrime)>0:
                            for i in range(len(variables)):
                                for j in range(len(variables[i])):
                                    if (count in nonzeroCoordinates):
                                        if coordinateLineIsZero(PPrime[count], logTolerance): # What should the logTolerance be here?
                                            label="prune"
                                    count = count +1;

                        # Proceed if the endpoing is smooth and nonempty
                        if label=="smooth" and len(PPrime)>1:
                            completedSmoothSolutions = "_completed_smooth_solutions"
                            PPi=[]
                            for i2 in range(len(variables)):
                                ppGroup = []
                                for j2 in range(len(variables[i2])):
                                    ppGroup.append(PPrime[count])
                                    count = count +1;
                                PPi.append(ppGroup)
                            if not pruneByPoint(bfePrime,i2,PPi):
                                PPrime = []
                                for i3 in range(len(PPi)):
                                    for j3 in range(len(PPi[i3])):
                                        PPrime.append(PPi[i3][j3])
                                solText = "\n"
                                for line in PPrime:
                                    solText += line+"\n"
                                solName = directoryNameTrackingSolution(depth, G, bfePrime, i3, j3, PPrime, startHash)
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

# Hash the coordinates of a point to a string of numbers, which can be 
# appended to filenames to avoid collisions.
def hashPoint(P):
    return(abs(hash("_".join(P))) % (10 ** 12))

# A function which calls bertini to decide whether the next function 
# (index = depth) vanishes on the point P
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
        print("Bertini error likely: check bertiniInput_...")
        isVanishing="error"
    value = solutionsLines[2].split(' ')
    # print("Value of the function at the point: %s" % value)
    isVanishing = isZero(value[0], logTolerance) and isZero(value[1], logTolerance)
    with open("isVanishing", "w") as isVanishingFile:
      isVanishingFile.write(str(isVanishing))
    os.chdir(cwd)
    return(isVanishing)

# Template for Bertini file that we fill in.
bertiniParameterHomotopyTwoTemplate='''
CONFIG
TRACKTOLBEFOREEG : 1e-8;
TRACKTOLDURINGEG : 1e-11;
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

# Write the coordinates of a point to a bertini readable file
def writePStart(P,fn):
    startText = "1\n\n"
    for line in P:
        startText += line+"\n"
    startFile = open(fn, "w")
    startFile.write(startText)
    startFile.close()
    return()

# Writes the initial and final values of the homotopy parameters to a 
# bertini readable file
def writeParameters():
    parametersFile = open("start_parameters", "w")
    parametersFile.write("1\n1 0")
    parametersFile.close()
    parametersFile = open("final_parameters", "w")
    parametersFile.write("1\n0 0")
    parametersFile.close()
    return()



# This function tracks the two paths associated to each job in the pool. 
# The input data is:

# dirTracking = The directory in which to store the bertini files

# depth = The number of user inputed equations that are satisfied by the 
# point P

# G = A witness system. (i.e. a subset of the first 'depth' many 
# equations which suffice to specify the irreducible component of P on 
# the variety defined by the first 'depth' many equations.)

# bfe = The dimension of the irreducible component of P on the variety 
# defined by the first 'depth' many equations.

# bfePrime = The new dimension of the irreducible component of P, after 
# P is tracked to satisfy the linear equation in variable group vg of 
# index rg.

# vg = the index of a variable group

# rg = the index of a linear equation (from 'r') in variable group vg

# M = a list of integers that stores the degree of the next equation 
# (index = depth) in the variable group vg.

# P = The coordinates of a point

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
    # Setup the input for calling bertini
    writePStart(P,"start")
    writePStart(P,"P")
    writeParameters()
    ## Now we do PQ
    if verbose > 1:
        print("vg = %s, rg = %s, bfePrime[eval(vg)] = %d"%(vg,rg,bfePrime[eval(vg)]))
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
        if label != "error" and os.path.exists("nonsingular_solutions"):
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
            process = subprocess.Popen(bertiniCommand.split(), stdout=subprocess.PIPE)
            output, errors = process.communicate()
        except:
            print("error (branch QP): %s" %dirTracking)
            label = "error"
        if label != "error" and os.path.exists("nonsingular_solutions"):
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


# A helper function to determine if a value is zero.
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
    useFunction = "_".join(map(lambda b: "1" if b else "0", G+[1]))
    dirName = "homotopy_tracking/depth_%d/gens_%s/dim_%s/varGroup_%d/regenLinear_%d/pointId_%s"%(depth,
        useFunction,
        "_".join(map(str, bfe)),
        varGroup,
        regenLinear,
        hashPoint(P)
        )
    return dirName


def directoryNameTrackingSolution(depth, G, bfe, varGroup, regenLinear, P, startHash):
    useFunction = "_".join(map(lambda b: "1" if b else "0", G+[1]))
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
    useFunction = "_".join(map(lambda b: "1" if b else "0", G+[1]))
    dirName = "homotopy_tracking/depth_%d/gens_%s/dim_%s/varGroup_%d/regenLinear_%d/pointId_%s"%(depth,
        useFunction,
        "_".join(map(str, bfe)),
        varGroup,
        regenLinear,
        hashPoint(P)
        )
    return dirName

def updateProgressDisplay(cursorLeftAtBotten = False):
    maxDepth = len(os.listdir("_completed_smooth_solutions"))
    # currentDepths = [int(s.split("_")[1]) for s in \
    #     os.listdir("_completed_smooth_solutions")]
    # currentDepths.sort()
    solsAtDepth = \
    [os.listdir("_completed_smooth_solutions/depth_"+str(depth))\
      for depth in range(maxDepth)]

    currentDisplay ="PROGRESS" + "\n"
    for depth in range(maxDepth):
      currentDisplay+=("Depth %d: %d\n"%(depth,len(solsAtDepth[depth])))

    fullDepthDims = []
    for s in solsAtDepth[-1]:
        if "tracking" in s:
           fullDepthDims.append(s.split("dim")[1].split("varGroup")[0])
        else:
           fullDepthDims.append(s.split("dim")[1].split("pointId")[0])


    currentDisplay += """
----------------------------------------------------------------
| # smooth isolated solutions  | # of general linear equations |
| found                        | added with variables in group |
----------------------------------------------------------------
                               | %s
----------------------------------------------------------------
"""%("  ".join([str(i) for i in range(len(variables))]))
    currentMultidegreeBound = Counter(fullDepthDims)
    for d in currentMultidegreeBound.keys():
      dimension = d.split("_")[1:-1]
      # if all([i=="0" for i in dimension]):
      #     currentDisplay += \
      #         "Found %d isolated smooth solutions\n"%currentMultidegreeBound[d]
      # else:
      currentDisplay += "  "\
          + str(currentMultidegreeBound[d])\
          + " "*(31-len(str(currentMultidegreeBound[d])))\
          + "".join([str(i) + " "*(3-len(str(i))) for i in dimension])\
          + "\n"

    sys.stdout.write(currentDisplay)
    sys.stdout.flush()
    if not cursorLeftAtBotten:
        sys.stdout.write("\033[F"*len(currentDisplay.splitlines()))
        sys.stdout.flush()

def updateProgressInfo():
  while True:
    updateProgressDisplay()
    time.sleep(0.4)




if __name__== "__main__":
  main()
