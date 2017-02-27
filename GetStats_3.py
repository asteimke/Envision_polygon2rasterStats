# this script reads in rasters of hydrologic variables and calculates the mean and standard deviation of their values
# ALS, 11/8/2016

import arcpy
import os
from arcpy import env
from arcpy.sa import *

# check out the ArcGIS Spatial Analyst extension license 
arcpy.CheckOutExtension("Spatial")


# variables (models/scenarios and hydro variables)
dataType = "ET_"     # change this for other types of variables (i.e. ET, Q, P)
landcover = ["FS05", "FSb1", "FSa2", "NLCD"]  # options: FSb1, FSa2, FS05, NLCD
modelList = ["Historical", "RCP45_CanESM2", "RCP45_CNRM_CM5", "RCP45_GFDL_ESM2M", "RCP85_CanESM2", "RCP85_CNRM_CM5", "RCP85_GFDL_ESM2M"]


# initialize lists
fileList = []
QmeanList = []
QstdList = []


for land in landcover:
    # set workspace name/location
    workspaceName = str("L:\\project-files\\Amy\\Envision\\FutureClimate_ForeSce_shrubGrassSeparated\\ET\\"+land+".gdb") # path to location of averaged rasters
    arcpy.env.workspace = workspaceName
    arcpy.env.overwriteOutput = True
    for model in modelList:
        if model == "Historical":
            startYr = [1980]
        else:
            startYr = [2010, 2040, 2070]
        for year in startYr:              
            yearStr = str(year)
            fileName = str("ET_"+land+"_"+model+"_"+yearStr)
            Qmean = arcpy.GetRasterProperties_management(fileName, 'MEAN', '#')
            Qstd = arcpy.GetRasterProperties_management(fileName, 'STD', '#')           
            fileList.append(fileName)
            QmeanList.append(Qmean)
            QstdList.append(Qstd)
            mean = str(Qmean)
            std = str(Qstd)
            print fileName+","+mean+","+std

