degrees = [[2],[2]]
verbose = 1
def pruneByPoint(bfePrime, i, PPi):
    # The complex coordinates (in variable group 0) of the point PPi
    coordinates = \
        [complex(s.replace(" -","-").replace(" ", "+") +"j") for \
        s in PPi[0]]

    # If either x_1=0 or x_2=0 is satisfied to within a 
    # tolerance of 1e-16, then the point will lie on the 'extra' 
    # component, and should be pruned.

    if abs(coordinates[1]) < 1e-16  or \
            abs(coordinates[2]) < 1e-16:
      return True
    else:
      return False

