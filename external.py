'''
External Test Set Split Code
Split the input data into train set and test set
Algorithm: Kennard Jones and sphere code
First written: Thien-Phuc Tu-Nguyen
Tested on Anaconda3 version 4.4 with respective packages
Last modified: June 2017 by Thien-Phuc Tu-Nguyen 
'''
import numpy as np
from scipy.spatial.distance import pdist,squareform

def Kennard_Stone(inp,pair):
    n = inp.shape[0]
    distance = squareform(pdist(inp))
    train_index = []
    for k in range(pair):
        i_max = 0
        j_max = 0
        max_distance = 0
        for i in range(n-1):
            for j in range(i+1,n):
                if i not in train_index and j not in train_index and distance[i,j] > max_distance:
                    i_max = i
                    j_max = j
                    max_distance = distance[i,j]
        train_index += [i_max,j_max]
    return train_index

def sphere_split(inp,first = 0,c=0.1):
    n = inp.shape[0]
    d = inp.shape[1] # Dimension
    distance = squareform(pdist(inp))
    center = first
    train_index = [first]
    test_index = []
    radius = 2*c / (n **(1/d))
    for i in range(n):
        if distance[center,i] <= radius and i != center:
            test_index += [i]
    while len(train_index) + len(test_index) < n:
        max_distance = 0
        temp = 0
        for i in range(n):
            if i not in train_index and i not in test_index and distance[i,center]>max_distance:
                temp = i
                max_distance = distance[i,center]
        center = temp
        train_index += [temp]
        for i in range(n):
            if distance[center,i] <= radius and i not in train_index and i not in test_index:
                test_index += [i]
    return train_index

def c_detector(inp,train_size,first=0,c_range = (0.01,100)):
    c_min = c_range[0]
    c_max = c_range[1]
    c = (c_min+c_max)/2
    current = len(sphere_split(inp,first,c))
    while current!=train_size:
        if current > train_size:
            c_min = c
        else:
            c_max = c
        c = (c_max+c_min)/2
        current = len(sphere_split(inp,first,c))
    return c