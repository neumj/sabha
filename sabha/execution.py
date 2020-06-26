# -*- coding: utf-8 -*-
import numpy as np
import networkx as nx
import time as tm
def makeRegularNetworkMatrix(width, height, ntype, xlow, ylow, xhigh, yhigh):
    """Create regularly spaced nodes in a square pattern and connect nodes based 
    on specified types.

    Network types include: Rook (4 connections per node), Queen (8 connections per node), 
    and Knight (16 connections per node).
    
    Returns: nodes <type 'numpy.ndarray'>; links <type 'numpy.ndarray'>
    """
    # This function will create regularly spaced nodes in a square pattern
    #and connect them based on type.  
    #Type 1 is Rook's
    #Type 2 is Queen's
    #Type 3 is Knight's
    #width=5;
    #height=5;
    #xlow=1;
    #ylow=1;
    #xhigh=width;
    #yhigh=height;
    #ntype=2;
    #width=Options['width'];
    #height=Options['height'];
    #xlow=Options['xlow'];
    #ylow=Options['ylow'];
    #xhigh=Options['xhigh'];
    #yhigh=Options['yhigh'];
    #ntype=2;
            
    ##Create nodes
    xres=int(width);
    yres=int(height);
    xstep = abs(xhigh-xlow)/(xres-1);
    ystep = abs(yhigh-ylow)/(yres-1);
    numnodes = xres*yres;
    xcoords = np.arange(xlow,(xhigh + (xstep / 2)),xstep);
    v1 = np.array([]);
    for i in range(0,yres):
        v1 = np.concatenate((v1,xcoords));
    v1 = v1.reshape((v1.shape[0],1))
    v2 = np.array([]);
    yinc = ylow;
    for i in range(0,yres):
        tempNodes = (yinc * np.ones((1,xres)))[0]; 
        v2 = np.concatenate((v2, tempNodes));
        yinc=yinc+ystep;
    v2 = v2.reshape((v2.shape[0],1));
    nodes = np.zeros((v2.shape[0],3));
    nodes[:,1]=v1[:,0];
    nodes[:,2]=v2[:,0];
    nodes[:,0]=np.arange(1,(nodes.shape[0] + 1),1);
    
    #Create links
    # Rook's Links
    up01 = np.arange(1,((numnodes-width)+1),1)
    up02 = np.arange((1+width),(numnodes+1),1)
    upward=np.int32(np.zeros((up01.shape[0],2)));
    upward[:,0]=up01
    upward[:,1]=up02
    rt01 = np.arange(1,numnodes,1)
    rt02 = np.arange(2,(numnodes+1),1);
    rightward=np.int32(np.zeros((rt01.shape[0],2)));
    rightward[:,0]=rt01
    rightward[:,1]=rt02
    d=list(np.arange((width-1),(numnodes-1),width));
    rightward = np.delete(rightward,d,axis=0) # Slice out rows d from rightward
    
    # Queen's Links
    if ntype >= 2:
        qUD01 = np.arange(1,(numnodes-width),1);
        qUD02 = np.arange((2+width),(numnodes+1),1);
        QUpDiag = np.int32(np.zeros((qUD01.shape[0],2)));
        QUpDiag[:,0] = qUD01;
        QUpDiag[:,1] = qUD02;
        d=list(np.arange((width-1),(numnodes-width-1),width));
        QUpDiag = np.delete(QUpDiag,d,axis=0)    
        qDD01 = np.arange(2,(numnodes-width+1),1);
        qDD02 = np.arange((1+width),numnodes,1);
        QDownDiag = np.int32(np.zeros((qDD01.shape[0],2)));
        QDownDiag[:,0] = qDD01;
        QDownDiag[:,1] = qDD02;
        d=list(np.arange((width-1),(numnodes-width-1),width));
        QDownDiag = np.delete(QDownDiag,d,axis=0);
    
    # Knight's links
    if ntype == 3:
        kUD101 = np.arange(1,(numnodes-2*width),1);
        kUD102 = np.arange((2+2*width),(numnodes+1),1);
        KUpDiag1 = np.int32(np.zeros((kUD101.shape[0],2)));
        KUpDiag1[:,0] = kUD101; 
        KUpDiag1[:,1] = kUD102
        d=list(np.arange((width-1),(numnodes-2*width-1),width));
        KUpDiag1 = np.delete(KUpDiag1,d,axis=0);
        kUD201 = np.arange(1,(numnodes-width-1),1);
        kUD202 = np.arange((1+width+2),(numnodes+1),1);
        KUpDiag2 = np.int32(np.zeros((kUD201.shape[0],2)));
        KUpDiag2[:,0] = kUD201; 
        KUpDiag2[:,1] = kUD202;
        d1 = (np.arange((width-1),(numnodes-2*width),width))-1;
        d2 = (np.arange(width,(numnodes-1*width),width))-1;
        d = list(np.concatenate((d1,d2)));
        KUpDiag2 = np.delete(KUpDiag2,d,axis=0);
        kDD101 = np.arange((1+width),(numnodes-1),1);
        kDD102 = np.arange(3,(numnodes-width+1),1);
        KDownDiag1 = np.int32(np.zeros((kDD101.shape[0],2)));
        KDownDiag1[:,0] = kDD101; 
        KDownDiag1[:,1] = kDD102;
        d1 = (np.arange((width-1),(numnodes-2*width),width))-1;
        d2 = (np.arange(width,(numnodes-1*width),width))-1;
        d = list(np.concatenate((d1,d2)));
        KDownDiag1 = np.delete(KDownDiag1,d,axis=0);
        kDD201 = np.arange((1+2*width),numnodes,1);
        kDD202 = np.arange(2,(numnodes-2*width)+1,1);
        KDownDiag2 = np.int32(np.zeros((kDD201.shape[0],2)));
        KDownDiag2[:,0] = kDD201; 
        KDownDiag2[:,1] = kDD202;
        d = (np.arange(width,(numnodes-2*width),width))-1;
        KDownDiag2 = np.delete(KDownDiag2,d,axis=0);
        
    # Assemble all links
    if ntype == 1:
        whole=np.concatenate((upward,rightward),axis=0);
    elif ntype ==2:
        whole=np.concatenate((upward,rightward,QUpDiag,QDownDiag),axis=0);
    elif ntype == 3:
        whole=np.concatenate((upward,rightward,QUpDiag,QDownDiag,KUpDiag1, \
        KUpDiag2,KDownDiag1,KDownDiag2),axis=0);
    c=np.int32(np.ones((whole.shape[0],1)));
    wholeDir1 = np.concatenate((whole,c),axis=1);
    wholeDir2 = np.zeros((wholeDir1.shape[0],3));
    wholeDir2[:,0] = wholeDir1[:,1]; 
    wholeDir2[:,1] = wholeDir1[:,0];
    wholeDir2[:,2] = 1;
    wholeList = np.concatenate((wholeDir1,wholeDir2),axis=0);
    linksId = np.arange(1,(wholeList.shape[0]+1),1);
    linksId = linksId.reshape((linksId.shape[0],1))
    links=np.concatenate((linksId,wholeList),axis=1);
    return nodes,links

