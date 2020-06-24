# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 14:58:50 2013

@author: Ben
"""

def writeSegmentDetailsKml(outPath,singleSimulation,nodes):
    """Write simulation segment statistics to KML file.
    
    Outputs a comma separated text file with a two line header.  
    Header01: #modelType: 1, 2, or 3
    Header02: #POINT_X1,POINT_Y1,POINT_X2,POINT_Y2,FREQ,PRCNT
    
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


<Placemark>
    <name>Polyline 1</name>
    <description>This is some info about polyline 1</description>

    <Style>
      <LineStyle>
        <color>ff00ff00</color>
        <width>6</width>
      </LineStyle>
    </Style>

    <LineString>
      <coordinates>-122.1,37.4,0 -122.0,37.4,0 -122.0,37.5,0 -122.1,37.5,0 -122.1,37.4,0


