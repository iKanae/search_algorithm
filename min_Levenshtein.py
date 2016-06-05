import numpy as np

def getMinValue(x,y):
    if str(x)==str(y):
        return 0
    else:
        return 1

def editDist(a,b):
    a='0'+a
    b='0'+b
    lenA=len(a)
    lenB=len(b)
    r=np.zeros((lenA,lenB))
    for i in range(len(a)):
        for j in range(len(b)):
            if i==1:
                r[i,j]=j
            elif j==1:
                r[i,j]=i
            else:
                r[i,j]=min(r[i-1,j]+1,r[i,j-1]+1,r[i-1,j-1]+getMinValue(a[i],b[j]))
    return r[lenA-1,lenB-1]