def travelDirection(direction,width,nodes,height):
    """Set network nodes as starting/ ending points based on a defined travel direction. 
    
    Travel directions are North to South, South to North, East to West, West to East.
    
    Returns: stPts <type 'dict'>; enPts <type 'dict'>
    """    
    height = int(height);
    width = int(width)
    stPts = {}
    enPts = {}
    if direction==1 or direction==2:
        SPts=nodes[0:width,:];
        NPts=nodes[((np.shape(nodes)[0])-(width)):(np.shape(nodes)[0]),:];
        if direction==1:
            for ln in NPts:
                stPts.update({int(ln[0]):{'lat':ln[2],'lon':ln[1]}})
            for ln in SPts:
                enPts.update({int(ln[0]):{'lat':ln[2],'lon':ln[1]}})
        elif direction==2:  
            for ln in SPts:
                stPts.update({int(ln[0]):{'lat':ln[2],'lon':ln[1]}})
            for ln in NPts:
                enPts.update({int(ln[0]):{'lat':ln[2],'lon':ln[1]}})
    elif direction==3 or direction==4:
        ETargets=np.arange((height-1),np.shape(nodes)[0]+1,height);
        EPts=nodes[ETargets,:];
        WTargets=np.arange(0,(np.shape(nodes)[0]-height)+1,height);
        WPts=nodes[WTargets,:];
        if direction==3:
            for ln in EPts:
                stPts.update({int(ln[0]):{'lat':ln[2],'lon':ln[1]}})
            for ln in WPts:
                enPts.update({int(ln[0]):{'lat':ln[2],'lon':ln[1]}})
        elif direction==4:  
            for ln in WPts:
                stPts.update({int(ln[0]):{'lat':ln[2],'lon':ln[1]}})
            for ln in EPts:
                enPts.update({int(ln[0]):{'lat':ln[2],'lon':ln[1]}})
    return stPts, enPts
    
