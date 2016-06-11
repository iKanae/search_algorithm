#quick_sort
def quick_sort(a,l,r):
    if l<r:
        i=l
        j=r
        x=a[l]
        while i<j:
            while i<j and a[j]>=x:
                j=j-1
            if i<j:
                a[i]=a[j]
                i=i+1

            while i<j and a[i]<x:
                i=i+1
            if i<j:
                a[j]=a[i]
                j=j-1
        a[i]=x
        quick_sort(a,l,i-1)
        quick_sort(a,i+1,r)
    return a
