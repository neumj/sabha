import time as tm
import numpy as np
import networkx as nx
from sabha.fileio import arcAsciiImport
from sabha.fileio import arcPtsToEdges
from sabha.execution import makeRegularNetworkMatrix
from sabha.execution import travelDirection
from sabha.execution import shrinkNetwork
from sabha.execution import makeWeightedDiGraph
from sabha.execution import nodeIdFromXY
from sabha.execution import startendPointsToNodes
from sabha.execution import traceNodesBack
from sabha.execution import updateDiGraphCosts
from sabha.execution import startSimulation
from sabha.execution import edgeMonteCarlo
from sabha.execution import routeDetails
from sabha.fileio import writeSegmentDetailsTxt
from sabha.fileio import writeSegmentDetailsKml
#def funCalls(optionsDict):
#    """Call all functions to run model. 
#    
#    Verifys and modifles parameters of Options file as well as input data.
#    
#    Returns: Options <type 'dict'>
#    """    
startTime=tm.asctime();
## Set parameters for slope (if present)
slopes=False;
for cs in Options['Costs']:
    if cs['type']==1 or cs['type']==2:
        slopes=True;
    
#%if slopes==true && Options.defaultSlopeValues~=4
#%    Options.areaSteepness=.05;
#%    switch Options.typeLinearSlopeTransform
#%        case 1 % Hiking Function
#%        case 2 % Splined Asymmetric
#%
#%    end
#%end
## Load Cost Rasters
print tm.asctime() + ' Loading raster cost surfaces.';
if Options['CstOpt']==1:
    Rasters=[];
    for cs in Options['Costs']:  # Iterate through list and load each raster.
        print tm.asctime() + ' Importing Ascii Raster';
        Raster = arcAsciiImport(cs['Filename']);
        Rasters.append(Raster);
print tm.asctime() + ' Finished loading raster cost surfaces.'

## Find maximum extent that all Rasters overlap
print tm.asctime() + ' Finding maximum extent common to all rasters.';
for i in range(0,len(Rasters)):
    if i==0:
        Options['RasterMaxLat']=Rasters[0]['Yurcorner'];
        Options['RasterMaxLon']=Rasters[0]['Xurcorner'];
        Options['RasterMinLat']=Rasters[0]['Yllcorner'];
        Options['RasterMinLon']=Rasters[0]['Xllcorner'];
    else:
        Options['RasterMaxLat'] = min(Options['RasterMaxLat'],Rasters[i]['Yurcorner']);
        Options['RasterMaxLon'] = min(Options['RasterMaxLon'],Rasters[i]['Xurcorner']);
        Options['RasterMinLat'] = max(Options['RasterMinLat'],Rasters[i]['Yllcorner']);
        Options['RasterMinLon'] = max(Options['RasterMinLon'],Rasters[i]['Xllcorner']);

## Find maximum resolution raster
Options['maxRasterResolution']=Inf;
for cs in Rasters:
    Options['maxRasterResolution'] = min(Options['maxRasterResolution'],cs['Cellsize']);

## Find network extent
if Options['GeoLim'] == 1:
    print tm.asctime() + ' Creating network with extents specified by the user.'
    #Nothing actually needs to be done here, since these points are provided.
elif Options['GeoLim'] == 2:
    print tm.asctime() + ' Creating network with extents defined by the raster.'
    Options['xlow']  = Options['RasterMinLon']
    Options['xhigh'] = Options['RasterMaxLon']
    Options['ylow']  = Options['RasterMinLat']
    Options['yhigh'] = Options['RasterMaxLat']
