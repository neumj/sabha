# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 12:25:42 2013

@author: Ben
"""

def updateGraphCosts(grph,perturbedCosts):
    """Update weights of graph.
    
    Generate an updated weighted graph using perturbed costs.
        
    Returns: grph <class 'networkx.classes.graph.Graph'>
    """
    edgesT = tuple(map(tuple, perturbedCosts[:,0:3]));
    for edg in edgesT:
        grph[edg[0]][edg[1]]['weight'] = edg[2]
    return grph