#####
# Coding Challenge 4
# goal: selecting Washington County and clipping it to land cover layer, then selecting
# power lines located in this county. 
#####

import arcpy

# First, I want to select only Washington County in RI using the towns shapefile
arcpy.analysis.Select(in_features=r"C:\NRS528\Class_04\challenge4\towns\towns.shp",
                      out_feature_class=r"C:\NRS528\Class_04\challenge4\Washington_County.shp",
                      where_clause="COUNTY = 'WASHINGTON'")

# Next, I want to clip Washington County to the 2011 land cover shapefile
arcpy.analysis.Clip(in_features=r"C:\NRS528\Class_04\challenge4\land_cover_2011\land_cover_2011.shp",
                    clip_features=r"C:\NRS528\Class_04\challenge4\Washington_County.shp",
                    out_feature_class=r"C:\NRS528\Class_04\challenge4\study_area.shp",
                    cluster_tolerance="#")

# Finally, I can identify type of land cover using the Select tool again. For example, I would like to
# see where power lines are located in Washington County
arcpy.analysis.Select(in_features=r"C:\NRS528\Class_04\challenge4\study_area.shp",
                      out_feature_class=r"C:\NRS528\Class_04\challenge4\powerlines_location.shp",
                      where_clause="Descr_2011 = 'Power Lines (100'' or more width)'")
