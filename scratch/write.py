# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 11:55:19 2013

@author: Ben
"""
def writeSegmentDetailsTxt(outPath,singleSimulation,nodes):
    tm.sleep(0.125)
    wTm = tm.strftime("%Y%m%d%H%M%S", tm.gmtime()) + str(tm.time()).split('.')[1]
    filePath = outPath + "\\" + "sabha_" + wTm + ".txt"
    toWrite = [['PtX01','PtY01','PtX02','PtY02','Freq','PrCnt']]
    for stat in singleSimulation['segmentStatistics']:
        ndIdx01 = stat[0] - 1
        ndIdx02 = stat[1] - 1
        toWrite.append([nodes[ndIdx01,1],nodes[ndIdx01,2], \
        nodes[ndIdx02,1],nodes[ndIdx02,2],stat[2],stat[3]])
    with open(filePath, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(toWrite) 

