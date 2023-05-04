###############
# Challenge 10
###############

### Prompt:
# Our coding challenge this week that improves our practice with rasters from Week 10.

# Task 1 - Use what you have learned to process the Landsat files provided, this time, you know you are interested in
# the NDVI index which will use Bands 4 (red, aka vis) and 5 (near-infrared, aka nir) from the Landsat 8 imagery, see
# here for more info about the bands: https://www.usgs.gov/faqs/what-are-band-designations-landsat-satellites.
# Data provided are monthly (a couple are missing due to cloud coverage) during the year 2015 for the State of RI, and
# stored in the file Landsat_data_lfs.zip.

# Before you start, here is a suggested workflow:
# 1. Extract the Landsat_data_lfs.zip file into a known location.
# 2. For each month provided, you want to calculate the NVDI, using the equation: ndvi = (nir - vis) / (nir + vis)
#    https://en.wikipedia.org/wiki/Normalized_difference_vegetation_index.
#    Consider using the Raster Calculator Tool in ArcMap and using "Copy as Python Snippet" for the first calculation.
#    The only rule is, you should run your script once, and generate the NDVI for ALL MONTHS provided.
#    As part of your code submission, you should also provide a visualization document (e.g. ArcMap layout in PDF format),
#    showing the patterns for an area of RI that you find interesting.

# Preliminary step: please change working directory on line 30 before running the code.

# Import system modules
import arcpy
import os

# Set analysis environment
arcpy.env.workspace = ws = r"C:\NRS528\Class_10\challenge10\Landsat_data_lfs"
arcpy.env.overwriteOutput = True

# Check out necessary licenses
arcpy.CheckOutExtension("Spatial")
arcpy.CheckOutExtension("ImageAnalyst")

# List the raster folder for each month in the directory
raster_folders = arcpy.ListWorkspaces()
print(raster_folders)

# For each folder in the directory, extract B4 tif files
for folder in raster_folders:
    arcpy.env.workspace = folder
    raster_name = path = os.path.basename(os.path.normpath(folder)) + ".tif"
    print(raster_name)

    raster_list_b4 = arcpy.ListRasters("*B4*", "TIF")
    raster_list_b5 = arcpy.ListRasters("*B5*", "TIF")

    print(raster_list_b4)
    print(raster_list_b5)

    # Set up raster calculator to calculate NDVI
    # Since B5 represents NIR and B4 represents VIS, we will replace
    # NDVI = (NIR - VIS)/(NIR + VIS) with the appropriate bands

    ndvi_02 = (arcpy.Raster(raster_list_b5[0]) - arcpy.Raster(raster_list_b4[0]))/arcpy.Raster((raster_list_b5[0]) + arcpy.Raster(raster_list_b4[0]))
    arcpy.env.workspace = ws
    ndvi_02.save(raster_name)

    print("NDVI calculation complete.")


### Analysis of visualization document attached
# I selected the area around the University of Rhode Island. Based on the NDVI calculated, we can see that
# there are significant differences in vegetation in the Kingston area of Rhode Island between July and November.
# The NDVI score in July is higher than that of November due to higher vegetation growth in the warmer months.
# Hence, the color of the July map also appears whiter.










