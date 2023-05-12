################
# Final Toolbox
# NRS 528
# Helen Liu
################

# Prompt:
# In your final assignment for this course, you should create a Python Toolbox that contains a minimum of three simple
# tools for undertaking geoprocessing and file management operations. These tools can be discrete or part of a larger
# workflow. However, the caveats are that you should create a "single file" toolbox (no includes, or external file
# tools) and you should aim to not exceed 2000 lines of code in its entirety (but if you do, no worries).
# You should document the toolbox using Github README.md and provide example data for running each of your tools.

# Grading and feedback will focus on:
    # 1) Does the toolbox install, and the tools run successfully?
    # 2) Cleanliness of code
    # 3) Functionality and depth of processing operation
    # 4) Appropriate use of documentation
    # 5) Provide example data that allows me to test your tools.

# The criteria are:
    # Does the toolbox install and run? (25 points)
    # Cleanliness of code (25 points)
    # Functionality and depth of processing (25 points)
    # Appropriate use of documentation (15 points)
    # In addition, you must provide example data (10 points).


# This toolbox consists of 3 main tools: Select and Describe, Species Split, and Create Shapefile.

# Select and Describe Tool
# The Select tool is used to select a specific feature in the input, such as selecting a town as the study area.
# In addition to Select, I also would like to obtain different elements of the data by using Describe.
# This returns different properties of the data, such as the data type, fields, indexes, etc.
# Here specifically, I would like to return the coordinate system.
# Steps:
# 1. Set up input shapefile
# 2. Input where clause expression if needed
# 3. Output selected shapefile
# 4. Describe input and output features and add description message

# Species Split Tool
# This tool takes a CSV input and splits the table based on the species and create new CSV files.
# Steps:
# 1. Set up input folder where the CSV file is located
# 2. Set up input CSV file
# 3. Create temporary files folder and output folder
# 4. Split CSV file

# Create Shapefile
# This tool creates shapefiles based on the species CSV files created by the Species Split Tool.
# Steps:
# 1. Set up input file
# 2. Generate shapefile using Make XY Event Layer



import arcpy
import csv
import os


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Python Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [SelectDescribeTool, SpeciesSplit, CreateShp]


# Select and Describe Tool: select a feature in the data as the main study area and describe the data elements
class SelectDescribeTool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Select and Describe Tool"
        self.description = "Select a feature from an input feature class or layer and describe feature elements."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        params = []
        in_feature = arcpy.Parameter(name="in_features",
                                     displayName="Input Features",
                                     datatype="GPFeatureLayer",
                                     parameterType="Required",  # Required|Optional|Derived
                                     direction="Input",  # Input|Output
                                     )
        # in_feature.value = r"C:\NRS528\FinalProject\towns.shp"  # This is a default value that can be over-ridden in the toolbox
        params.append(in_feature)

        expression_input = arcpy.Parameter(name="where_clause",
                                           displayName="Expression",
                                           datatype="GPSQLExpression",
                                           parameterType="Optional",
                                           direction="Input",
                                           )
        expression_input.parameterDependencies = [in_feature.name]
        params.append(expression_input)

        out_feature = arcpy.Parameter(name="out_feature_class",
                                      displayName="Out Feature Class",
                                      datatype="DEFeatureClass",
                                      parameterType="Required",
                                      direction="Output",
                                      )
        # out_feature.value = r"Select_Output.shp"  # This is a default value that can be over-ridden in the toolbox
        params.append(out_feature)

        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        in_feature = parameters[0].valueAsText
        expression_input = parameters[1].valueAsText
        out_feature = parameters[2].valueAsText

        object_input = arcpy.Describe(in_feature)

        arcpy.Select_analysis(in_features=in_feature,
                              out_feature_class=out_feature,
                              where_clause=expression_input,
                              )

        object_output = arcpy.Describe(out_feature)

        # Describe the coordinate system of the input and output features
        arcpy.AddMessage("Input feature had a coordinate system of: " + object_input.SpatialReference.name)
        arcpy.AddMessage("Output feature had a coordinate system of: " + object_output.SpatialReference.name)

        return


# Species Split Tool: split input CSV file based on species names
class SpeciesSplit(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Species Split"
        self.description = "Splits CSV file based on different species."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        params = []
        input_folder = arcpy.Parameter(name="input_folder",
                                       displayName="Input Folder",
                                       datatype="DEWorkspace",
                                       parameterType="Required",  # Required|Optional|Derived
                                       direction="Input",  # Input|Output
                                       )
        # input_folder.value = r"C:\NRS528\FinalProject"
        params.append(input_folder)

        input_file = arcpy.Parameter(name="input_file",
                                     displayName="Input Species CSV file",
                                     datatype="DETable",
                                     parameterType="Required",  # Required|Optional|Derived
                                     direction="Input",  # Input|Output
                                     )
        # input_file.value = r"species.csv"
        params.append(input_file)

        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    # Create new file paths and generate new csv files
    def execute(self, parameters, messages):
        """The source code of the tool."""
        input_directory = parameters[0].valueAsText

        keep_temp_files = True

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
                    try:
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

        data_file = parameters[1].valueAsText
        define_species(data_file)

        return


# Create Shapefile Tool: create a shapefile based on input CSV file(s)
class CreateShp(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Create Shapefile"
        self.description = "Create shapefile based on input CSV file(s)."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        params = []
        input_csv = arcpy.Parameter(name="input_csv",
                                    displayName="Input CSV",
                                    datatype="DETable",
                                    parameterType="Required",  # Required|Optional|Derived
                                    direction="Input",  # Input|Output
                                    )
        # input_csv.value = r"species.csv"
        params.append(input_csv)

        output_shp = arcpy.Parameter(name="output_shp",
                                     displayName="Output Shapefile",
                                     datatype="DEFeatureClass",
                                     parameterType="Required",  # Required|Optional|Derived
                                     direction="Output",  # Input|Output
                                     )
        params.append(output_shp)

        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    # Create shapefile based on coordinates in CSV file
    def execute(self, parameters, messages):
        """The source code of the tool."""
        in_Table = parameters[0].valueAsText
        x_coords = "Longitude"
        y_coords = "Latitude"
        z_coords = ""
        out_Layer = parameters[0].name
        saved_Layer = parameters[1].valueAsText

        # Spatial reference for the coordinates
        spRef = arcpy.SpatialReference(4326)  # 4326 == WGS 1984

        # Using XY Event Layer to create a point feature layer based on XY coordinates
        lyr = arcpy.MakeXYEventLayer_management(in_Table, x_coords, y_coords, out_Layer, spRef, z_coords)

        arcpy.CopyFeatures_management(lyr, saved_Layer)

        return


# # Test tools: SelectDescribeTool, SpeciesSplit, CreateShp
# def main():
#     tool = SelectDescribeTool()
#     tool.execute(tool.getParameterInfo(), None)
#
# if __name__ == '__main__':
#     main()




