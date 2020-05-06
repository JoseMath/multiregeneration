import time
import sys
import os
from collections import Counter

while True:
  time.sleep(1)
  sys.stdout.write("\033[F"*len(currentDisplay.splitlines()))
  sys.stdout.flush()
  currentDepths = os.listdir("run/_completed_smooth_solutions")
  currentDepths.sort()
  solsAtDepth = [os.listdir("run/_completed_smooth_solutions/"\
      +directory) for directory in currentDepths]

  currentDisplay = "#"*40+"\n"
  currentDisplay = "PROGRESS\n" 
  currentDisplay += "#"*40+"\n"
  for i in range(len(currentDepths)):
    currentDisplay+=("%s: %d\n"%(currentDepths[i],\
      len(solsAtDepth[i])))

  currentDisplay += "#"*40 + "\n\n"
  fullDepthDims = [(s.split("dim")[1].split("varGroup")[0])\
      for s in solsAtDepth[-1]]
  currentMultidegreeBound = Counter(fullDepthDims)
  for d in currentMultidegreeBound.keys():
    currentDisplay += "Found components of multidimension (%s)\n"%(",".join(d.split("_")))
    currentDisplay +=\
        "Total degree of these components is >= %d\n"%currentMultidegreeBound[d]
    currentDisplay += "\n\n"
  




  sys.stdout.write(currentDisplay)
  sys.stdout.flush()
