#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  3 17:36:22 2022

@author: ozgesurer
"""
import numpy as np
from collections import Counter
#  SSE of a a new splitted point; if nonparent it is two nodes (left, right)
#   if parent, only one node
def sse_for_new_split(groups, notparent, args):
    sse = 0.0
    if notparent:
        for group in groups:
            mean_target = sum([row[-1] for row in group])/float(len(group))
            sse += sum([pow(row[-1]-mean_target,2) for row in group])
    else:
        mean_target = sum([row[-1] for row in groups])/float(len(groups))
        sse = sum([pow(row[-1]-mean_target,2) for row in groups])  
    return sse

def crps_for_new_split(groups, notparent, args):
    total_crps = 0          
    if notparent:
        for group in groups:
            targets = np.asarray([row[-1] for row in group])            
            x = list(Counter(targets).keys())
            r = list(Counter(targets).values())
            
            crps_2 = 0.0
            for j, leaf_point_q in enumerate(x):
                s = 0.0
                for i, leaf_point in enumerate(x):
                    s += abs(leaf_point_q-leaf_point)*r[i]
                crps_2 += s*r[j]            
            total_crps += crps_2/(2*len(targets))
    else:
        targets = np.asarray([row[-1] for row in groups])
        x = list(Counter(targets).keys())
        r = list(Counter(targets).values())
        
        crps_2 = 0.0
        for j, leaf_point_q in enumerate(x):
            s = 0.0
            for i, leaf_point in enumerate(x):
                s += abs(leaf_point_q-leaf_point)*r[i]
            crps_2 += s*r[j]
        total_crps += crps_2/(2*len(targets))
    return total_crps  

def dss_for_new_split(groups, notparent, args):
    dss = 0.0
    if notparent:
        for group in groups:
            targets = np.asarray([row[-1] for row in group])
            mhat = np.mean(targets)
            vhat = max(np.var(targets),.1)
            dss += (np.log(vhat)*len(targets)+ sum([pow(x-mhat,2) for x in targets])/vhat)
    else:
        targets = np.asarray([row[-1] for row in groups])
        mhat = np.mean(targets)
        vhat = max(np.var(targets),.1)
        dss += (np.log(vhat)*len(targets)+ sum([pow(x-mhat,2) for x in targets])/vhat)
    return dss

def is1_for_new_split(groups, notparent, args):
    alpha = args['alpha']
    is1 = 0.0
    if notparent:
        for group in groups:
            targets = sorted(np.asarray([row[-1] for row in group]))
            u = targets[int(np.ceil((1-alpha)*len(targets)))-1]
            is1 += (u*len(targets)+sum([(x-u)*(x>=u) for x in targets])/alpha)
    else:
        targets = sorted(np.asarray([row[-1] for row in groups]))
        u = targets[int(np.ceil((1-alpha)*len(targets)))-1]
        is1 += (u*len(targets)+sum([(x-u)*(x>=u) for x in targets])/alpha)
    return is1
