# -*- coding: utf-8 -*-
import os
from osgeo import gdal, gdalconst
os.environ['PROJ_LIB'] = r'C:\Users\Nkuhan\anaconda3\Library\share\proj'
os.environ['GDAL_DATA'] = r'C:\Users\Nkuhan\anaconda3\Library\share'

# convert all files at once 
# \ next line


def ConvertToPCRaster(src_filename,dst_filename,ot,VS):
    #open existing dataset
    src_ds=gdal.Open(src_filename) #source filename
    #GDAL Translate
    dst_ds = gdal.Translate(dst_filename, src_ds, format='PCRaster', \
                        outputType=ot, metadataOptions = VS)
# properly close the datasets to flush the disk
    dst_ds = None
    src_ds = None

#ConvertToPCRaster("data/buidg.tif", "data/buildg.map",gdalconst.GDT_Int32,"VS_NOMINAL")
ConvertToPCRaster("data/roads.tif", "data/roads.map",gdalconst.GDT_Int32, "VS_NOMINAL")
ConvertToPCRaster("data/gwlevel.tif","data/gwlevel.map",gdalconst.GDT_Float32, "VS_SCALAR")
ConvertToPCRaster("data/dtm.tif", "data/dtm.map",gdalconst.GDT_Float32,"VS_SCALAR")
