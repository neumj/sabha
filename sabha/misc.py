# -*- coding: utf-8 -*-
"""
Created on Thu Nov 07 09:40:04 2013

@author: Ben
"""

import sys
sys.path.append('C:\Users\Ben\Documents\code\python')
import sabha
from sabha import *
Options = sabha.fileio.readJSON('C:\\Users\\Ben\\Documents\\code\\python\\routing\\optionsAgent.json')
Options['typeHeight'] = 10
Options['typeWidth'] = 10
Options['ModelType']=1
Options['SngPathOpt']=0