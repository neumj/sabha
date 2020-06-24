%%Function to run Monte Carlo simulation 

function [Routes,SimDetails] = EdgeMonteCarlo(nodes,links,totalCost,pathS,pathE,PrCnt,NumRuns,SngPathOpt);

disp('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
disp('%% Monte Carlo Simulation. %%')
disp('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
disp(' ')
disp('Working...')
disp(' ');
StartTime=now;

%%Monte Carlo simulation steps
Routes=[];
distances=zeros(length(nodes),1);

%Java Dijkstra Requirement
if strcmp(computer,'PCWIN')==1 | strcmp(computer,'PCWIN64') == 1
    javaaddpath I:\gapt\gapt_projects\neumann\VEGAS_MobilityModel\code\java
else
    javaaddpath /gac/gapt/gapt_projects/neumann/VEGAS_MobilityModel/code/java
end

import Graph.*
import dijkstraJ.*
graph = Graph(int32(links(:,2)),int32(links(:,3)),totalCost);

if NumRuns>500 displayCount=25;
elseif NumRuns>=100 && NumRuns<=500 displayCount=10;
elseif NumRuns>10 && NumRuns<100 displayCount=5;
else displayCount=1;
end
Dist = cell(1,NumRuns);
for z=1:NumRuns
  costModifier=PrCnt*totalCost.*(2*rand(size(totalCost))-1);
  costs=totalCost+costModifier;
  graph.updateCosts(costs);
  if mod(z,displayCount)==0
    disp([datestr(now,14),' Simulation No: ',int2str(z)])
  end
  resultsJ=dijkstraJ.findPath(graph,pathS);
  d=resultsJ(:,2);
  p=resultsJ(:,3);
  clear resultsJ;
  paths={};
  pcosts=[];
  for i=1:size(pathE,2)
    [path,pathcost]=traceBack(p,d,pathS,pathE(i)); %%Build node path for route
    if SngPathOpt==1      %%Option to return only one least cost route
      paths=[paths; path];
      pcosts=[pcosts; pathcost];
    end
    Routes=[Routes; ones(length(path),1)*(z+(i/10)) path'];  %%Write routes 
    clear path    
  end
  if SngPathOpt==1  
    pcosts=pcosts';
    [pmin,minloc]=min(pcosts);
    path=paths{minloc};
    Routes=[];
    Routes=[Routes; ones(length(path),1)*(z+(i/10)) path'];  %%Write routes 
    clear path
  end
end
%distances=distances/NumRuns;
UsedNodes=(unique(Routes(:,2)));
EndTime=now;
Time=EndTime-StartTime;
disp('Done.');
disp(' ');
disp('Number of simulations: ');
disp(NumRuns);
disp('Number of successful routes: ');
disp(length(unique(Routes(:,1))));
disp('Total Process Time:');
disp(datestr(Time,13));
disp(' ')
SimDetails=struct('StartNode',pathS,'EndNode',pathE,'ValMaxVar',PrCnt,'NumSims',NumRuns,'NumRoutes',length(unique(Routes(:,1))),'Routes',Routes);
SimDetails.distances=distances(pathE);
clear distances Cls MInf Negs Pert PertRaster PosNeg PrCnt Rws r_path transmat z NumRuns pathE pathS ObsIndex StartTime EndTime Time
clear PertMatrix PrepEnd PrepStart RtEnd RtStart Zrs