
def shrinkNetwork(nodes,links,Xllcorner,Yllcorner,Xurcorner,Yurcorner):
    """Remove nodes and links from a network to fit inside raster.
    
    Replaces nodes outside raster with NaN.  Deletes rows of links where a
    node of that link is outside raster.  Renumbers links.
    """
    nodesoutside1 = np.nonzero(nodes[:,1]<Xllcorner);
    nodesoutside2 = np.nonzero(nodes[:,1]>Xurcorner);
    nodesoutside3 = np.nonzero(nodes[:,2]<Yllcorner);
    nodesoutside4 = np.nonzero(nodes[:,2]>Yurcorner);
    nodesOutsideIdx = np.concatenate((nodesoutside1[0],nodesoutside2[0], \
        nodesoutside3[0],nodesoutside4[0]),axis=0);
    nodesoutside = nodesOutsideIdx + 1;
    linksoutside1=np.in1d(links[:,1],nodesoutside);  
    linksoutside2=np.in1d(links[:,2],nodesoutside);
    linksoutsideIdx1=np.nonzero(linksoutside1[:]==1); 
    linksoutsideIdx2=np.nonzero(linksoutside2[:]==1);
    linksoutsideIdx = np.concatenate((linksoutsideIdx1,linksoutsideIdx2),axis=1);
    linksoutsideLst = set(list(linksoutsideIdx[0]));
    links = np.delete(links,linksoutsideLst,axis=0);
    links[:,1]=np.arange(1,links.shape[0]+1,1);
    nodes[nodesOutsideIdx,:]=NaN;
    return nodes, links