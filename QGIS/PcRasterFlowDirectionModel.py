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
        
      #  Read Static map from disk (Static map with the .map file extension)  
    def initial(self):
        landuse = self.readmap("./Data/landuse")
        soil = self.readmap("./Data/soil")
        self.metstat = self.readmap("./Data/metstat")
        DEM = self.readmap("./Data/dem")
        self.mask = self.readmap("./Data/mask")
        self.flowdirection = self.readmap("./Data/ldd")
        
        # Add the constants as global variables
        self.Ku = scalar(1.5)                   # Recession contstant of flow from unsaturated to saturated zone
        self.surface = scalar(0.01)             # surface of a gridcell (km2)
        self.ConvConst = scalar(0.00001157407)  # From mm/10 days to m3/s: *1/1000 * 1/10 *
                                                # # 1/24 * 1/3600 * 100^2
                                                
        self.rtq = scalar(1.2)                  # Recession contstant quick flow
        self.rts = scalar(5.3)                  # Recession contstant slow flow
        self.Su = scalar(50.0)                  # storage unsaturated zone
        self.Ssmx = scalar(0.0)                 # parameter controlling the groundwater flow to the river
        self.Ss = scalar(50.0)                  # storage saturated zone 
        self.Ss0 = scalar(100.0)                # Distance between the surface and the bottom of the river
        
            
         # lookup tables
        self.InterceptionThreshold = lookupscalar("./Data/intThrshhold.tbl",landuse)       # Lookup table(Interception threshold data for different land-use types.
        self.report(self.InterceptionThreshold,"./Data/intThrshhold")                      # Write the result to disk using self.report
        
        self.SuMax = lookupscalar("./Data/smax.tbl", soil)                      # maximum storage unsaturated zone mm
        self.report(self.SuMax, "./Data/SuMax")
          
        self.SeparationCoefficient = lookupscalar("./Data/cr.tbl", landuse)     # separation coefficient(-)
        self.report(self.SeparationCoefficient,"./Data/cr")

        self.QuickFlowCoefficient = lookupscalar("./Data/qc.tbl", soil)         # Quick flow coefficient(-)       
        self.report(self.QuickFlowCoefficient,"./Data/Qc")
    
        self.MaxCapRise = lookupscalar("./Data/cp.tbl", landuse)                # potential capillary rise (mm)
        self.report(self.MaxCapRise,"./Data/cMax")
        
         
        # Calculation of the flow direction map
        self.flowdirection = lddcreate(DEM,1e31,1e31,1e31,1e31)
        self.flowdirection = lddmask(self.flowdirection,self.mask)
        self.report(self.flowdirection,"./Data/ldd")
                   
               
                
    # Make a global variable, by adding self (PCRaster dynamic map stacks)
    # Write the code that needs to be executed every time step
    def dynamic(self):
        Precipitation = self.readmap("./Data/pr")
        Interception = min(Precipitation, self.InterceptionThreshold)
        self.report(Interception,"./Data/int")
        
        
#Define the clone map(mask) All raster maps need to have the same properties as the clone map (i.e. same number of rows and collumns, coordinate system, extent, pixels size). PCRaster checks this when the code is run.
myModel = RunoffModel("./Data/mask.map")

# The model runs 10 time steps starting at time step 1.
dynModelFw = DynamicFramework(myModel, lastTimeStep=10, firstTimestep=1)
dynModelFw.run()

# Visualise the land-use map and map with the interception threshold
aguila("./Data/landuse.map","./Data/intThrshhold.map","./Data/ldd.map")
