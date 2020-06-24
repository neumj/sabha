#function [path,pathcost] = traceBack(predecessors,distance,startNode,endNode)  % pass in a vector of previous nodes and a start and end point

endNode = 100
startNode = 1
predecessor = pred
distance = dist

n=endNode;
path = [];
#cost = [];
while predecessor[n]!=[]:
    path.append(n);
    #cost=[cost; d(n)];
    n=predecessor[n][0];
path.append(startNode)
path.reverse()
pathCost = dist[endNode]   
 # pathcost=sum(cost);
  
#elseif Opt==2
[100, 89.0, 78.0, 67.0, 56.0, 45.0, 34.0, 23.0, 12.0, 1]

grph[100][89]['weight'] + grph[89][78]['weight'] + grph[78][67]['weight'] + \
grph[67][56]['weight'] + grph[56][45]['weight'] + grph[45][34]['weight'] + \
grph[34][23]['weight'] + grph[23][12]['weight'] + grph[12][1]['weight']

grph[1][12]['weight'] + grph[12][23]['weight'] + grph[23][34]['weight'] + \
grph[34][45]['weight'] + grph[45][56]['weight'] + grph[56][67]['weight'] + \
grph[67][78]['weight'] + grph[78][89]['weight'] + grph[89][100]['weight']