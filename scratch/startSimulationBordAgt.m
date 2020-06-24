%% Clear old values
clear Results

%% Calculate start and end nodes and run simulation
disp([datestr(now,14),' Calculating Start and End nodes.']);
Options.StNode=[];
for j=1:size(Options.StartPoint,1)
    Options.StNode(j)= NodeIDFromXY(Options.StartPoint(j,2), Options.StartPoint(j,1), nodes);
end
Options.EnNode=[];
for j=1:size(Options.EndPoint,1)
  Options.EnNode(j) = NodeIDFromXY(Options.EndPoint(j,2), Options.EndPoint(j,1), nodes);
end  
clear j

%%Iterate for Border Agent
StartNodes=Options.StNode;
for z=1:size(StartNodes,2)
  Options.StNode=StartNodes(z);
  Options.StartLabel={num2str(StartNodes(z))};
  % Simulation
  Results=cell(1,length(Options.StNode));
  for i=1:length(Options.StNode)
      disp([datestr(now,14),' Running simulation for start point ' int2str(i)]);
      %%[Results{i}.Routes,Results{i}.SimDetails] = EdgeMonteCarlo(nodes,links,totalCost,Options.StNode(i),Options.EnNode,Options.PrCnt,Options.NumRuns);
      [Results{i}.Routes,Results{i}.SimDetails] = EdgeMonteCarlo(nodes,links,totalCost,Options.StNode(i),Options.EnNode,Options.PrCnt,Options.NumRuns,Options.SngPathOpt);
  end
  clear i;

  % Recover Information
  disp([datestr(now,14),' Sorting results.']);
  for i=1:length(Options.StNode)
      Results{i}.SegmentStats=RouteDetails(Results{i}.SimDetails,Options,i);
  end
  clear i;

  % Write out to file
  disp([datestr(now,14),' Writing details out to file.']);
  dirToWrite='./';
  if outputFolderExists() dirToWrite='./output/'; end
  %%Uncomment for KML start points%%%filename=[dirToWrite,datestr(now,30),'-StartPoints.kml'];
  %%Uncomment for KML start points%%%writePointsToKML(Options.StartPoint,Options.StartLabel,filename);
  %%Uncomment for KML end points%%%filename=[dirToWrite,datestr(now,30),'-EndPoints.kml'];
  %%Uncomment for KML end points%%%writePointsToKML(Options.EndPoint,Options.EndLabel,filename);
  for i=1:length(Options.StNode)
      filename=[dirToWrite,datestr(now,30),'-SegmentStats-',int2str(i),'.txt'];
      WriteSegmentDetails(nodes,Results{i}.SegmentStats,filename);
      %%%Uncomment for KML%%%
      filename=[dirToWrite,datestr(now,30),'-SegmentStats-',int2str(i),'.kml'];
      %%%Uncomment for KML%%%
      writeSegmentStatsToKML(nodes,Results{i}.SegmentStats,filename);
  end
  %%Uncomment for Options File%%%filename=[dirToWrite,datestr(now,30),'-Options.txt'];
  %%Uncomment for Options File%%%writeOptionsToText(Options,filename);
  %%Uncomment for Options File%%%filename=[dirToWrite,datestr(now,30),'-Options.mat'];
  %%Uncomment for Options File%%%save(filename,'Options');
  clear filename i dirToWrite;
  disp([datestr(now,14),' Model run complete.']);
end
