###############
# Challenge 8
###############

# Our coding challenge this week follows from the last exercise that we did in class during Week 8 where we worked with
# functions. Convert some of your earlier code into a function. The only rules are:
    # 1) You must do more than one thing to your input to the function
    # 2) the function must take two arguments or more.
    # 3) provide a zip file of example data within your repo.
# Plan the task to take an hour or two, so use one of the simpler examples from our past classes.

# The example I used for this exercise is a part of Class 7 Step 2. The goal of this step is to create a temporary
# folder and an output folder, and store the generated CSV files in the temporary folder.

# Preliminary step: please change the working directory on line 16 before running the code.

import os
import csv

input_directory = r"C:\NRS528\Class_08\challenge8"

keep_temp_files = True

# DO NOT DO ANYTHING TO THE BELOW
if not os.path.exists(os.path.join(input_directory, "temporary_files")):
    os.mkdir(os.path.join(input_directory, "temporary_files"))
if not os.path.exists(os.path.join(input_directory, "outputs")):
    os.mkdir(os.path.join(input_directory, "outputs"))

# Let's determine our species and split files
def define_species(data_file):

    species_list = []
    with open(os.path.join(input_directory, data_file)) as species_csv:
        header_line = next(species_csv)
        for row in csv.reader(species_csv):
            try: # Using try/except saves us if there is a line with no data in the file
                if row[0] not in species_list:
                    species_list.append(row[0])
            except:
                pass
    print("..There are: " + str(len(species_list)) + " species to process..")

    if len(species_list) > 1:
        for s in species_list:
            s_count = 1
            with open(os.path.join(input_directory, data_file)) as species_csv:
                for row in csv.reader(species_csv):
                    if row[0] == s:
                        if s_count == 1:
                            file = open(os.path.join(input_directory, "temporary_files", s + ".csv"), "w")
                            file.write(header_line)
                            s_count = 0
                        # make well formatted line
                        file.write(",".join(row))
                        file.write("\n")
            file.close()

data_file = "species.csv"
define_species(data_file)



