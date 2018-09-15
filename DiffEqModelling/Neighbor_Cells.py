from numpy import *

def nbrs(mat, x, y ):
    results = []
    for dx in [-1,0,1]:
        for dy in [-1,0,1]:
            newx = x+dx
            newy = y+dy
            if (dx == 0 and dy == 0):
                continue
            if (newx>=0 and newx<len(mat) and newy >=0 and newy<len(mat)):
                results.append( mat[newx, newy] )
    return results

test = random.randint(3, size = (5,5))
print test

print nbrs(test, 0, 0)
print nbrs(test, 0, 0).count(1)


