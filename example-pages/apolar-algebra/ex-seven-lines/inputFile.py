# seven-lines
degrees  = [
    [1,1,1, 1,0],[1,1,1, 1,0],[1,1,1, 1,0],[1,1,1, 1,0],[1,1,1, 1,0],
    [1,1,1, 1,0],[1,1,1, 1,0],[1,1,1, 1,0],[1,1,1, 1,0],[1,1,1, 1,0],
    [1,1,1, 1,0],[1,1,1, 1,0],[1,1,1, 1,0],[1,1,1, 1,0],[1,1,1, 1,0],
    [1,1,1, 0,1],[1,1,1, 0,1],[1,1,1, 0,1],[1,1,1, 0,1],[1,1,1, 0,1],
    [1,1,1, 0,1],[1,1,1, 0,1],[1,1,1, 0,1],[1,1,1, 0,1],[1,1,1, 0,1],
    [1,1,1, 0,1],[1,1,1, 0,1],[1,1,1, 0,1],[1,1,1, 0,1],[1,1,1, 0,1]
    ]

targetDimensions = [[0, 0, 0, 0, 0]]
explorationOrder = "depthFirst"
verbose = 1
#algebraicTorusVariableGroups =[0,1,2,3,4]
#nonzeroCoordinates = [0,8,16]
# def pruneByPoint(coordinates):
#     if min(abs(coordinates[0]),abs(coordinates[3]),abs(coordinates[6])) > 1e-12:
#         if abs(sum(coordinates[0:3])/coordinates[0]-sum(coordinates[3:6])/coordinates[3])<1e-9:
#             return True
#         if abs(sum(coordinates[0:3])/coordinates[0]-sum(coordinates[6:9])/coordinates[6])<1e-9:
#             return True
#         if abs(sum(coordinates[3:6])/coordinates[3]-sum(coordinates[6:9])/coordinates[6])<1e-9:
#             return True
#     else:
#       return False
