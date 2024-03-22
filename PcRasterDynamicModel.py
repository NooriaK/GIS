# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 21:15:19 2024

@author: Noori
"""
# precipitation (mm/10 days).
from pcraster import *
from pcraster.framework import *


class RunoffModel(DynamicModel):
    def __init__(self,cloneMap):
        DynamicModel.__init__(self)
        setclone(cloneMap)
        
      #  Read land-use map and soil map from disk (Static map with the .map file extension)  
    def initial(self):
        landuse = self.readmap("./Data/landuse")
        soil = self.readmap("./Data/soil")
        # Interception threshold data for different land-use types.
        self.InterceptionThreshold = lookupscalar("./Data/d.tbl",landuse)
        # Write the result to disk using self.report
        self.report(self.InterceptionThreshold,"./Data/d")
        
    # Make a global variable, by adding self (PCRaster dynamic map stacks)
    # Write the code that needs to be executed every time step
    def dynamic(self):
        Precipitation = self.readmap("./Data/pr")
   
#Define the clone map(mask) All raster maps need to have the same properties as the clone map (i.e. same number of rows and collumns, coordinate system, extent, pixels size). PCRaster checks this when the code is run.
myModel = RunoffModel("./Data/mask.map")

# The model runs 10 time steps starting at time step 1.
dynModelFw = DynamicFramework(myModel, lastTimeStep=10, firstTimestep=1)
dynModelFw.run()

# Visualise the land-use map and map with the interception threshold
aguila("./Data/landuse.map","./Data/d.map")