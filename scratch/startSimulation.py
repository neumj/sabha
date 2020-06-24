



##Simulation
Results=[];
totalCost = links[:,3]
#Regular or Agent type simulation. Connects each start node to all end nodes.
if Options['ModelType']==1 or Options['ModelType']==3:
    for i in range(0,len(Options['StNode'])):
        print tm.asctime() + ' Running simulation for start point ' + str(i);
        Results.append(edgeMonteCarlo(nodes,links,totalCost, \
        Options['StNode'][i],Options['EnNode'],Options['PrCnt'], \
        Options['NumRuns'],Options['SngPathOpt'],Options['ModelType']));
elif Options['ModelType']==2:
    print '2'
    for i in range(0,len(Options['StNode'])):
        print tm.asctime() + ' Running simulation for start point ' + str(i);
        endNode = [Options['EnNode'][i]];
        Results.append(edgeMonteCarlo(nodes,links,totalCost, \
        Options['StNode'][i],Options['EnNode'],Options['PrCnt'], \
        Options['NumRuns'],Options['SngPathOpt'],Options['ModelType']));    


###Recover Information
#print tm.asctime + ' Sorting results.';
#for i in range(0,len(Options['StNode'])):
#    Results{i}.SegmentStats=RouteDetails(Results{i}.SimDetails,Options,i);
#end
#clear i;
#
#%% Write out to file
#disp([datestr(now,14),' Writing details out to file.']);
#dirToWrite='./';
#if outputFolderExists() dirToWrite='./output/'; end
#%%Uncomment for KML start points%%%filename=[dirToWrite,datestr(now,30),'-StartPoints.kml'];
#%%Uncomment for KML start points%%%writePointsToKML(Options.StartPoint,Options.StartLabel,filename);
#%%Uncomment for KML end points%%%filename=[dirToWrite,datestr(now,30),'-EndPoints.kml'];
#%%Uncomment for KML end points%%%writePointsToKML(Options.EndPoint,Options.EndLabel,filename);
#for i=1:length(Options.StNode)
#    filename=[dirToWrite,datestr(now,30),'-SegmentStats-',int2str(i),'.txt'];
#    WriteSegmentDetails(nodes,Results{i}.SegmentStats,filename);
#    %%%Uncomment for KML%%%
#    filename=[dirToWrite,datestr(now,30),'-SegmentStats-',int2str(i),'.kml'];
#    %%%Uncomment for KML%%%
#    writeSegmentStatsToKML(nodes,Results{i}.SegmentStats,filename);
#end
#%%Uncomment for Options File%%%filename=[dirToWrite,datestr(now,30),'-Options.txt'];
#%%Uncomment for Options File%%%writeOptionsToText(Options,filename);
#%%Uncomment for Options File%%%filename=[dirToWrite,datestr(now,30),'-Options.mat'];
#%%Uncomment for Options File%%%save(filename,'Options');
#clear filename i dirToWrite;
#disp([datestr(now,14),' Model run complete.']);
