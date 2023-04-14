###############
# Challenge 7
###############

import csv
import os
import arcpy

input_directory = r"C:\NRS528\Class_07\challenge7"
csv_file = r"species.csv"

### Step 1. Read csv and extract the 2 species names into a list
species_list = []

with open(os.path.join(input_directory, csv_file)) as species_file:
    header = next(species_file)
    print(header)

    for row in csv.reader(species_file, delimiter=","):
        species = row[0]
        longitude = row[1]
        latitude = row[2]
        if species not in species_list:
            species_list.append(species)

    print(species_list)

### Step 2. Read csv file, ask if row contains 1 of the species and copy the row to a new file
if not os.path.exists(os.path.join(input_directory, "Species_Directory")):
    os.mkdir(os.path.join(input_directory, "Species_Directory"))

header = "Species,Longitude,Latitude\n"

for species in species_list:
    with open(os.path.join(input_directory, csv_file)) as species_file:
        print(os.path.join(input_directory, csv_file))
        species_count = 1
        for row in csv.reader(species_file):
            if row[0] == species:
                if species_count == 1:
                    file = open(os.path.join(r"Species_Directory/" + str(species) + ".csv"), "w")
                    file.write(header)
                    species_count = 0
                file.write(",".join(row))
                file.write("\n")
        print(file)
    file.close()

    new_directory = r"Species_Directory"
    arcpy.env.workspace = new_directory

    # Inputs for XY Event Layer
    in_Table = r"Species_Directory/" + str(species) + ".csv"
    x_coords = "Longitude"
    y_coords = "Latitude"
    z_coords = ""
    out_Layer = str(species)
    saved_Layer = r"Species_Directory/" + str(species) + "_Output.shp"

    # Spatial reference for the coordinates
    spRef = arcpy.SpatialReference(4326)  # 4326 == WGS 1984

    # Using XY Event Layer to create a point feature layer based on XY coordinates
    lyr = arcpy.MakeXYEventLayer_management(in_Table, x_coords, y_coords, out_Layer, spRef, z_coords)

    arcpy.CopyFeatures_management(lyr, saved_Layer)

    if arcpy.Exists(saved_Layer):
        print("Created file successfully " + str(species))

    ### Step 4. Describe shp to get extent
    desc = arcpy.Describe(r"Species_Directory/" + str(species) + "_Output.shp")

    print('Extent:\n XMin: {},\n YMin: {}'.format(desc.extent.XMin, desc.extent.YMin))
    print('Extent:\n XMax: {},\n YMax: {}'.format(desc.extent.XMax, desc.extent.YMax))

    ### Step 5. Generate fishnet
    # Create output name
    outFeatureClass = str(species) + "_Fishnet.shp"

    # Set origin of fishnet
    originCoordinate = str(desc.extent.XMin) + " " + str(desc.extent.YMin)
    yAxisCoordinate = str(desc.extent.XMin) + " " + str(desc.extent.YMin + 10)
    cellSizeWidth = "0.25"
    cellSizeHeight = "0.25"
    numRows = ""
    numColumns = ""
    oppositeCorner = str(desc.extent.XMax) + " " + str(desc.extent.YMax)  # i.e. max x and max y coordinate
    labels = "NO_LABELS"
    templateExtent = "#"
    geometryType = "POLYGON"

    arcpy.CreateFishnet_management(outFeatureClass, originCoordinate, yAxisCoordinate,
                                   cellSizeWidth, cellSizeHeight, numRows, numColumns,
                                   oppositeCorner, labels, templateExtent, geometryType)

    print("End of Step 5")

    ### Step 6. Spatial join
    print("Start of Step 6 " + str(species))

    target_features = str(species) + "_Fishnet.shp"
    print("Fishnet created")
    join_features = str(species) + "_Output.shp"
    print("Output file created")
    out_feature_class = r"Species_Directory/" + str(species) + "_HeatMap.shp"
    print("Heat map created")
    join_operation = "JOIN_ONE_TO_ONE"
    join_type = "KEEP_ALL"
    field_mapping = ""
    match_option = "INTERSECT"
    search_radius = ""
    distance_field_name = ""
    print("All files done")
    print("all files " + str(species))

    arcpy.SpatialJoin_analysis(target_features, join_features, out_feature_class,
                               join_operation, join_type, field_mapping, match_option,
                               search_radius, distance_field_name)

    print("End of Step 6 " + str(species))


    ### Step 7. Clean up (delete intermediary files)
    if arcpy.Exists(out_feature_class):
        print("Deleting intermediate files")
        arcpy.Delete_management(target_features)
        arcpy.Delete_management(join_features)







