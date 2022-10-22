from math import fabs
import numpy as np
import numba as nb


"""Implementation of different kind of user build-in functions.
"""
@nb.jit 
def mean_filter(data,height,width,radius):
    mean_logy=np.zeros((height,width))
    radius-=1
    for i in range(height):
        limitUp = (i-radius) if (i-radius)>0 else 0
        limitDown = (i+radius) if (i+radius)<(height-1) else (height-1)
        
        for j in range(width):
            summ = N = 0
            limitLeft = (j-radius) if (j-radius)>0 else 0
            limitRight = (j+radius) if (j+radius)<(width-1) else (width-1)
            
            for x in range(limitUp,limitDown+1):
                for y in range(limitLeft, limitRight+1):
                    summ += data[x, y]
                    N += 1
                    
            if (N>0):
                summ /= N
                mean_logy[i, j] = summ
            else:
                print("Value of width, height and radius is invalid")
                
    return mean_logy

@nb.jit     
def clip(data,height, width, limit):
   
    result=np.zeros((height,width))
    
    for i in range(height):
        for j in range(width):
            if (fabs(data[i, j])> limit):
                if (data[i, j]>0):
                    result[i, j]=limit
                else:
                    result[i, j]=-limit
            else:
                result[i, j]=data[i, j]
    return result                    
    
    

                