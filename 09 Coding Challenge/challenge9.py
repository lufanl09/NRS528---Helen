###############
# Challenge 9
###############

# Prompt:
# In this coding challenge, your objective is to utilize the arcpy.da module to undertake some basic partitioning of
# your dataset. I want you to work with the Forest Health Works dataset from RI GIS

# Using the arcpy.da module, I want you to extract all sites that have a photo of the invasive species into
# a new Shapefile, and do some basic counts of the dataset.

# In summary, please addressing the following:
# 1. Count how many individual records have photos, and how many do not (2 numbers), print the results.
# 2. Count how many unique species there are in the dataset, print the result.
# 3. Generate two shapefiles, one with photos and the other without.

# Preliminary step: please change your arcpy workspace on line 22 before running the code.

# Importing tool
import arcpy
arcpy.env.overwriteOutput = True

# Setting workspace
arcpy.env.workspace = r"C:\NRS528\Class_09\challenge9"
input_shp = r"RI_Forest_Health_Works_Project%3A_Points_All_Invasives.shp"

# Creating file names for shapefile with photo and shapefile without photo
new_shpfile_photo = arcpy.CreateFeatureclass_management(arcpy.env.workspace, "new_shapefile_photo.shp", "POINT", input_shp,
                                    "DISABLED", "DISABLED", spatial_reference=4326)

new_shpfile_nophoto = arcpy.CreateFeatureclass_management(arcpy.env.workspace, "new_shapefile_nophoto.shp", "POINT", input_shp,
                                    "DISABLED", "DISABLED", spatial_reference=4326)


### Step 1. Count how many individual records have photos, and how many do not (2 numbers), print the results.
# Records with photos in the shapefile
count = 0
with arcpy.da.SearchCursor(input_shp, ['photo']) as cursor:
    for row in cursor:
        if row[0] == 'y':
            count += 1
print("There are " + str(count) + " records with photos.")

# Records without photos in the shapefile
count = 0
with arcpy.da.SearchCursor(input_shp, ['photo']) as cursor:
    for row in cursor:
        if row[0] != 'y':
            count += 1
print("There are " + str(count) + " records without photos.")


### Step 2. Count how many unique species there are in the dataset, print the result.
# Create a list to store the species
species_list = []

line_count = 0
with arcpy.da.SearchCursor(input_shp, ['Species']) as cursor:
    for row in cursor:
        if row[0] not in species_list:
            species_list.append(row[0])

print("There are " + str(len(species_list)) + " unique species in the dataset.")


### Step 3. Generate two shapefiles, one with photos and the other without.
# list fields tool
field_list = [f.name for f in arcpy.ListFields(input_shp)]  # generates all fields

# Generate a shapefile of fields with photos
expression = arcpy.AddFieldDelimiters(input_shp, "photo") + " = 'y'"
with arcpy.da.SearchCursor(input_shp, field_list, expression) as sCursor:
    with arcpy.da.InsertCursor(new_shpfile_photo, field_list) as iCursor:
        for row in sCursor:
            iCursor.insertRow(row)
print("New shapefile with photos is created.")

# Generate a shapefile of fields without photos
expression = arcpy.AddFieldDelimiters(input_shp, "photo") + " <> 'y'"
with arcpy.da.SearchCursor(input_shp, field_list, expression) as sCursor:
    with arcpy.da.InsertCursor(new_shpfile_nophoto, field_list) as iCursor:
        for row in sCursor:
            iCursor.insertRow(row)
print("New shapefile with no photos is created.")

print("End of assignment")

