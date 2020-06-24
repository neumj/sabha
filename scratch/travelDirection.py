import numpy as np
def travelDirection(direction,width,nodes,height):
    height = int(height);
    width = int(width)
    stPts = {}
    enPts = {}
    if direction==1 or direction==2:
        SPts=nodes[0:width,:];
        NPts=nodes[((np.shape(nodes)[0])-(width)):(np.shape(nodes)[0]),:];
        if direction==1:
            for ln in NPts:
                stPts.update({int(ln[0]):{'lat':ln[2],'lon':ln[1]}})
            for ln in SPts:
                enPts.update({int(ln[0]):{'lat':ln[2],'lon':ln[1]}})
        elif direction==2:  
            for ln in SPts:
                stPts.update({int(ln[0]):{'lat':ln[2],'lon':ln[1]}})
            for ln in NPts:
                enPts.update({int(ln[0]):{'lat':ln[2],'lon':ln[1]}})
    elif direction==3 or direction==4:
        ETargets=np.arange((height-1),np.shape(nodes)[0]+1,height);
        EPts=nodes[ETargets,:];
        WTargets=np.arange(0,(np.shape(nodes)[0]-height)+1,height);
        WPts=nodes[WTargets,:];
        if direction==3:
            for ln in EPts:
                stPts.update({int(ln[0]):{'lat':ln[2],'lon':ln[1]}})
            for ln in WPts:
                enPts.update({int(ln[0]):{'lat':ln[2],'lon':ln[1]}})
        elif direction==4:  
            for ln in WPts:
                stPts.update({int(ln[0]):{'lat':ln[2],'lon':ln[1]}})
            for ln in EPts:
                enPts.update({int(ln[0]):{'lat':ln[2],'lon':ln[1]}})
    return stPts, enPts