def shrinkNetwork(nodes,links,Xllcorner,Yllcorner,Xurcorner,Yurcorner):
    """Remove nodes and links from a network to fit inside raster.
    
    Replaces nodes outside raster with NaN.  Deletes rows of links where a
    node of that link is outside raster.  Renumbers links.
    
    Returns: nodes <type 'numpy.ndarray'>; links <type 'numpy.ndarray'>
    """
    #Xllcorner=Options['RasterMinLon'];
    #Yllcorner=Options['RasterMinLat'];
    #Xurcorner=Options['RasterMaxLon'];
    #Yurcorner=Options['RasterMaxLat'];    
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
    linksoutsideLst = list(np.unique(linksoutsideIdx));
    links = np.delete(links,linksoutsideLst,axis=0);
    links[:,1]=np.arange(1,links.shape[0]+1,1);
    nodes[nodesOutsideIdx,:]=np.nan;
    return nodes, links
    
def nodeIdFromXY(lat, lon, nodes):
    """Calculate closest network node from input latitude/ longitude.
        
    Returns: nodeId <type 'numpy.float64'>
    """
    d = np.sqrt(np.square(nodes[:,1]-lon) + np.square(nodes[:,2]-lat))
    nodeIdx = np.nonzero(d == d.min())
    nodeId = nodes[nodeIdx[0][0],0]
    return nodeId 

def makeWeightedDiGraph(nodes,links):
    #def makeWeightedGraph(nodes,links,totalCost):
    """Generated a weighted, directed, graph.
    
    Generate a weighted graph from nodes and links arrays.  Graph should be 
    directed, as links is a directed list of all arcs. 
        
    Returns: grph <class 'networkx.classes.graph.Graph'>
    """
    grph = nx.DiGraph();
    grph.add_nodes_from(nodes[:,0]);
    edgesT = tuple(map(tuple, links[:,1:4]));
    grph.add_weighted_edges_from(edgesT,weight='weight');
    return grph 
    
def updateDiGraphCosts(grph,perturbedCosts):
    """Update weights of directed graph.
    
    Generate an updated weighted, directed, graph using perturbed costs.
        
    Returns: grph <class 'networkx.classes.graph.Graph'>
    """
    edgesT = tuple(map(tuple, perturbedCosts[:,0:3]));
    for edg in edgesT:
        grph[edg[0]][edg[1]]['weight'] = edg[2]
    return grph

def traceNodesBack(predecessors,distance,startNode,endNode):
    """Generate least cost path and cost from a start node to end node.
    
    Generate a path and total cost from a start node to end node based
    on a Predecessor and Distance matrix from a Dijkstra solution.
        
    Returns: path <type 'list'>; pathCost <type 'numpy.float64'>
    """    
    n=endNode;
    path = [];
    while predecessors[n]!=[]:
        path.append(n);
        n=predecessors[n][0];
    path.append(startNode)
    path.reverse()
    pathCost = distance[endNode]
    return path, pathCost
    
def startendPointsToNodes(Options,nodes):
    """From starting and ending points, generate list of corresponding nodes.
    
    Uses 'nodeIdFromXY' to identify closest node.  Loops and generates a list.  
    Updates Options file with Options['StNode'], Options['EnNode'].
    
    Returns: Options <type 'dict'>
    """
    ##Calculate start and end nodes
    Options['StNode']=[];
    for ky in Options['StartPoints'].keys():
        Options['StNode'].append(nodeIdFromXY(Options['StartPoints'][ky]['lat'], \
        Options['StartPoints'][ky]['lon'], nodes));
    Options['EnNode']=[];
    for ky in Options['EndPoints'].keys():
        Options['EnNode'].append(nodeIdFromXY(Options['EndPoints'][ky]['lat'], \
        Options['EndPoints'][ky]['lon'], nodes));
    return Options
    
