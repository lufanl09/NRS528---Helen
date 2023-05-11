################
# Final Toolbox
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


# The goal of this project is to find a suitable area to build a wind farm. The main geoprocessing tools that will be
# used to create the toolbox are: Select, Clip, and Buffer.

# Preliminary step: please change the working directory on line 32 before running the code.

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
        self.tools = [FirstSelectTool, ClipTool, SecondSelectTool, BufferTool, SpeciesSplit]


# The select tool is to select a town in Rhode Island as the main study area
class FirstSelectTool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "First Select Tool"
        self.description = "Select a feature from an input feature class or layer."
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
        # in_feature.value = r"towns.shp"  # This is a default value that can be over-ridden in the toolbox
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
        out_feature.value = r"First_Select_Output.shp"  # This is a default value that can be over-ridden in the toolbox
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

        arcpy.AddMessage("Input feature had a coordinate system of: " + object_input.SpatialReference.name)
        arcpy.AddMessage("Output feature had a coordinate system of: " + object_output.SpatialReference.name)

        return


# The clip tool is to clip the RI land cover shapefile to the study area
class ClipTool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Clip Tool"
        self.description = "Extracts input features that overlay the clip features."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        params = []
        in_feature = arcpy.Parameter(name="input_feature",
                                     displayName="Input Feature",
                                     datatype="GPFeatureLayer",
                                     parameterType="Required",  # Required|Optional|Derived
                                     direction="Input",  # Input|Output
                                     )
        # in_feature.value = r"rilc11d.shp"  # This is a default value that can be over-ridden in the toolbox
        params.append(in_feature)

        clip_feature = arcpy.Parameter(name="clip_feature",
                                       displayName="Clip Feature",
                                       datatype="GPFeatureLayer",
                                       parameterType="Required",  # Required|Optional|Derived
                                       direction="Input",  # Input|Output
                                       )
        clip_feature.value = r"First_Select_Output.shp"  # This is a default value that can be over-ridden in the toolbox
        params.append(clip_feature)

        output_feature = arcpy.Parameter(name="output_feature",
                                         displayName="Output Feature",
                                         datatype="DEFeatureClass",
                                         parameterType="Required",  # Required|Optional|Derived
                                         direction="Output",  # Input|Output
                                         )
        output_feature.value = r"Clip_Output.shp"  # This is a default value that can be over-ridden in the toolbox
        params.append(output_feature)

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
        clip_feature = parameters[1].valueAsText
        output_feature = parameters[2].valueAsText

        arcpy.Clip_analysis(in_features=in_feature,
                            clip_features=clip_feature,
                            out_feature_class=output_feature,
                            cluster_tolerance="")
        return


# The select tool is to select a land cover type to study
class SecondSelectTool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Second Select Tool"
        self.description = "Select a feature from an input feature class or layer."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        params = []
        in_feature = arcpy.Parameter(name="in_features",
                                     displayName="Input Features",
                                     datatype="GPFeatureLayer",
                                     parameterType="Required", # Required|Optional|Derived
                                     direction="Input", # Input|Output
                                     )
        # in_feature.value = r"rilc11d.shp"  # This is a default value that can be over-ridden in the toolbox
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
        out_feature.value = r"Second_Select_Output.shp"  # This is a default value that can be over-ridden in the toolbox
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

        arcpy.AddMessage("Input feature had a coordinate system of: " + object_input.SpatialReference.name)
        arcpy.AddMessage("Output feature had a coordinate system of: " + object_output.SpatialReference.name)

        return


# The buffer tool is to buffer around a certain type of land cover to find suitable land
class BufferTool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Buffer Tool"
        self.description = "Creates buffer polygons around input features to a specified distance."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        params = []
        input_feature = arcpy.Parameter(name="input_feature",
                                        displayName="Input Feature",
                                        datatype="GPFeatureLayer",
                                        parameterType="Required",  # Required|Optional|Derived
                                        direction="Input",  # Input|Output
                                        )
        input_feature.value = r"Second_Select_Output.shp"  # This is a default value that can be over-ridden in the toolbox
        params.append(input_feature)

        buffer_distance = arcpy.Parameter(name="buffer_distance",
                                          displayName="Buffer Distance",
                                          datatype="GPLinearUnit",
                                          parameterType="Required",  # Required|Optional|Derived
                                          direction="Input",  # Input|Output
                                          )
        buffer_distance.parameterDependencies = [input_feature.name]  # This is a default value that can be over-ridden in the toolbox
        buffer_distance.value = "1 kilometer"
        params.append(buffer_distance)

        output_feature = arcpy.Parameter(name="output_feature",
                                         displayName="Output Feature",
                                         datatype="DEFeatureClass",
                                         parameterType="Required",  # Required|Optional|Derived
                                         direction="Output",  # Input|Output
                                         )
        output_feature.value = r"Buffer_Output.shp"  # This is a default value that can be over-ridden in the toolbox
        params.append(output_feature)

        buffer_method = arcpy.Parameter(displayName="Method",
                                        name="buffer_method",
                                        datatype="GPString",
                                        parameterType="Optional",  # Required|Optional|Derived
                                        direction="Input"  # Input|Output
                                        )
        buffer_method.filter.type = "Value List"
        buffer_method.filter.list = ["PLANAR", "GEODESIC"]
        params.append(buffer_method)

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
        input_feature = parameters[0].valueAsText
        buffer_distance = parameters[1].valueAsText
        output_feature = parameters[2].valueAsText
        buffer_method = parameters[3].valueAsText

        arcpy.Buffer_analysis(in_features=input_feature,
                              out_feature_class=output_feature,
                              buffer_distance_or_field=buffer_distance,
                              method=buffer_method)
        return



# The buffer tool is to buffer around a certain type of land cover to find suitable land
class SpeciesSplit(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Buffer Tool"
        self.description = "Creates buffer polygons around input features to a specified distance."
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
        params.append(input_folder)

        input_file = arcpy.Parameter(name="input_file",
                                     displayName="Input Species CSV file",
                                     datatype="DETable",
                                     parameterType="Required",  # Required|Optional|Derived
                                     direction="Input",  # Input|Output
                                     )
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

    def execute(self, parameters, messages):
        """The source code of the tool."""
        input_directory = parameters[0].valueAsText

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

        data_file = parameters[1].valueAsText
        define_species(data_file)

        return


# Test tools: FirstSelectTool, ClipTool, SecondSelectTool, BufferTool, SpeciesSplit
def main():
    tool = FirstSelectTool()
    tool.execute(tool.getParameterInfo(), None)

if __name__ == '__main__':
    main()




