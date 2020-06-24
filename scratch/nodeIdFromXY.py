def nodeIdFromXY(lat, lon, nodes):
    """Calculate closest network node from input latitude/ longitude.
        
    Returns: nodeId <type 'numpy.float64'>
    """
    d = np.sqrt(np.square(nodes[:,1]-lon) + np.square(nodes[:,2]-lat))
    nodeIdx = np.nonzero(d == d.min())
    nodeId = nodes[nodeIdx[0][0],0]
