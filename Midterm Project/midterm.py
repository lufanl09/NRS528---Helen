###############
# Helen Liu - 528 Midterm

# For this midterm, I want to find the average number of days with good air quality for each state. I started by
# creating a list of all the states in the csv file. Then, I used that list to split the csv file by state into separate
# files. Next, I created calculated the average for each state and created a new file with the result.
# The 2022 air quality data is downloaded from the EPA.

# The air quality data is collected by different monitors installed at various sites in the US. I want to map out
# where the sites are located in Providence, Rhode Island, so I downloaded the coordinates from EPA as well.
# To map the sites, I created a point feature layer using the XY Event Layer tool. Then, I selected Providence from
# the Towns layer and clipped the Sites layer to it so only the AQS sites located in Providence are selected. Finally,
# I created a buffer zone around each site of 1 kilometer.

# Preliminary step: please change the working directories on line 24 and 27 before running the code. Please also unzip
# "Towns" folder for the towns shapefile. 
###############

### Import modules
import os
import csv
import glob
import arcpy

arcpy.env.workspace = r"C:\NRS528\midterm"

### Set directory - THIS NEEDS TO BE CHANGED
input_directory = r"C:\NRS528\midterm"
annual_aqi = "annual_aqi_by_county_2022.csv"

keep_temp_files = True

# Creating folders to store temporary files
if not os.path.exists(os.path.join(input_directory, "state_csv_files")):
    os.mkdir(os.path.join(input_directory, "state_csv_files"))

### Create a list of states from the csv file
state_list = []

with open(os.path.join(input_directory, annual_aqi)) as aqi:
    header = next(aqi)
    print("Header for " + annual_aqi + ": " + header)

    for row in csv.reader(aqi, delimiter=","):
        state = row[0]
        if state not in state_list:
            state_list.append(state)
    print("There are " + str(len(state_list)) + " states in the file.")

### Split the file by states
for state in state_list:
    state_count = 1
    with open(os.path.join(input_directory, annual_aqi)) as aqi:
        for row in csv.reader(aqi):
            if row[0] == state:
                if state_count == 1:
                    file = open(os.path.join(input_directory, "state_csv_files", state + "2022.csv"), "w")
                    file.write(header)
                    state_count = 0
                file.write(",".join(row))
                file.write("\n")
    file.close()

### After files are created, we can find the average number of good days by state
# Change directory to the folder where all state files are stored
os.chdir(os.path.join(input_directory, "state_csv_files"))
state_file_list = glob.glob("*.csv")      # Find all CSV files in the directory
print("There are " + str(len(state_file_list)) + " CSV files.")

state_directory = input_directory + r"\state_csv_files"
avg_directory = input_directory + r"\average"

# Another way to make a new directory that stores the final file created
os.mkdir(avg_directory)

avg_file = open(os.path.join(avg_directory, "avg_good_days.csv"), "w")
avg_file.write("State, Average Good Days")
avg_file.write("\n")

for state_file in state_file_list:
    print("Processing: " + str(state_file))

    with open(os.path.join(state_directory, state_file)) as state_csv:
        sum_good_days = 0
        county = 0
        for row in csv.reader(state_csv):
            if county > 0:
                good_days = row[4]
                sum_good_days += int(good_days)
            county += 1
    avg_good_days = sum_good_days/(county-1)
    print(avg_good_days)

    avg_file.write(row[0] + "," + str(avg_good_days))
    avg_file.write("\n")

    print("We wrote that " + str(row[0]) + " " + str(avg_good_days))

avg_file.close()


### Next, I want to map out the AQS sites to see where they are located in Rhode Island
# First, create a point feature layer based on the x- and y-coordinates defined in the AQS sites table
in_Table = r"aqs_sites_RI.csv"
x_coords = "Longitude"
y_coords = "Latitude"
z_coords = ""
out_Layer = "RI_sites"
saved_Layer = r"RI_AQS_Sites.shp"

# Set the spatial reference
spRef = arcpy.SpatialReference(4326)  # 4326 == WGS 1984

lyr = arcpy.MakeXYEventLayer_management(in_Table, x_coords, y_coords, out_Layer, spRef, z_coords)  # order matters

# Save to a layer file
arcpy.CopyFeatures_management(lyr, saved_Layer) # save in-memory file onto computer

if arcpy.Exists(saved_Layer):
    print("Created file successfully!")


### I only want to select the power plants located in Providence, so I will select "Providence" in the
### towns layer and clip the power plants to the town.

# Select Providence
print("Selecting town...")
arcpy.analysis.Select(in_features = r"towns.shp",
                      out_feature_class = r"Providence.shp",
                      where_clause = "NAME = 'PROVIDENCE'")

print("Providence selected.")


# Clip power stations layer to Providence layer
print("Clipping layer...")
arcpy.analysis.Clip(in_features = r"RI_AQS_Sites.shp",
                    clip_features = r"Providence.shp",
                    out_feature_class = r"Providence_Sites.shp",
                    cluster_tolerance = "#")

print("Layer clipped.")


# Finally, I created a buffer zone of 1km around the sites to see the areas that ar
print("Buffering...")
arcpy.Buffer_analysis(in_features = r"Providence_Sites.shp",
                      out_feature_class = r"Sites_Buffer.shp",
                      buffer_distance_or_field = "1 Kilometers",
                      line_side = "FULL",
                      line_end_type = "ROUND",
                      dissolve_option = "NONE",
                      dissolve_field = "#",
                      method = "PLANAR")

print("Layer buffered.")




