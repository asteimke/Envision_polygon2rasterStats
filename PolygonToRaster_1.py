# this script reads in shapefiles in a geodatabase and converts them to raster
# ALS, 11/8/2016


import arcpy
import os
from arcpy import env
from arcpy.sa import *

# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

valField = "ET_yr"		    # hydro variable of interest (i.e. Q, P, ET)
cellSize =  100                     # output raster cell size (in meters)
landcover = ["FS05", "FSa2", "FSb1", "NLCD"] 
modelList = ["Historical", "RCP45_CanESM2", "RCP45_CNRM-CM5", "RCP45_GFDL-ESM2M", "RCP85_CanESM2", "RCP85_CNRM-CM5", "RCP85_GFDL-ESM2M"] # these are changed from CNRM-CM5 to CNRM_CM5, FYI

# set geoprocessing environments (change workspace as needed)
for land in landcover:
    for model in modelList:
	
	# path to geodatabase locations 
        if model == "Historical":           
            workSpace = str("L:\\project-files\\Amy\\Envision\\FutureClimate_ForeSce_shrubGrassSeparated\\"+land+"\\Outputs\\"+model+"-NoFire\\Run0")
        else:
            workSpace = str("L:\\project-files\\Amy\\Envision\\FutureClimate_ForeSce_shrubGrassSeparated\\"+land+"\\Outputs\\"+model+"+noFire\\Run0")
        arcpy.env.workspace = workSpace
        arcpy.env.overwriteOutput = True
        
	# path to output locations
	outputWorkSpace = str("L:\\project-files\\Amy\\Envision\\FutureClimate_ForeSce_shrubGrassSeparated\\ET\\"+land+".gdb\\")
        outputFolder = outputWorkSpace
        
	# get shapefiles
	shpList = arcpy.ListFeatureClasses()      
        
        for shp in shpList:  
            # shorten filenames
	    filename2 = shp[:13]
            filename = filename2[8:]
			
	    # rename because of GIS issues with dashes (easier than changing individual files)
            if model == "RCP45_CNRM-CM5":
                model = "RCP45_CNRM_CM5"
            elif model == "RCP45_GFDL-ESM2M":
                model = "RCP45_GFDL_ESM2M"
            elif model == "RCP85_CNRM-CM5":
                model = "RCP85_CNRM_CM5"
            elif model == "RCP85_GFDL-ESM2M":
                model = "RCP85_GFDL_ESM2M"
            else:
                model = model
				
            print str("processing " + filename + model + land)
            
	    outRaster = str(outputWorkSpace+land+filename+model)  # out raster name
            arcpy.PolygonToRaster_conversion(shp, valField, outRaster, "CELL_CENTER", "NONE", cellSize)  # convert polygon to raster
			
