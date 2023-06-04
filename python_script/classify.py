# Divide code
import numpy as np
import pandas as pd

def classify(x,n):
    y = pd.DataFrame(index = x.index,columns = x.columns)
    dim = x.shape[0]
    for name,dat in x.iteritems():
        dat = dat.sort_values()
        index = np.zeros(n+1)
        index[0] = dat.min() - 1
        index[n] = dat.max() + 1
        for i in range(1,n):
            index[i] = (dat.iloc[i*dim//n-1] + dat.iloc[i*dim//n])/2
        for i in range(n):
            y.loc[(index[i] <= dat) & (dat < index[i+1]),name] = i
    return y
