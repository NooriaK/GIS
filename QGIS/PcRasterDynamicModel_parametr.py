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
        self.InterceptionThreshold = lookupscalar("./Data/d.tbl",landuse)       # Lookup table(Interception threshold data for different land-use types.
        self.report(self.InterceptionThreshold,"./Data/d")                      # Write the result to disk using self.report
        
        self.SuMax = lookupscalar("./Data/smax.tbl", soil)                      # maximum storage unsaturated zone mm
        self.report(self.SuMax, "./Data/SuMax")
          
        self.SeparationCoefficient = lookupscalar("./Data/cr.tbl", landuse)     # separation coefficient(-)
        self.report(self.SeparationCoefficient,"./Data/cr")

        self.QuickFlowCoefficient = lookupscalar("./Data/qc.tbl", soil)         # Quick flow coefficient(-)       
        self.report(self.QuickFlowCoefficient,"./Data/Qc")
    
        self.MaxCapRise = lookupscalar("./Data/cp.tbl", landuse)                # potential capillary rise (mm)
        self.report(self.MaxCapRise,"./Data/cMax")
        
        # Calculate maximum to the storage of the saturated zone
        SsDEM = DEM + self.Ss0
        self.SsMax = 25 * ln(SsDEM)
        self.report(self.SsMax,"./Data/ssmax")
        
        # Minimum Capillary rise
        self.MinCapRise = self.SsMax / 4.0
        
        # initialise time series ouput
        
        self.Measurements = self.readmap("./Data/measurements")     # read map with measurement locations
        DischargeAtMeasurementLocation = "./Data/discharge.tss"       # define the output timeseries filename
        self.DischargeTSS = TimeoutputTimeseries(DischargeAtMeasurementLocation,
                                                 self, self.Measurements,noHeader=False)
        
       
     
          
    # Make a global variable, by adding self (PCRaster dynamic map stacks)
    # Write the code that needs to be executed every time step
    def dynamic(self):
        Precipitation = self.readmap("./Data/pr")
        Interception = min(Precipitation, self.InterceptionThreshold)
        self.report(Interception,"./Data/int")
   
        # calculate Net Precipitation
        NetPrecipitation = Precipitation - Interception
        self.report(NetPrecipitation,"./Data/pn")
                
        # Create map with actual evaporation
        ETStations = timeinputscalar("./Data/et.tss", self.metstat)
        self.report(ETStations,"./Data/etstat")
        
        # interpolate ETa with IDW
        ET = inversedistance(self.mask,ETStations, 2, 0, 0)
        self.report(ET,"./Data/et")
        
        # Interpolate ETa with Thiessent
        #ThET = defined(ET)
        #ThETID = nominal(uniqueid(ThET))
        #ThiessendID = spreadzone(ThETID, 0, 1)
        #self.report(ThiessendID,"./Data/thi")
        
        # Modeling of the unsaturated zone
        self.Su = self.Su + (1-self.SeparationCoefficient) * NetPrecipitation
        SuExcess = max(0,((self.Su - self.SuMax)/self.Ku))
        self.Su = self.Su - SuExcess
        self.Su = self.Su - ET
        self.report(self.Su,"./Data/su")
        
        # Modeling of the saturated zone
        self.Ss = self.Ss + (self.SeparationCoefficient * NetPrecipitation) + SuExcess
        self.report(self.Ss,"./Data/ss")
        
        # With [1,10,1] indicate first time step, last time step and interval respectively.
        # in commandl line, aguila --timesteps [1,10,1] ss
        
        # Calculate the saturated overland flow
        SaturatedOverlandFlow = ifthenelse(self.Ss > self.SsMax, self.Ss - self.SsMax,0)
        self.Ss = self.Ss - SaturatedOverlandFlow
        self.report(SaturatedOverlandFlow,"./Data/saof")
        
        # Calculate the quick flow
        SsQuick = self.SsMax * self.QuickFlowCoefficient
        QuickFlow = max((self.Ss - SsQuick), 0) / self.rtq
        self.Ss = self.Ss - QuickFlow
        self.report(QuickFlow, "./Data/qflo")
        
        # calculate the slow flow
        SlowFlow = max(self.Ss, 0) / self.rts
        self.Ss = self.Ss - SlowFlow
        self.report(SlowFlow,"./Data/sflo")
        
        # Capillary rise
        CapRise = ifthenelse(self.Ss > self.MinCapRise, min(self.MinCapRise,ET,self.Ss), self.MinCapRise)
        self.Ss = self.Ss - CapRise
        self.Su = self.Su + CapRise
        self.report(self.Su,"./Data/su")
        self.report(self.Ss,"./Data/ss")
        
        # calculate the runoff and discharge
        Runoff = SaturatedOverlandFlow + QuickFlow + SlowFlow
        Discharge = accuflux(self.flowdirection,Runoff) * self.ConvConst
        self.report(Discharge,"./Data/q")
        self.report(Runoff,"./Data/runoff")
        
        # Report discharge time series at meansurement locations
        self.DischargeTSS.sample(Discharge)
        # aguila discharge.tss
     
   
    
#Define the clone map(mask) All raster maps need to have the same properties as the clone map (i.e. same number of rows and collumns, coordinate system, extent, pixels size). PCRaster checks this when the code is run.
myModel = RunoffModel("./Data/mask.map")

# The model runs 10 time steps starting at time step 1.
dynModelFw = DynamicFramework(myModel, lastTimeStep=10, firstTimestep=1)
dynModelFw.run()

# Visualise the land-use map and map with the interception threshold
#aguila("./Data/landuse.map","./Data/d.map")