def edgeMonteCarlo(nodes,links,totalCost,pathS,pathE,PrCnt,NumRuns,SngPathOpt,modelType):
    """Run Monte Carlo Dijkstra simulation for input start and end nodes.
    
    Solves least cost path for a graph and perturbs the weights to traverse
    each arc in the graph.  Iterates to produce a set of simulations.
    Uses several NetworkX methods, as well as 'makeWeightedDiGraph', 
    'updateDiGraphCosts', and 'traceNodesBack'.
    
    Returns: simDetails <type 'dict'>
    """    
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    print('%% Monte Carlo Simulation. %%')
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    print(' ')
    print('Working...')
    print(' ');
    ##Monte Carlo simulation steps
    StartTime=tm.asctime();
    if NumRuns>500: 
        displayCount=25;
    elif NumRuns>=100 and NumRuns<=500:
        displayCount=10;
    elif NumRuns>10 and NumRuns<100:
        displayCount=5;
    else:
        displayCount=1;
    
    ##Make graph
    grph = makeWeightedDiGraph(nodes,links);
    #grph = makeWeightedGraph(nodes,links,totalCost);
    
    simResults = {}
    for z in range(0,np.int(NumRuns)):
        if z == 0:
            [pred, dist] = nx.dijkstra_predecessor_and_distance(grph,pathS,weight='weight');
        else:
            #totalCost = links[:,3]
            costModifier=PrCnt*totalCost*(2*np.random.random(size=totalCost.shape)-1);
            pertCosts=np.ones((costModifier.shape[0],3));
            pertCosts[:,0] = links[:,1];
            pertCosts[:,1] = links[:,2];
            pertCosts[:,2] = totalCost+costModifier;
            grph = updateDiGraphCosts(grph,pertCosts);
            [pred, dist] = nx.dijkstra_predecessor_and_distance(grph,pathS,weight='weight')
        if np.mod(z,displayCount)==0:
            print(tm.asctime() + ' Simulation No: ' + str(z));
        paths=[];
        pCosts=[];
        for ep in pathE:
            [path,pathCost] = traceNodesBack(pred,dist,pathS,ep);
            #if SngPathOpt==1:      ##Option to return only one least cost route
            paths.append(path);
            pCosts.append(pathCost);
            #Routes=[Routes; ones(length(path),1)*(z+(i/10)) path'];  ##Write routes 
            ##I'm here
        simResults.update({z:{'paths':paths,'costs':pCosts}})
    
    #for single path option, look through results and identify least cost single route
    if SngPathOpt==1:
        for sm in simResults.keys():
            minCost = np.array(simResults[sm]['costs']).min()
            minIdx = np.nonzero(np.array(simResults[sm]['costs']) == minCost)[0][0]
            minPath = simResults[sm]['paths'][minIdx]
            simResults[sm].update({'costs':[minCost],'paths':[minPath]})
    
    #Combine all simulation details        
    simDetails = {}
    simDetails.update({'startNode':pathS,'endNode':pathE,'valMaxVar':PrCnt, \
    'numSims':NumRuns,'numRoutes':(len(pathE) * NumRuns)});
    simDetails.update({'simResults':simResults})
    simDetails.update({'modelType':modelType})
    EndTime=tm.asctime();
    print('Done.');
    print(' ');
    print('Number of simulations: ');
    print(NumRuns);
    print('Number of successful routes: ');
    print(len(pathE) * NumRuns);
    print('Total Process Time:');
    print(StartTime + ' to ' + EndTime)
    return simDetails
    
def startSimulation(Options,nodes,links,totalCost):
    """Run simulation based on model type.
    
    Start a specific simulation style based on model type.  
    Uses 'edgeMonteCarlo'.
    
    Returns: Results <type 'list'>
    """            
    Results=[];
    #Regular or Agent type simulation. Connects each start node to all end nodes.
    if Options['ModelType']==1 or Options['ModelType']==3:
        print("******1 or 3********")
        for i in range(0,len(Options['StNode'])):
            print(tm.asctime() + ' Running simulation for start point ' + str(i));
            Results.append(edgeMonteCarlo(nodes,links,totalCost, \
            Options['StNode'][i],Options['EnNode'],Options['PrCnt'], \
            Options['NumRuns'],Options['SngPathOpt'],Options['ModelType']));
    #Modified type simulation. Connects each start node to each end node.
    elif Options['ModelType']==2:
        print("******2********")
        for i in range(0,len(Options['StNode'])):
            print(tm.asctime() + ' Running simulation for start point ' + str(i));
            endNode = [Options['EnNode'][i]];
            Results.append(edgeMonteCarlo(nodes,links,totalCost, \
            Options['StNode'][i],endNode,Options['PrCnt'], \
            Options['NumRuns'],Options['SngPathOpt'],Options['ModelType']));    
    return Results
    
def routeDetails(singleSimulation):
    """Calculate usage statistics for every edge of a route.
    
    Returns: segmentStats <type 'dict'>
    """         
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    print('%% Calculating segment statistics. %%')
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    print(' ')
    print('Working...')
    ssPaths = singleSimulation['simResults']
    allNodes = []
    for ky in ssPaths.keys():
        for pth in ssPaths[ky]['paths']:
            for i in range(0,len(pth)-1):
                allNodes.append((int(pth[i]),int(pth[i+1])));
    segmentStats = []
    uniqueNodes = list(set(allNodes));        
    for uNd in uniqueNodes:
        frq = allNodes.count(uNd);
        prc = (frq / (singleSimulation['numSims']*len(singleSimulation['endNode']))) * 100;
        segStat = (uNd[0],uNd[1],frq,prc);
        segmentStats.append(segStat)
    print(' ')
    print('Done.')
    print(' ')
    print('Total Time: ')
    #disp(datestr((EndTime-StartTime),13));
    return segmentStats