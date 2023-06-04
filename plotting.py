'''
Plotting Module
Plot the data for QSPR model
First written by: Thien-Phuc Tu-Nguyen
Tested on Anaconda3 version 4.4 with respective packages
Last modified: June 2017 by Thien-Phuc Tu-Nguyen
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from sklearn.preprocessing import StandardScaler

def regression(pred,obs,pre = None,title='',expand = 0.1):
    if pre != None:
        x = pre.output_scaler.inverse_transform(pred)
        y = pre.output_scaler.inverse_transform(obs)
    else:
        x = pred
        y = obs
    fig = plt.figure()
    ax = fig.add_subplot(111)
    min_value = min(x.min(),y.min())
    max_value = max(x.max(),y.max())
    ax.scatter(x,y,marker='o')
    min_value,max_value = min_value - (max_value - min_value)*expand , max_value + (max_value - min_value)*expand
    ax.set(xlim=[min_value,max_value],ylim=[min_value,max_value])
    ax.set(title = '')
    ax.set(xlabel = 'Predicted Values',ylabel = 'Experimental Values')
    ax.plot([min_value,max_value],[min_value,max_value])
    return fig
    
def split_regression(pred_train,obs_train,pred_test,obs_test,pre = None,title = '',expand = 0.1):
    if pre != None:
        x_train = pre.output_scaler.inverse_transform(pred_train)
        y_train = pre.output_scaler.inverse_transform(obs_train)
        x_test = pre.output_scaler.inverse_transform(pred_test)
        y_test = pre.output_scaler.inverse_transform(obs_test)
    else:
        x_train = pred_train
        y_train = obs_train
        x_test = pred_test
        y_test = obs_test
    fig = plt.figure()
    ax = fig.add_subplot(111)
    min_value = min(x_train.min(),y_train.min(),x_test.min(),y_test.min())
    max_value = max(x_train.max(),y_train.max(),x_test.max(),y_test.max())
    ax.scatter(x_train,y_train,marker='o',color='blue')
    ax.scatter(x_test,y_test,marker='^',color='red')
    min_value,max_value = min_value - (max_value - min_value)*expand , max_value + (max_value - min_value)*expand
    ax.set(xlim=[min_value,max_value],ylim=[min_value,max_value])
    ax.set(title = title)
    ax.set(xlabel = 'Predicted Values',ylabel = 'Experimental Values')
    ax.plot([min_value,max_value],[min_value,max_value])
    return fig
    
def plot3d(x_list,y_list,data,xlabel = '',ylabel = '',zlabel = ''):
    x,y = np.meshgrid(x_list,y_list)
    dat = np.array(data)
    z = np.copy(x)
    fig = plt.figure()
    ax = fig.add_subplot(111,projection = '3d')
    for j in range(len(x_list)):
        for i in range(len(y_list)):
            index = 0
            while (dat[index,0] != x_list[j])**2 > 0.000001 or (dat[index,1] != y_list[i])**2 > 0.000001:
                index += 1
            z[i,j] = dat[index,2]
    surf = ax.plot_surface(x,y,z,cmap = cm.coolwarm, antialiased=False,cstride =1,rstride=1)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_zlabel(zlabel)
    fig.colorbar(surf, shrink=0.5, aspect=5)
    return fig
    
def william(inp_train,inp_test,outp_train,outp_test,pred_train,pred_test,h = -1, expand = 0.2):
    # Only work with linear regression
    x_train = np.array(inp_train)
    x_test = np.array(inp_test)
    beta =  np.linalg.inv(np.dot(x_train.transpose(),x_train))
    H_train = np.dot(np.dot(x_train,beta),x_train.transpose())
    H_test = np.dot(np.dot(x_test,beta),x_test.transpose())
    h_train = H_train.diag()
    h_test = H_test.diag()
    rs_train = pred_train - outp_train
    rs_test = pred_test - outp_test
    r_train = rs_train / rs_train.std()
    r_test = rs_test / rs_test.std()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(h_train,r_train,marker = 'o', color = 'blue')
    ax.scatter(h_test,r_test,marker = '^',color = 'red')
    x_max = max(h_train.max(),h_test.max()) * (1+expand)
    y_max = 0
    if max(r_train.max(),r_test.max()) < 3 and min(r_train.min(),r_test.min())>-3:
        y_max = 4
    else:
        y_max = max(max(r_train.max(),r_test.max()),-min(r_train.min(),r_test.min())) + 1
    ax.set_xlim([0,x_max])
    ax.set_ylim([-y_max,y_max])
    ax.plot([0,x_max],[3,3],'--',color = 'black')
    ax.plot([0,x_max],[-3,-3],'--',color = 'black')
    ax.plot([0.512,0.512],[-y_max,y_max],'--',color = 'black')
    return fig