def edgeMonteCarlo(nodes,links,totalCost,pathS,pathE,PrCnt,NumRuns,SngPathOpt,modelType):
    """Run Monte Carlo Dijkstra simulation for input start and end nodes.
    
    Solves least cost path for a graph and perturbs the weights to traverse
    each arc in the graph.  Iterates to produce a set of simulations.
    Uses several NetworkX methods, as well as 'makeWeightedDiGraph', 
    'updateDiGraphCosts', and 'traceNodesBack'
    
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
            print tm.asctime() + ' Simulation No: ' + str(z);
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
            simResults[sm].update({'costs':[minCost],'paths':minPath})
    
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
    print StartTime + ' to ' + EndTime
    disp(' ')
    return simDetails
