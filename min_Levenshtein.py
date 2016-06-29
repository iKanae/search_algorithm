import numpy as np

def getMinValue(x,y):
    if str(x)==str(y):
        return 0
    else:
        return 1

def editDist(a,b):
    lenA=len(a)+1
    lenB=len(b)+1
    r=np.zeros((lenA,lenB))
    for i in range(lenA):
        for j in range(lenB):
            if i==0 and j>0:
                r[i,j]=j
            elif j==0 and i>0:
                r[i,j]=i
            elif i>=1 and j>=1:
                r[i,j]=min(r[i-1,j]+1,r[i,j-1]+1,r[i-1,j-1]+getMinValue(a[i-1],b[j-1]))
    return r

