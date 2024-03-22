
>>> # finds all cells over 3500 meters in an elevation raster and makes a new raster that codes all those cells as 1. Remaining values in the new raster are coded as 0
import arcpy
from arcpy.sa import *
inRaster = r"C:\Temp\GEOG\foxlake"
cutoffElevation = 3500
# check out Spatial Analyst extesion
arcpy.CheckExtension("Spatial")
# Make a map algebra expression and save the result raster
outRaster = Raster(inRaster) > cutoffElevation
outRaster.save(r"C:\Temp\GEOG\foxlake_hi_10")
arcpy.CheckExtension("Spatial")
