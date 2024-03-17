#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Noori
#
# Created:     17-03-2024
# Copyright:   (c) Noori 2024
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import arcpy
arcpy.env.overwriteOutput = True
try:
    # get the parameter for buffer tool
     inPath = arcpy.GetParameterAsText(0)
     outPath = arcpy.GetParameterAsText(1)
     bufferDistance = arcpy.GetParameterAsText(2)

     #Run the Buffer tool
     arcpy.Buffer_analysis(inPath, outPath, bufferDistance)

     # Report a sucess message
     arcpy.AddMessage("All done!")
except:
     # Report an error message
     arcpy.AddError("could not complete the buffer")

     # Report any error message that the buffer tool might have generated
     arcpy.AddMessage(arcpy.GetMessage())