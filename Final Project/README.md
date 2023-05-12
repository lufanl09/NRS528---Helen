# NRS 528 Semester Final Project

This is a toolbox that contains three main tools: Select and Describe, Split Species, and Create Shapefile. The first tool can use any shapefile the user would like to select a specific feature. The second tool uses a CSV file that includes different species and their coordinates. The last tool also uses the coordinates from the CSV file to generate shapefiles. All sample data are included. 

Select and Describe Tool
The Select tool is used to select a specific feature in the input, such as selecting a town as the study area.
In addition to Select, I also would like to obtain different elements of the data by using Describe.
This returns different properties of the data, such as the data type, fields, indexes, etc.
Here specifically, I would like to return the coordinate system.
Steps:
1. Set up input shapefile
2. Input where clause expression if needed
3. Output selected shapefile
4. Describe input and output features and add description message

Species Split Tool
This tool takes a CSV input and splits the table based on the species and create new CSV files.
Steps:
1. Set up input folder where the CSV file is located
2. Set up input CSV file
3. Create temporary files folder and output folder
4. Split CSV file

Create Shapefile
This tool creates shapefiles based on the species CSV files created by the Species Split Tool.
Steps:
1. Set up input file
2. Generate shapefile using Make XY Event Layer

