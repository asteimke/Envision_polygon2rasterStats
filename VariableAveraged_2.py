# this script reads in rasters in a geodatabase and creates a new raster that is the averaged values of rasters for specified year intervals
# ALS, 11/18/2016


import arcpy
import os
from arcpy import env
from arcpy.sa import *

# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

# set variables
hydro_variable = "ET"                          # variable of interest (runoff, ET, etc.)
landcover = ["FS05", "FSa2", "FSb1", "NLCD"]   # land cover scenarios
startYr = [2010, 2040, 2070]                   # start year for averages
modelList = ["RCP45_CanESM2", "RCP45_CNRM_CM5", "RCP45_GFDL_ESM2M", "RCP85_CanESM2", "RCP85_CNRM_CM5", "RCP85_GFDL_ESM2M"]  # future scenarios
numYears = 30                                  # number of years to average for
model_hist = "Historical"                      # name for historical scenario
histyears = range(1980,1980+30)                # range for historical run


# set workspace name
for land in landcover:
    workspaceName = str("L:\\project-files\\Amy\\Envision\\FutureClimate_ForeSce_shrubGrassSeparated\\"+hydro_variable+"\\"+land+".gdb") # set workspace location
    arcpy.env.workspace = workspaceName
    arcpy.env.overwriteOutput = True

    # build file list for historical values
    fileList = []
    for year in histyears:
        yearStr = str(year)
        fileName = str(land+yearStr+"_Historical")
        fileList.append(fileName)

    # create new raster with mean of values for historical values  
    outras = CellStatistics(fileList,"MEAN","DATA")
    outName = str(hydro_variable+"_"+land+"_"+model_hist+"_1980")
    outras.save(outName)
    print str("saving " + outName)

    # average for future scenarios
    for model in modelList:
        for Yr in startYr:  
            years = range(Yr,Yr+numYears)
            outRasYr = str(Yr)

            # build file list
            fileList = []
            for year in years:
                yearStr = str(year)
                fileName = str(land+yearStr+"_"+model)
                fileList.append(fileName)

            # create new raster with mean of values 
            outras = CellStatistics(fileList,"MEAN","DATA")  
            outName = str(hydro_variable+"_"+land+"_"+model+"_"+outRasYr)
            outras.save(outName)
            print str("saving " + outName)
            
