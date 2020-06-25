# -*- coding: utf-8 -*-
import numpy as np
import json as js
import csv as csv
import time as tm

def arcAsciiImport(filePath):
    """Reads ArcGIS ASCII Grid file to Python dictionary.
    
    File should be a ArcGIS ASCII Grid.

    Returns: Raster <type 'dict'>
    """
    Raster ={}
    Raster['Filename'] = filePath
    fl = open(Raster['Filename'])
    print('Loading and parsing data.')
    print('Working...')
    lnCount = 0
    while lnCount < 6:
        rawLine = fl.readline()
        rawLine = rawLine.replace('\n','')
        if lnCount == 0:
            Raster['NCols'] = float(rawLine[5:len(rawLine)])
            print('Number of columns to process: ' + str(Raster['NCols']))
        elif lnCount == 1:
            Raster['NRows'] = float(rawLine[5:len(rawLine)])
            print('Number of rows to process: ' + str(Raster['NRows']))
        elif lnCount == 2:
            Raster['Xllcorner'] = float(rawLine[9:len(rawLine)])
        elif lnCount == 3:
            Raster['Yllcorner'] = float(rawLine[9:len(rawLine)])
        elif lnCount == 4:
            Raster['Cellsize'] = float(rawLine[8:len(rawLine)])
        elif lnCount == 5:
            Raster['Nodata_value'] = float(rawLine[12:len(rawLine)])
        lnCount = lnCount + 1
    fl.close()
    Raster['Xurcorner'] = Raster['Xllcorner'] + ((Raster['NCols'] -1) * Raster['Cellsize']);
    Raster['Yurcorner'] = Raster['Yllcorner'] + ((Raster['NRows'] - 1) * Raster['Cellsize']);
    Raster['Image'] = np.loadtxt(filePath, skiprows=6)
    return Raster

def arcPtsToEdges(filePath):
    """Converts ArcGIS generated paths to a network.
    
    Path file should be a comma separated text file with a one line header.  
    Header: LnId,Label,POINT_X1,POINT_Y1,POINT_X2,POINT_Y2

    Returns: nodes <type 'numpy.ndarray'>; links <type 'numpy.ndarray'>
    """
    #filePath = filePath = 'C:\\Users\\Ben\\Documents\\code\\python\\routing\\testNetwork.txt'
    print(' ')
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    print('%% Reading and processing edge vertices from ArcGIS output text file. %%')
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    print(' ')
    print('Working...')
    print(' ')
    print('Reading file...')
    print(' ')
    lnId, x1, y1, x2, y2 = np.loadtxt(filePath, delimiter=',', usecols=(0,2,3,4,5), skiprows=1, unpack=True)
    print('Creating Edges...')
    print(' ')
    verts01 = np.zeros((x1.shape[0],2))
    verts01[:,0] = x1
    verts01[:,1] = y1
    verts02 = np.zeros((x2.shape[0],2))
    verts02[:,0] = x2
    verts02[:,1] = y2
    allVerts=np.concatenate((verts01,verts02))
    d1Verts = np.concatenate((verts01,verts02),axis=1)
    d2Verts = np.concatenate((verts02,verts01),axis=1)
    arcVerts=np.concatenate((d1Verts,d2Verts),axis=0)
    avLst = allVerts.tolist()
    unqNodesLst=list(set([tuple(llPair) for llPair in avLst]))
    nodes=np.zeros((len(unqNodesLst),3))
    nodes[:,0] = np.arange(1,(len(unqNodesLst) + 1),1)
    nodes[:,1:nodes.shape[1]] = np.array(unqNodesLst)
    links = np.zeros((arcVerts.shape[0],4))
    links[:,0] = np.arange(1,(allVerts.shape[0] + 1),1)
    links[:,3] = 1
    for i in range(0,len(unqNodesLst)):
        #print unqNodesLst[i]
        for j in range(0,arcVerts.shape[0]):
            t1LL = (arcVerts[j,0],arcVerts[j,1])
            t2LL = (arcVerts[j,2],arcVerts[j,3])
            if t1LL == unqNodesLst[i]:
                #print "match" + " " + str(i) + " " + str(j)
                links[j,1] = (i+1)
            if t2LL == unqNodesLst[i]:
                #print "match" + " " + str(i) + " " + str(j)
                links[j,2] = (i+1)
    links=np.int32(links);
    print('Done.');
    return nodes,links

def read_json(file_path):
    """Read JSON file to Python dictionary.

    Returns d <type 'dict'>
    """
    with open(file_path) as json_data:
        d = json.load(json_data)
    return d


def write_json(data_dict,file_path):
    """Writes Python object to a JSON file.
    """
    with open(file_path, 'w') as fp:
        json.dump(data_dict, fp, indent=4)


def writeSegmentDetailsTxt(outPath,singleSimulation,nodes):
    """Write simulation segment statistics to text file.
    
    Outputs a comma separated text file with a two line header.  
    Header01: #modelType: 1, 2, or 3
    Header02: #POINT_X1,POINT_Y1,POINT_X2,POINT_Y2,FREQ,PRCNT
    
    No return.
    """    
    tm.sleep(0.125)
    wTm = tm.strftime("%Y%m%d%H%M%S", tm.gmtime()) + str(tm.time()).split('.')[1]
    filePath = outPath + "\\" + "sabha_" + wTm + ".txt"
    toWrite = [["#modelType: " + str(singleSimulation['modelType'])], \
    ['#POINT_X1','POINT_Y1','POINT_X2','POINT_Y2','FREQ','PRCNT']]
    for stat in singleSimulation['segmentStatistics']:
        ndIdx01 = stat[0] - 1
        ndIdx02 = stat[1] - 1
        toWrite.append([nodes[ndIdx01,1],nodes[ndIdx01,2], \
        nodes[ndIdx02,1],nodes[ndIdx02,2],stat[2],stat[3]])
    with open(filePath, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(toWrite) 

def writeSegmentDetailsKml(outPath,singleSimulation,nodes):
    """Write simulation segment statistics to KML file.
        
    No return.
    """    
    tm.sleep(0.125)
    wTm = tm.strftime("%Y%m%d%H%M%S", tm.gmtime()) + str(tm.time()).split('.')[1]
    filePath = outPath + "\\" + "sabha_" + wTm + ".kml"
    hdr = ['<?xml version="1.0" encoding="UTF-8"?>\n',
           '<kml xmlns="http://earth.google.com/kml/2.2">\n',
           '<Document>\n',
           '<name>Model Results</name>\n',
           '<description>Model Results</description>\n',
           '<Style>\n',
           '<LineStyle>\n',
           '<color>ff00ff00</color>\n',
           '<width>3</width>\n',
           '</LineStyle>\n',
           '</Style>\n',
           '<Placemark>\n',
           '<LineString>\n',
           '<coordinates>\n']
    fl = open(filePath, 'a')
    for hline in hdr:
        fl.write(hline)
    for stat in singleSimulation['segmentStatistics']:
            ndIdx01 = stat[0] - 1
            ndIdx02 = stat[1] - 1
            ndLin01 = str(nodes[ndIdx01,1]) + "," + str(nodes[ndIdx01,2]) + ",1\n"
            fl.write(ndLin01)
            ndLin02 = str(nodes[ndIdx02,1]) + "," + str(nodes[ndIdx02,2]) + ",1\n"
    ftr = ['</coordinates>\n',
           '</LineString>\n',
           '</Placemark>\n',
           '</Document>\n',
           '</kml>\n']
    for fline in ftr:
        fl.write(fline)
    fl.close()