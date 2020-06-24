function [] = writePointsToKML(point,label,filename)

if nargin==2
    filename=label;
end
fid=fopen(filename,'wt');
fprintf(fid,'<Document>\n');
for i=1:size(point,1)
    fprintf(fid,'<Placemark>\n');
    if nargin>2
        fprintf(fid,['<name>',label{i},'</name>\n']);
    end
    fprintf(fid,'<Point>\n');
    fprintf(fid,'<coordinates>');
    fprintf(fid,[num2str(point(i,1)),',',num2str(point(i,2))]);
    fprintf(fid,'</coordinates>\n');
    fprintf(fid,'</Point>\n');
    fprintf(fid,'</Placemark>\n');
end
fprintf(fid,'</Document>\n');
fclose(fid);