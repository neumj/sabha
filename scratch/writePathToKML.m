function [] = writePathToKML(nodes,netpath,filename)

ArcFormat=nodes(netpath,2:3);
ArcFormat=[ArcFormat, ones(length(ArcFormat),1)]';
fid=fopen(filename,'wt');
fprintf(fid,'<Placemark>\n');
fprintf(fid,'<LineString>\n');
fprintf(fid,'<coordinates>\n');
fprintf(fid,'%6.8f,%6.8f,%3.1f\n',ArcFormat);
fprintf(fid,'</coordinates>\n');
fprintf(fid,'</LineString>\n');
fprintf(fid,'</Placemark>\n');
fclose(fid);