elif Options['GeoLim'] == 3:
    print 'Creating network with extents defined by the start and end points.'
    # Initially, set extent of the network to max/min of point values
    spArr = np.zeros((len(Options['StartPoints']),2))
    for i in range(0,len(Options['StartPoints'])):
        spArr[i,0] = Options['StartPoints'][Options['StartPoints'].keys()[i]]['lon']
        spArr[i,1] = Options['StartPoints'][Options['StartPoints'].keys()[i]]['lat']
    epArr = np.zeros((len(Options['EndPoints']),2))
    for i in range(0,len(Options['EndPoints'])):
        epArr[i,0] = Options['EndPoints'][Options['EndPoints'].keys()[i]]['lon']
        epArr[i,1] = Options['EndPoints'][Options['EndPoints'].keys()[i]]['lat']
    Options['xlow'] = min(spArr[:,0].min(),epArr[:,0].min());
    Options['xhigh'] = max(spArr[:,0].min(),epArr[:,0].min());
    Options['ylow'] = min(spArr[:,1],epArr[:,1]);
    Options['yhigh'] = max(spArr[:,1],epArr[:,1]);
        
    #Add 10%, and check for case when points are nearly in a line
    xdiff1 = (Options['xhigh'] - Options['xlow']);
    ydiff1 = (Options['yhigh'] - Options['ylow']);
    xscalefactor = 0.1;
    yscalefactor = 0.1;
    if xdiff1/ydiff1 < .25:
        xscalefactor=(ydiff1/xdiff1)/8;
    if ydiff1/xdiff1 < .25:
        yscalefactor=(xdiff1/ydiff1)/8;
    print tm.asctime() + ' Scaling factors: ' + str(xscalefactor) + ',' + str(yscalefactor);
    xadd = xscalefactor*xdiff1;
    yadd = yscalefactor*ydiff1;
    Options['xlow']=Options['xlow']-xadd;
    Options['xhigh']=Options['xhigh']+xadd;
    Options['ylow']=Options['ylow']-yadd;
    Options['yhigh']=Options['yhigh']+yadd;

#Find network width and height
maxWidthPossible = round(((Options['RasterMaxLon']-Options['RasterMinLon']) / \
    Options['maxRasterResolution'])+1);
maxHeightPossible = round(((Options['RasterMaxLat']-Options['RasterMinLat']) / \
    Options['maxRasterResolution'])+1);
if Options['typeWidth']<=0 or Options['typeWidth']==1:
    #Make network size equal to the full extent possible for Rasters
    Options['width']  = maxWidthPossible;
    Options['height'] = maxHeightPossible;
elif Options['typeWidth']>1:
    #Use values specified by the user
    Options['width']  = Options['typeWidth'];
    Options['height'] = Options['typeHeight'];
else:
    #Scale values as specified by the user
    Options['width']  = floor(Options['typeWidth']*maxWidthPossible);
    Options['height'] = floor(Options['typeHeight']*maxHeightPossible);

#Actually make or load the network
print tm.asctime() + ' Initial Network Size: ' + str(Options['height']) + ',' + str(Options['width']);
print tm.asctime() + ' Loading/Creating Network';
if Options['NetOpt']==1:
    [nodes,links] = arcPtsToEdges(Options['NetFile']);
else:
    [nodes,links] = makeRegularNetworkMatrix(Options['width'],Options['height'],Options['type'],Options['xlow'],Options['ylow'],Options['xhigh'],Options['yhigh']);        

#Replace Start/ End Points with Network Nodes 
if Options['ModelType']==3:
    if Options['StEnPts']==1:
        [Options['StartPoints'], Options['EndPoints']] = travelDirection(Options['Direction'],Options['width'],nodes,Options['height']);

#Shrink Network to raster bounds
print tm.asctime() + ' Checking network to see if trimming is necesary.';
if Options['CstOpt']==1: 
    maxLat=nodes[:,2].max();
    maxLon=nodes[:,1].max();
    minLat=nodes[:,2].min();
    minLon=nodes[:,1].min();
    if maxLat > Options['RasterMaxLat'] or minLat < Options['RasterMinLat'] or \
    maxLon > Options['RasterMaxLon'] or minLon < Options['RasterMinLon']:
        print tm.asctime() + ' Network is outside of the bounds of raster.  Shrinking Network.'
        [nodes, links] = shrinkNetwork(nodes,links,Options['RasterMinLon'],Options['RasterMinLat'],Options['RasterMaxLon'],Options['RasterMaxLat']);
    else:
        print tm.asctime() + ' No trimming necessary.'

