# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 11:02:44 2024

@author: Nooria
"""
from osgeo import gdal
import pycrs
gdal.UseExceptions()

#converted the GeoTIFF files to PCRaster format,check their properties

def RasterLayerProperties(RasterLayer):
    print('Raster file: {}'.format(RasterLayer.GetDescription()))
    print('Driver: {}/{}'.format(RasterLayer.GetDriver().ShortName, RasterLayer.GetDriver().LongName))
    print('Size is {}x{}x{}'.format(RasterLayer.RasterXSize,RasterLayer.RasterYSize,RasterLayer.RasterCount))
    RasterLayerProjection = RasterLayer.GetProjection()
    crs = pycrs.parse.from_ogc_wkt(RasterLayerProjection)
    print('Projection:',crs.name)
    print('Map units:',crs.unit.unitname.ogc_wkt)
    geotransform = RasterLayer.GetGeoTransform()
    if geotransform:
        print('Origin = {}, {})'.format(geotransform[0], geotransform[3]))
        print('Pixel Size=({} {},{},{})'.format(geotransform[1],crs.unit.unitname.ogc_wkt,\
                                                geotransform[5],crs.unit.unitname.ogc_wkt))
    RasterLayerBand = RasterLayer.GetRasterBand(1)
    print('Minimum: {}'.format(RasterLayerBand.GetMinimum()))
    print('Maximum: {}'.format(RasterLayerBand.GetMaximum()))

    print()
    RasterLayer = None
    
    
DTMLayer = gdal.Open(r'C:\Temp\PCRasterTutorials-main\MapAlgebra\data\dtm.map')
RasterLayerProperties(DTMLayer)

BuildingLayer = gdal.Open(r'C:\Temp\PCRasterTutorials-main\MapAlgebra\data\buildg.map')
RasterLayerProperties(BuildingLayer)

RoadLayer = gdal.Open(r'C:\Temp\PCRasterTutorials-main\MapAlgebra\data\roads.map')
RasterLayerProperties(RoadLayer)

GWLevelLayer = gdal.Open(r'C:\Temp\PCRasterTutorials-main\MapAlgebra\data\gwlevel.map')
RasterLayerProperties(GWLevelLayer)