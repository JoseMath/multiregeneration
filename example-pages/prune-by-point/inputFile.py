degrees = [[3]]
verbose = 1
def pruneByPoint(coordinates):
    # If either x-y is satisfied to within a 
    # tolerance of 1e-16, then the point will lie on the 'extra' 
    # component, and should be pruned.

    if abs(coordinates[0] - coordinates[1]) < 1e-10:
      return True
    else:
      return False
