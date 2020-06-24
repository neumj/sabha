# -*- coding: utf-8 -*-
import csv
def mobilityModelParameters():
    """Generate a model control Python dictionary from user input.
    
    Creates a Python dictionary with all model parameters and pointers to data.  
    
    Returns Options <type 'dict'>
    """
    ##########################################
    ###Mobility Model Control script.###
    ##########################################
    print(' ')
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    print('%%    Mobility Model.    %%')
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    print(' ')
    print(' ')
    print('%%%%%%%%%%%%%%%%%%%%%%%%')
    print('%% Define Model Type. %%')
    print('%%%%%%%%%%%%%%%%%%%%%%%%')
    print(' ')
    Options ={}
    print('1) Standard VEGAS Mobility Model');
    print('2) Iterative VEGAS Mobility Model');
    print('3) Agent Based VEGAS Mobility Model'); 
    Options['ModelType']=int(raw_input('Input model type: '));
    print(' ')
    if Options['ModelType']==1:
        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
        print('%%    Standard Mobility Model.    %%')
        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
        Options['SngPathOpt']=0;  ##Option to return only one least cost path for all possible end points.
    elif Options['ModelType']==2: 
        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
        print('%%    Iterative Mobility Model.    %%')
        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
        Options['SngPathOpt']=0;  ##Option to return only one least cost path for all possible end points.
    elif Options['ModelType']==3:
        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
        print('%%    Agent Based Mobility Model.    %%')
        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
        Options['SngPathOpt']=1;  #Option to return only one least cost path for all possible end points.
    print(' ')
    ##Cost Surface##
    print(' ')
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    print('%% Define Cost Surface(s). %%')
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    print(' ')
    print('Enter 1 to load a cost surface(s).')
    Options['CstOpt']=int(raw_input('Enter 2 for no cost surface (only use distance): '));
    if Options['CstOpt']==1:
        Options['Costs'] = []
        numCosts=int(raw_input('How many raster cost surfaces: '));
        wts = []
        for i in range(0,numCosts):
            csDict = {}
            csFilename=raw_input('Input file path (ex: c:\\data\\e32n35.mat or c:\\data\\e32n35.txt): ');
            csDict.update({'Filename':csFilename})
            print('Type of Raster: ');
            print('1) Area Based Slope');
            print('2) Linear Based Slope');
            print('3) Other / General');
            csType = int(raw_input('Input type of cost surface: '));
            csDict.update({'type':csType})
            wtVal=float(raw_input('Input weight in percent for this layer: '));
            wts.append(wtVal)
            Options['Costs'].append(csDict)
            print(' ');
        Options['weights'] = wts
    slopes=False;
    if Options['CstOpt']==1:
        for cs in Options['Costs']:
            if cs['type']==1 or cs['type']==2:
                slopes=True;
        if slopes==True:
            print('How to assess slope cost?');
            print('1) Hiking Function');
            Options['typeLinearSlopeTransform']=int(raw_input('2) Splined Asymmetric: '));
            print(' ');
            print('Type of travel:');
            print('1) Passenger Car');
            print('2) Heavy Off-Road Vehicle');
            print('3) Pedestrian / Animal');
            print('4) Custom define the parameters');
            Options['defaultSlopeValues'] = int(raw_input('Type of slope parameters to use: '));
            if Options['defaultSlopeValues']==4:
                Options.areaSteepness=float(raw_input('Steepness factor for areal slope calculation: '));
                if Options['typeLinearSlopeTransform']==1:
                    Options['linearSteepness']=float(raw_input('Steepness factor for linear slope calculation: '));
                    Options['linearSquareness']=float(raw_input('Squareness factor for linear slope calculation: '));
                    Options['linearAsymmetry']=float(raw_input('Asymmetry factor for linear slope calculation: ')); #%% Check this  %%
                else:
                    Options['breakpoint']=float(raw_input('Slope of Asymmetry: '));
                    Options['slopeCutoff']=float(raw_input('Slope at which travel is impossible: '));
                    Options['positiveScalingFactor']=float(raw_input('exp equation coefficient for positive slope values: '));
                    Options['negativeScalingFactor']=float(raw_input('exp equation coefficient for negatiev slope values: '));
    ##Network##
    print(' ')
    print('%%%%%%%%%%%%%%%%%%%%%')
    print('%% Define Network. %%')
    print('%%%%%%%%%%%%%%%%%%%%%')
    print(' ')
    print('Enter 1 to load a network.')
    Options['NetOpt']=int(raw_input('Enter 2 to create a regular network: '));
    if Options['NetOpt']==1:
        Options['NetFile']=raw_input('Input file path (ex: c:\\data\\Edges.txt): ');
        Options['GeoLim']=1;
        Options['typeWidth']=0;
        Options['typeHeight']=0;
    else:    
        print(' ');
        print('Input network size.');
        print('For a scaled value, input a value greater than 0 and less than or equal to 1.')
        print('Example: Input of .5 will create a network along the given dimension that is half the size of the largest raster.');
        print('Example: Input of 1 will create a network along the given dimension that is as large as the largest raster.');
        print('Example: Input of 200 will create a network of 200 nodes along the given dimension.');
        Options['typeWidth']=float(raw_input('Input network width: ')); 
        Options['typeHeight']=float(raw_input('Input network height: ')); 
        print('Input network type (default is Queen):')
        print('Enter 1 for Rook.')
        print('Enter 2 for Queen.')
        Options['type']=int(raw_input('Enter 3 for Knight: '));
        print('How do you want to define the limits of the network?');
        print('1) Custom');
        print('2) Extent of raster(s)');
        Options['GeoLim']=int(raw_input('3) Extent of Start/End Points: '));
        if Options['GeoLim']==1:
            Options['xlow']=float(raw_input('Input min X: '));
            Options['ylow']=float(raw_input('Input min Y: '));
            Options['xhigh']=float(raw_input('Input max X: '));
            Options['yhigh']=float(raw_input('Input max Y: '));
    ##Simulation##
    print(' ')
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    print('%%Define Starting/ Ending Points. %%')
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    print(' ')
    print('Define Start and End Points: ')
    print('1) Use network nodes');
    print('2) Load points from a file');
    Options['StEnPts']=int(raw_input('3) Manually enter points: '));
    print(' ')
    if Options['StEnPts']==1:
        print('%% Use network nodes %%')
        print('What direction should the agent travel?');
        print('1) North to South');
        print('2) South to North');
        print('3) East to West');
        Options['Direction']=int(raw_input('4) West to East: '));
    elif Options['StEnPts']==2:
        Options['StartPoints'] = {}
        Options['EndPoints'] = {}
        print('%% Load points from file %%')
        print('Starting Points: ');
        StPtFile=raw_input('Input start points file path (ex: c:\\data\\StartPoints.txt): ');
        fl = open(StPtFile, mode='r')
        csvReader = csv.reader(fl)
        for ln in csvReader:
            if ln[0] != 'PtId':
                Options['StartPoints'].update({ln[0]:{'lat':ln[1],'lon':ln[2]}})
        fl.close()
        print(' ')
        print('Ending Points: ');
        EnPtFile=raw_input('Input end points file path (ex: c:\\data\\EndPoints.txt): ');  
        fl = open(EnPtFile, mode='r')
        csvReader = csv.reader(fl)
        for ln in csvReader:
            if ln[0] != 'PtId':
                Options['EndPoints'].update({ln[0]:{'lat':ln[1],'lon':ln[2]}})
        fl.close()
        print(' ')
    elif Options['StEnPts']==3:
        Options['StartPoints'] = {}
        Options['EndPoints'] = {}
        print('%% Manually enter points %%')  
        NumSt=int(raw_input('Number of start points: '));
        for i in range(0,NumSt):
            ptID = int(raw_input('Please give a label for this point: '));
            lat = float(raw_input('Input start coordinate latitude: '));
            lon = float(raw_input('Input start coordinate longitude: '));
            Options['StartPoints'].update({ptID:{'lat':lat,'lon':lon}})
        print(' ')
        NumEn=int(raw_input('Number of end points: '));
        for i in range(0,NumEn):
            ptID = raw_input('Please give a label for this point: ');
            lat = float(raw_input('Input start coordinate latitude: '));
            lon = float(raw_input('Input start coordinate longitude: '));
            Options['EndPoints'].update({ptID:{'lat':lat,'lon':lon}})
    print(' ')
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    print('%% Define Monte Carlo Simulation. %%')
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    print(' ')
    Options['PrCnt']=float(raw_input('Maximum per cent of cost value perturbation: '));
    Options['PrCnt']=Options['PrCnt']/100;
    Options['NumRuns']=float(raw_input('Number of simulations (for each Start Location): '));
    return Options
    
#Options = mobilityModelParameters()