## Replace NaNs in Raster with some value;
if Options['CstOpt']==1:
    print tm.asctime() + ' Checking raster values for NaN.'
    for i in range(0,len(Rasters)):
        #averagevalue = nanmean(np.reshape(Rasters[i]['Image'],(Rasters[i]['NCols']*Rasters[i]['NRows'],1)));
        maxvalue = np.max(np.reshape(Rasters[i]['Image'],Rasters[i]['NCols']*Rasters[i]['NRows'],1));
        locatenan = np.nonzero(Rasters[i]['Image'] == Rasters[i]['Nodata_value']);
        Rasters[i]['Image'][locatenan]=maxvalue;

#Calculate edge costs
print tm.asctime() + ' Calculating edge costs.';
#if strcmp(computer,'PCWIN') | strcmp(computer,'PCWIN64')
#    javaclasspath i:\gapt\gapt_projects\neumann\VEGAS_MobilityModel\code\java
#    import i:\gapt\gapt_projects\neumann\VEGAS_MobilityModel\code\java\calcEdgeCostJ2.*
#else
#    javaclasspath /gac/gapt/gapt_projects/neumann/VEGAS_MobilityModel/code/java
#    import /gac/gapt/gapt_projects/neumann/VEGAS_MobilityModel/code/java/calcEdgeCostJ2.*
#end
print tm.asctime() + ' Calculating Distance';
#Costs=cell(2,length(Rasters)+1);
#gcDistance = calcEdgeCostJ2.calc(int32(nodes(:,1)),nodes(:,2),nodes(:,3),links(:,2),links(:,3),ones(2,2),ones(7,1),1)';
#Costs{1,1} = single(gcDistance(:,1));
#clear gcDistance;
#
#%Costs{1,1} = single(calcEdgeCostM(nodes,links,1)); % Calculate absolute distance;
#if Options.CstOpt~=2
#    for i=1:length(Options.Costs)
#        if Options.Costs{i}.type==2 type=3; % Translate between Options type and calcEdgeCostJ type
#        else type=2;
#        end
#        disp([datestr(now,14),' Calculating edge costs for surface ',int2str(i),' using type ',int2str(type)]);
#        %averageValue = calcEdgeCostJ.calc(nodes',links',Rasters{i}.Image,getRasterInfo(Rasters{i}),type)';
#        averageValue = calcEdgeCostJ2.calc(int32(nodes(:,1)),nodes(:,2),nodes(:,3),links(:,2),links(:,3),single(Rasters{i}.Image),getRasterInfo(Rasters{i}),type)';
#        Costs{1,i+1} = single(averageValue(:,1)); % First column is data, second column is number of pixels which we do not need now
#        clear averageValue type;
#    end
#end
#clear i;

#%% Do numerical transformations for slope
#applyCostTransforms
#
#%% Combine Costs to single cost value
#calcTotalEdgeCost
totalCost = links[:,3];

#Calculate closest nodes to start/end pts
print tm.asctime() + ' Calculating Start and End nodes.';
Options = startendPointsToNodes(Options,nodes)

#Run simulation and output results
allSimulations=startSimulation(Options,nodes,links,totalCost);

#Recover information
print tm.asctime() + ' Sorting results.';
for i in range(0,len(Options['StNode'])):
    singleSimulation = allSimulations[i]
    segmentStats = routeDetails(singleSimulation); 
    allSimulations[i].update({'segmentStatistics':segmentStats})    
    
#Write file
outPath = "C:\\Users\\Ben\\Documents\\code\\python\\routing";
print tm.asctime() + ' Writing details out to file.';
for i in range(0,len(Options['StNode'])):
    singleSimulation = allSimulations[i];
    writeSegmentDetailsTxt(outPath,singleSimulation,nodes); 
    writeSegmentDetailsKml(outPath,singleSimulation,nodes);
    
endTime=tm.asctime();
print 'Model ran from ' + startTime + ' to '  + endTime;
print tm.asctime() + ' Model run complete.';
