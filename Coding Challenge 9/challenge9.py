###############
# Challenge 9 #
###############

import arcpy
arcpy.env.overwriteOutput = True

arcpy.env.workspace = r"C:\NRS528\Class_09\challenge9"
input_shp = r"C:\NRS528\Class_09\challenge9\RI_Forest_Health_Works_Project%3A_Points_All_Invasives.shp"

new_shpfile_photo = arcpy.CreateFeatureclass_management(arcpy.env.workspace, "new_shapefile_photo.shp", "POINT", input_shp,
                                    "DISABLED", "DISABLED", spatial_reference=4326)

new_shpfile_nophoto = arcpy.CreateFeatureclass_management(arcpy.env.workspace, "new_shapefile_nophoto.shp", "POINT", input_shp,
                                    "DISABLED", "DISABLED", spatial_reference=4326)


### Count how many individual records have photos, and how many do not (2 numbers), print the results.
# with photos
count = 0
with arcpy.da.SearchCursor(input_shp, ['photo']) as cursor:
    for row in cursor:
        if row[0] == 'y':
            count += 1
print("There are " + str(count) + " records with photos.")

# without photos
count = 0
with arcpy.da.SearchCursor(input_shp, ['photo']) as cursor:
    for row in cursor:
        if row[0] != 'y':
            count += 1
print("There are " + str(count) + " records without photos.")


### Count how many unique species there are in the dataset, print the result.
species_list = []

line_count = 0
with arcpy.da.SearchCursor(input_shp, ['Species']) as cursor:
    for row in cursor:
        if row[0] not in species_list:
            species_list.append(row[0])

print("There are " + str(len(species_list)) + " unique species in the dataset.")


### Generate two shapefiles, one with photos and the other without.
# list fields tool
field_list = [f.name for f in arcpy.ListFields(input_shp)]  # generates all fields

# with photo
expression = arcpy.AddFieldDelimiters(input_shp, "photo") + " = 'y'"
with arcpy.da.SearchCursor(input_shp, field_list, expression) as sCursor:
    with arcpy.da.InsertCursor(new_shpfile_photo, field_list) as iCursor:
        for row in sCursor:
            iCursor.insertRow(row)
print("New shapefile with photos is created.")

# without photo:
expression = arcpy.AddFieldDelimiters(input_shp, "photo") + " <> 'y'"
with arcpy.da.SearchCursor(input_shp, field_list, expression) as sCursor:
    with arcpy.da.InsertCursor(new_shpfile_nophoto, field_list) as iCursor:
        for row in sCursor:
            iCursor.insertRow(row)
print("New shapefile with no photos is created.")



