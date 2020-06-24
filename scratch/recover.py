def routeDetails(singleSimulation):

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