# -*- coding: utf-8 -*-
"""
Created on Fri Nov 08 14:19:43 2013

@author: Ben
"""

import networkx as nx
grph = nx.Graph();
grph.add_nodes_from(nodes[:,0]);
edgesT = tuple(map(tuple, links[:,1:4]));
grph.add_weighted_edges_from(edgesT,weight='weight');
#for edg in grph.edges():
#    grph[edg[0]][edg[1]]['weight'] = np.random.rand()
    #print grph[edg[0]][edg[1]]