# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 10:23:08 2024

@author: Nooria
"""
import os
from pcraster import *

def WithinDistance(raster,maxdistance):
    RestultWithDistance = spreadmaxzone(raster,0,1,maxdistance)
    return RestultWithDistance

def BeyondDistance(raster,mindistance):
    ResultBeyondDistance = ~ spreadmaxzone(raster,0,1,mindistance)
    return ResultBeyondDistance

# Change to data folder if needed
os.chdir('./data')

#Read all input maps
Buildings = readmap('buildg.map')
Roads = readmap('roads.map')
GWLevel = readmap('gwlevel.map')
DTM = readmap('dtm.map')

#Set thresholds for conditions
DistanceCondition1 = 150
DistanceCondition2 = 300
DepthCondition3 = 40

#condition 1: Wells within X meters of houses or roads
Houses = Buildings == 1
Houses150m = WithinDistance(Houses,DistanceCondition1)

IsRoad = Roads !=0
Roads150m = WithinDistance(IsRoad, DistanceCondition1)

#Condition 2: No Inustry, Mine or Landfill within X metters from Wells
Industry = lookupboolean('industry.tbl', Buildings)
IndustryMin300m = BeyondDistance(Industry, DistanceCondition2)


#Condition 3: Wells Less than X meters Deep
WelDepth = DTM - GWLevel
NoDeep = WelDepth < DepthCondition3

#Combine conditions
AccessibleWells = Houses150m & Roads150m & IndustryMin300m & NoDeep

# Write restuls to disk and visualize
report(AccessibleWells, 'accessiblewells.map')
aguila(AccessibleWells)


#plot(AccessibleWells,labels={0:'Not Accessinle', 1:'Accessible'}, Title='Wells',filename=None)









