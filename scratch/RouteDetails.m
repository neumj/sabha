function [SegmentStats] = RouteDetails(SimDetails,Options,position);
disp('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
disp('%% Calculating segment statistics. %%')
disp('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
disp(' ')
disp('Working...')
StartTime=now;
Sgmnts=sortrows([SimDetails.Routes((1:size(SimDetails.Routes,1)-1),2) SimDetails.Routes(2:size(SimDetails.Routes,1),2)]);
NodSet=[Options.EnNode' ones(size(Options.EnNode,2),1)*Options.StNode(position); ones(size(Options.EnNode,2),1)*Options.StNode(position) Options.EnNode'];  
Pos=ismember(Sgmnts,NodSet,'rows');
Sgmnts(find(Pos==1),:)=[];
SegmentStats.UnqSegments=[unique(Sgmnts,'rows')]; 
Vals=sortrows(Sgmnts(:,1)+(Sgmnts(:,2)/(max(max(Sgmnts)))));
UVals=unique(Vals);
SegmentStats.Freq=hist(Vals,UVals)';
SegmentStats.Percent=[(SegmentStats.Freq/(Options.NumRuns*size(Options.EnNode,2)))*100];

EndTime=now;
disp(' ')
disp('Done.')
disp(' ')
disp('Total Time: ')
disp(datestr((EndTime-StartTime),13));

clear Vals i Sgmnts StartTime EndTime


